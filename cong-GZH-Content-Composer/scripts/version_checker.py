# -*- coding: utf-8 -*-
"""
版本一致性检查脚本
检查所有文件的版本号是否同步，引用路径是否存在

检查项：
  V1: SKILL.md 与 shared-definitions.md 主版本同步
  V2: 所有 section 文件（S1-S12）版本一致
  V3: 所有 compliance 文件版本一致
  V4: 所有 profiles 文件版本一致
  V5: SKILL.md 中引用的文件路径全部存在
  V6: CHANGELOG 中最新版本的变更记录与实际修改文件一致
  V7: frameworks.md / examples/style-preview.html 版本合理性
  V8: 正文标题版本号与 frontmatter 一致性校验（新增）

用法：
  python scripts/version_checker.py
  python scripts/version_checker.py --fix  # 自动修复可修复的问题

公众号内容智能生成器 v8.5.0
"""
import re
import sys
from pathlib import Path
from datetime import datetime

# Windows 控制台 UTF-8 支持
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# ============================================================================
# 配置
# ============================================================================

SKILL_ROOT = Path(__file__).parent.parent.resolve()
MAIN_VERSION = "v8.5.0"          # 当前主版本（需手动更新发布新版本时）
ENFORCE_MAIN_VERSION = True       # 是否强制所有文件版本号与主版本一致


# ============================================================================
# 工具函数
# ============================================================================

def get_version(content):
    """从文件中提取版本号（支持 frontmatter 或 blockquote 格式）"""
    # 优先尝试 YAML frontmatter
    fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL | re.MULTILINE)
    if fm_match:
        fm_text = fm_match.group(1)
        v_match = re.search(r"version:\s*(v?\d+\.\d+\.\d+)", fm_text)
        if v_match:
            return v_match.group(1)

    # 兜底：blockquote格式 > **版本**：v8.x.x
    patterns = [
        r">\s*\*版本\*[：:]\s*(v?\d+\.\d+\.\d+)",
        r">\s*版本[：:]\s*(v?\d+\.\d+\.\d+)",
        r"\bv\d+\.\d+\.\d+\b",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if "/" not in match:  # 排除URL格式
                return match
    return None


def print_header(text):
    print(f"\n{'=' * 55}")
    print(f"  {text}")
    print("=" * 55)


def get_version_from_footer(content):
    """从 footer 中提取版本号（最后300字符）"""
    footer = content[-300:] if len(content) > 300 else content
    matches = re.findall(r"\bv\d+\.\d+\.\d+\b", footer)
    return matches[-1] if matches else None


def print_result(passed, message):
    icon = "✅" if passed else "❌"
    print(f"  {icon} {message}")


def print_warning(message):
    print(f"  ⚠️  {message}")


# ============================================================================
# V1: 主版本一致性
# ============================================================================

def check_main_version_consistency():
    """检查 SKILL.md 与 shared-definitions.md 版本一致"""
    print_header("V1: 主版本一致性检查")

    skill_path = SKILL_ROOT / "SKILL.md"
    shared_path = SKILL_ROOT / "shared-definitions.md"

    if not skill_path.exists():
        print_result(False, f"SKILL.md 不存在: {skill_path}")
        return False
    if not shared_path.exists():
        print_result(False, f"shared-definitions.md 不存在: {shared_path}")
        return False

    skill_content = skill_path.read_text(encoding="utf-8")
    shared_content = shared_path.read_text(encoding="utf-8")

    skill_version = get_version(skill_content)
    shared_version = get_version(shared_content)

    # 检查frontmatter版本
    fm_match = skill_version == shared_version
    print_result(fm_match, f"SKILL.md 版本: {skill_version}")
    print_result(fm_match, f"shared-definitions.md 版本: {shared_version}")

    if ENFORCE_MAIN_VERSION:
        skill_main_ok = skill_version == MAIN_VERSION
        shared_main_ok = shared_version == MAIN_VERSION
        print_result(skill_main_ok, f"SKILL.md 应为 {MAIN_VERSION}: {skill_version}")
        print_result(shared_main_ok, f"shared-def. 应为 {MAIN_VERSION}: {shared_version}")
        return skill_main_ok and shared_main_ok and fm_match
    else:
        return fm_match


# ============================================================================
# V2: Section 文件版本一致性
# ============================================================================

SECTION_FILES = {
    "S1":  "quick-mode.md",
    "S2":  "standard-mode.md",
    "S3":  "rewrite-mode.md",
    "S4":  "batch-mode.md",
    "S5":  "layout-presets.md",
    "S6":  "html-structure.md",
    "S7":  "topic-inspiration.md",
    "S8":  "channel-adaptation.md",
    "S9":  "content-review.md",
    "S10": "shortcut-mode.md",
    "S11": "error-handling.md",
    "S12": "emotional-resonance.md",
}


def check_section_versions():
    """检查所有 section 文件版本一致性"""
    print_header("V2: Section 文件版本一致性")

    sections_dir = SKILL_ROOT / "sections"
    if not sections_dir.exists():
        print_result(False, f"sections/ 目录不存在: {sections_dir}")
        return False

    all_ok = True
    versions_found = {}

    for code, filename in SECTION_FILES.items():
        path = sections_dir / filename
        if not path.exists():
            print_result(False, f"[{code}] 文件缺失: {filename}")
            all_ok = False
            continue

        content = path.read_text(encoding="utf-8")
        version = get_version(content)
        ft_version = get_version_from_footer(content)

        if version:
            versions_found[code] = version
        else:
            print_result(False, f"[{code}] 未找到版本号")
            all_ok = False
            continue

        # 检查frontmatter版本与footer版本是否一致
        if version and ft_version and version != ft_version:
            print_warning(f"[{code}] 检测版本={version}, footer={ft_version}（不一致）")

        # 与主版本比较（允许小版本差）
        v_parts = re.findall(r"\d+", version or "")
        main_parts = re.findall(r"\d+", MAIN_VERSION)
        version_ok = v_parts[:2] == main_parts[:2]
        print_result(version_ok, f"[{code}] {filename}: {version} (vs 主版本 {MAIN_VERSION})")

    # 检查所有section版本是否一致（允许与主版本差1个修订号）
    unique_versions = set(versions_found.values())
    if len(unique_versions) > 2:
        print_warning(f"⚠️  检测到 {len(unique_versions)} 个不同版本号: {unique_versions}")
        print_warning("建议统一为同一主版本（前两个数字一致即可）")
    else:
        print_result(True, f"所有section版本一致: {unique_versions}")

    return all_ok


# ============================================================================
# V3: Compliance 文件版本一致性
# ============================================================================

COMPLIANCE_FILES = [
    "universal.md",
    "insurance-terms.md",
    "healthcare-terms.md",
    "finance-terms.md",
    "education-terms.md",
    "tech-terms.md",
]


def check_compliance_versions():
    """检查所有 compliance 文件版本一致性"""
    print_header("V3: Compliance 词库版本一致性")

    compliance_dir = SKILL_ROOT / "compliance"
    if not compliance_dir.exists():
        print_result(False, f"compliance/ 目录不存在: {compliance_dir}")
        return False

    all_ok = True
    versions_found = {}

    for filename in COMPLIANCE_FILES:
        path = compliance_dir / filename
        if not path.exists():
            print_result(False, f"文件缺失: {filename}")
            all_ok = False
            continue

        content = path.read_text(encoding="utf-8")
        version = get_version(content)

        if version:
            versions_found[filename] = version
        else:
            print_result(False, f"未找到版本号: {filename}")
            all_ok = False
            continue

        v_parts = re.findall(r"\d+", version)
        main_parts = re.findall(r"\d+", MAIN_VERSION)
        version_ok = v_parts[:2] == main_parts[:2]
        print_result(version_ok, f"{filename}: {version}")

    unique_versions = set(versions_found.values())
    if len(unique_versions) > 3:
        print_warning(f"⚠️  合规词库有 {len(unique_versions)} 个不同版本")
    else:
        print_result(True, f"合规词库版本: {unique_versions}")

    return all_ok


# ============================================================================
# V4: Profiles 文件版本一致性
# ============================================================================

PROFILE_FILES = [
    "insurance.md", "healthcare.md", "finance.md", "education.md",
    "tech.md", "real-estate.md", "auto.md", "travel.md",
]


def check_profile_versions():
    """检查所有 profiles 文件版本一致性"""
    print_header("V4: 行业Profile版本一致性")

    profiles_dir = SKILL_ROOT / "profiles"
    if not profiles_dir.exists():
        print_result(False, f"profiles/ 目录不存在: {profiles_dir}")
        return False

    all_ok = True
    versions_found = {}

    for filename in PROFILE_FILES:
        path = profiles_dir / filename
        if not path.exists():
            print_result(False, f"文件缺失: {filename}")
            all_ok = False
            continue

        content = path.read_text(encoding="utf-8")
        version = get_version(content)

        if version:
            versions_found[filename] = version
        else:
            print_warning(f"未找到版本号: {filename}（建议补充）")
            all_ok = False

        fm_parts = re.findall(r"\d+", version or "")
        main_parts = re.findall(r"\d+", MAIN_VERSION)
        version_ok = fm_parts[:2] == main_parts[:2]
        print_result(version_ok, f"{filename}: {version or '无版本号'}")

    unique_versions = set(v for v in versions_found.values() if v)
    if len(unique_versions) > 2:
        print_warning(f"⚠️  Profile有 {len(unique_versions)} 个不同版本: {unique_versions}")

    return all_ok


# ============================================================================
# V5: SKILL.md 引用的文件路径存在性
# ============================================================================

def check_skill_md_references():
    """检查 SKILL.md 中引用的所有文件路径是否存在"""
    print_header("V5: SKILL.md 文件引用完整性")

    skill_path = SKILL_ROOT / "SKILL.md"
    content = skill_path.read_text(encoding="utf-8")

    # 提取所有文件路径引用（排除模板占位符）
    # 模板占位符特征：包含 {xxx} 的反引号内容
    path_pattern = re.compile(
        r"`([^`]+\.md)`|`([^`]+/)`|"
        r"section[s]?/(\w+\.md)|profiles/(\w+\.md)|"
        r"compliance/(\w+\.md)|templates/(\w+\.md)|examples/(\w+\.\w+)"
    )

    # 模板占位符特征：路径中包含 {字母或中文}
    PLACEHOLDER_PATTERN = re.compile(r"\{[\w\u4e00-\u9fa5]+\}")

    all_ok = True
    checked = 0
    skipped_placeholders = 0

    for match in path_pattern.finditer(content):
        for group_idx in range(1, len(match.groups()) + 1):
            path_str = match.group(group_idx)
            if path_str:
                # 跳过模板占位符（如 {行业代码}.md, {industry_code}-terms.md）
                if PLACEHOLDER_PATTERN.search(path_str):
                    skipped_placeholders += 1
                    continue
                checked += 1
                full_path = SKILL_ROOT / path_str
                if not full_path.exists():
                    print_result(False, f"引用文件不存在: {path_str}")
                    all_ok = False

    if all_ok:
        print_result(True, f"所有引用路径均存在（已跳过{skipped_placeholders}个模板占位符）")
    return all_ok


# ============================================================================
# V6: CHANGELOG 覆盖性
# ============================================================================

def check_changelog_coverage():
    """检查 CHANGELOG 中最新版本的变更记录是否与实际文件匹配"""
    print_header("V6: CHANGELOG 覆盖性检查")

    changelog_path = SKILL_ROOT / "CHANGELOG.md"
    if not changelog_path.exists():
        print_result(False, f"CHANGELOG.md 不存在")
        return False

    content = changelog_path.read_text(encoding="utf-8")

    # 提取最新版本（第一个 ## v8.x.x）
    latest_version_match = re.search(r"##\s+(v\d+\.\d+\.\d+)", content)
    if not latest_version_match:
        print_result(False, "未找到版本标记 ## v数字.数字.数字")
        return False

    latest_version = latest_version_match.group(1)
    print(f"  📌 最新版本: {latest_version}")

    # 提取该版本下所有提及的文件名
    # 找到版本标题到下一个版本标题之间的内容
    version_header = latest_version_match.group(0)
    end_pos = latest_version_match.end()
    next_version = re.search(r"\n##\s+v\d+\.\d+\.\d+", content[end_pos:])
    if next_version:
        version_section = content[end_pos:end_pos + next_version.start()]
    else:
        version_section = content[end_pos:]

    # 提取所有 .md 文件引用
    referenced_files = set(re.findall(r"`([^`]+\.md)`", version_section))
    # 排除 CHANGELOG.md 自身
    referenced_files.discard("CHANGELOG.md")

    if len(referenced_files) == 0:
        print_warning(f"⚠️  {latest_version} 版本记录的文件变更数量为0")
        print_warning("建议在 CHANGELOG 中记录本次修改的文件")
        return False

    print(f"  📝 CHANGELOG记录的变更文件数: {len(referenced_files)}")
    for f in sorted(referenced_files):
        print(f"    - {f}")

    # 检查所有记录的文件是否存在
    all_ok = True
    for filename in referenced_files:
        full_path = SKILL_ROOT / filename
        if not full_path.exists():
            print_result(False, f"CHANGELOG记录了不存在的文件: {filename}")
            all_ok = False

    print_result(all_ok, f"CHANGELOG覆盖性: {len(referenced_files)}个文件")
    return all_ok


def get_version_from_body_heading(content):
    """从正文第一行标题提取版本号（如 '# 某文件 v8.5.0'）"""
    first_line = content.split('\n')[0]
    match = re.search(r'#\s+.*[vV](\d+\.\d+\.\d+)', first_line)
    return match.group(1) if match else None


# ============================================================================
# V8: 正文标题版本号与 frontmatter 一致性校验（新增）
# ============================================================================

def check_body_vs_frontmatter_versions():
    """检查有 frontmatter 的 .md 文件中，正文标题版本号是否与 frontmatter 一致"""
    print_header("V8: 正文标题与Frontmatter版本一致性")

    all_ok = True
    checked = 0
    mismatched = []

    for md_file in SKILL_ROOT.rglob("*.md"):
        if md_file.is_dir():
            continue
        content = md_file.read_text(encoding="utf-8")

        # 提取 frontmatter 版本
        fm_version = None
        fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL | re.MULTILINE)
        if fm_match:
            v_match = re.search(r"version:\s*(v?\d+\.\d+\.\d+)", fm_match.group(1))
            if v_match:
                fm_version = v_match.group(1)

        # 提取正文标题版本
        body_version = get_version_from_body_heading(content.split('---\n')[-1] if '---\n' in content else content)

        if fm_version and body_version:
            checked += 1
            relative_path = md_file.relative_to(SKILL_ROOT)
            if fm_version != body_version:
                mismatched.append(f"{relative_path}: fm={fm_version} ≠ body={body_version}")
                print_result(False, f"{relative_path}: frontmatter={fm_version} ≠ 正文标题={body_version}")
                all_ok = False
            else:
                print_result(True, f"{relative_path}: {fm_version} ✓")

    if checked == 0:
        print_warning("未找到同时有 frontmatter 和正文标题版本号的文件")
    elif all_ok:
        print_result(True, f"全部 {checked} 个文件正文标题与 frontmatter 版本一致")

    if mismatched:
        print(f"\n  🔧 自动修复建议：以下文件需要手动同步")
        for m in mismatched:
            print(f"    - {m}")

    return all_ok


# ============================================================================
# V7: 框架和示例文件版本合理性
# ============================================================================

def check_other_files():
    """检查 frameworks.md 和 examples/style-preview.html 版本合理性"""
    print_header("V7: 框架和示例文件版本")

    all_ok = True

    # frameworks.md
    fw_path = SKILL_ROOT / "frameworks.md"
    if fw_path.exists():
        content = fw_path.read_text(encoding="utf-8")
        version = get_version(content)
        v_parts = re.findall(r"\d+", version or "")
        main_parts = re.findall(r"\d+", MAIN_VERSION)
        version_ok = v_parts[:2] == main_parts[:2]
        print_result(version_ok, f"frameworks.md: {version} (vs {MAIN_VERSION})")
    else:
        print_result(False, "frameworks.md 不存在")
        all_ok = False

    # examples/style-preview.html
    ex_path = SKILL_ROOT / "examples" / "style-preview.html"
    if ex_path.exists():
        content = ex_path.read_text(encoding="utf-8")
        version = get_version(content)
        v_parts = re.findall(r"\d+", version or "")
        main_parts = re.findall(r"\d+", MAIN_VERSION)
        version_ok = v_parts[:2] == main_parts[:2]
        print_result(version_ok, f"examples/style-preview.html: {version} (vs {MAIN_VERSION})")
    else:
        print_result(False, "examples/style-preview.html 不存在")
        all_ok = False

    return all_ok


# ============================================================================
# 主函数
# ============================================================================

def run_all_checks():
    """运行所有版本检查"""
    print(f"\n🔍 公众号内容智能生成器 v{MAIN_VERSION} - 版本一致性检查")
    print(f"   检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   根目录: {SKILL_ROOT}")

    results = {}

    results["V1-主版本一致性"] = check_main_version_consistency()
    results["V2-Section版本"] = check_section_versions()
    results["V3-Compliance版本"] = check_compliance_versions()
    results["V4-Profile版本"] = check_profile_versions()
    results["V5-引用路径完整性"] = check_skill_md_references()
    results["V6-CHANGELOG覆盖"] = check_changelog_coverage()
    results["V7-其他文件版本"] = check_other_files()
    results["V8-标题Frontmatter一致性"] = check_body_vs_frontmatter_versions()

    # 汇总
    print_header("版本一致性检查汇总")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for name, ok in results.items():
        print_result(ok, name)

    print(f"\n  通过率: {passed}/{total} ({passed/total:.0%})")

    if passed == total:
        print("\n  🎉 所有版本检查通过！")
        return True
    else:
        failures = [k for k, v in results.items() if not v]
        print(f"\n  ❌ 失败项: {', '.join(failures)}")
        return False


if __name__ == "__main__":
    # 支持 --fix 参数（预留扩展）
    if "--fix" in sys.argv:
        print("⚠️  自动修复模式暂未实现，请手动修复上述问题。")

    ok = run_all_checks()
    sys.exit(0 if ok else 1)
