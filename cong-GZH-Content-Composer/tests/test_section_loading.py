# -*- coding: utf-8 -*-
"""
Section 文件加载完整性测试
验证 S1-S12 所有 section 文件存在且格式正确

测试内容：
  T1: S1-S12 文件全部存在
  T2: frontmatter 格式正确（name/version/description）
  T3: 章节编码在文件内一致（S1-S12 互引）
  T4: 与 SKILL.md 目录引用对齐
  T5: footer 版本号存在

公众号内容智能生成器 v8.4.1
"""
import re
import pytest
from pathlib import Path


# ============================================================================
# 期望数据（来源：SKILL.md 章节目录）
# ============================================================================

EXPECTED_SECTIONS = {
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

# SKILL.md 中记录的 token 消耗（用于一致性验证）
EXPECTED_TOKEN_CONSUMPTION = {
    "S1":  "~3,000字",
    "S2":  "~3,500字",
    "S3":  "~3,000字",
    "S4":  "~2,500字",
    "S5":  "~4,000字",
    "S6":  "~3,500字",
    "S7":  "~3,000字",
    "S8":  "~5,000字",
    "S9":  "~3,000字",
    "S10": "~2,500字",
    "S11": "~2,000字",
    "S12": "~3,500字",
}

# 必需 frontmatter 字段
REQUIRED_FRONTMATTER_FIELDS = ["name", "version", "description"]


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(scope="module")
def sections_dir(skill_root):
    return skill_root / "sections"


@pytest.fixture(scope="module")
def section_files(sections_dir):
    """加载所有 section 文件内容"""
    files = {}
    for code, filename in EXPECTED_SECTIONS.items():
        path = sections_dir / filename
        if path.exists():
            files[code] = {
                "path": path,
                "content": path.read_text(encoding="utf-8"),
                "filename": filename,
            }
        else:
            files[code] = {"path": path, "content": None, "filename": filename, "missing": True}
    return files


# ============================================================================
# T1: 文件存在性
# ============================================================================

class TestSectionExistence:
    """T1: 验证 S1-S12 所有文件存在"""

    @pytest.mark.parametrize("code", list(EXPECTED_SECTIONS.keys()))
    def test_file_exists(self, code, section_files):
        f = section_files[code]
        assert not f.get("missing"), (
            f"[T1] ❌ 文件缺失: {code} ({f['filename']}) "
            f"→ 期望路径: {f['path']}"
        )

    def test_all_files_exist_summary(self, section_files):
        missing = [code for code, f in section_files.items() if f.get("missing")]
        assert len(missing) == 0, f"[T1] ❌ 缺失文件: {missing}"


# ============================================================================
# T2: frontmatter 格式
# ============================================================================

class TestFrontmatterFormat:
    """T2: 验证所有 section 文件 frontmatter 格式正确"""

    FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL | re.MULTILINE)
    KEY_VALUE_PATTERN = re.compile(r"^(\w+):\s*(.*)$", re.MULTILINE)

    @pytest.mark.parametrize("code", list(EXPECTED_SECTIONS.keys()))
    def test_frontmatter_exists(self, code, section_files):
        f = section_files[code]
        assert f["content"] is not None, f"[T2-{code}] ❌ 文件内容为空"
        match = self.FRONTMATTER_PATTERN.match(f["content"])
        assert match is not None, f"[T2-{code}] ❌ frontmatter 格式缺失（应包含 --- 包裹的 YAML 头）"

    @pytest.mark.parametrize("code", list(EXPECTED_SECTIONS.keys()))
    def test_frontmatter_required_fields(self, code, section_files):
        f = section_files[code]
        if f.get("missing"):
            pytest.skip("文件不存在")
        match = self.FRONTMATTER_PATTERN.match(f["content"])
        fm_text = match.group(1)
        keys = {m.group(1): m.group(2).strip() for m in self.KEY_VALUE_PATTERN.finditer(fm_text)}
        for field in REQUIRED_FRONTMATTER_FIELDS:
            assert field in keys, f"[T2-{code}] ❌ 缺少必需字段: {field}"

    @pytest.mark.parametrize("code", list(EXPECTED_SECTIONS.keys()))
    def test_version_format(self, code, section_files):
        """验证版本号格式为 v8.x.x"""
        f = section_files[code]
        if f.get("missing"):
            pytest.skip("文件不存在")
        match = self.FRONTMATTER_PATTERN.match(f["content"])
        fm_text = match.group(1)
        keys = {m.group(1): m.group(2).strip() for m in self.KEY_VALUE_PATTERN.finditer(fm_text)}
        version = keys.get("version", "")
        assert re.match(r"^v\d+\.\d+\.\d+$", version), (
            f"[T2-{code}] ❌ version 格式错误: '{version}' → 应为 v数字.数字.数字"
        )

    @pytest.mark.parametrize("code", list(EXPECTED_SECTIONS.keys()))
    def test_version_consistency_with_main(self, code, section_files):
        """验证 section 版本与主版本一致（允许小版本差）"""
        f = section_files[code]
        if f.get("missing"):
            pytest.skip("文件不存在")
        match = self.FRONTMATTER_PATTERN.match(f["content"])
        fm_text = match.group(1)
        keys = {m.group(1): m.group(2).strip() for m in self.KEY_VALUE_PATTERN.finditer(fm_text)}
        section_version = keys.get("version", "")
        main_version = "v8.4.1"
        # 提取主版本号（允许子版本差：v8.4.1 与 v8.4.0 兼容）
        sec_parts = re.findall(r"\d+", section_version)
        main_parts = re.findall(r"\d+", main_version)
        assert sec_parts[:2] == main_parts[:2], (
            f"[T2-{code}] ❌ 主版本不一致: section={section_version}, main={main_version}"
        )


# ============================================================================
# T3: 章节编码一致性
# ============================================================================

class TestSectionCodeConsistency:
    """T3: 验证章节编码在文件内互引一致"""

    @pytest.mark.parametrize("code", list(EXPECTED_SECTIONS.keys()))
    def test_section_references_correct(self, code, section_files):
        """验证 S1-S12 的 section 文件内没有错误引用其他 section 代码"""
        f = section_files[code]
        if f.get("missing"):
            pytest.skip("文件不存在")
        content = f["content"]
        # 检查是否有错误引用不存在的 section（S99 等）
        wrong_refs = re.findall(r"S(\d{2,})", content)
        valid_codes = list(EXPECTED_SECTIONS.keys())
        valid_num = [int(code[1:]) for code in valid_codes]
        for ref in wrong_refs:
            num = int(ref)
            assert num <= 12, f"[T3-{code}] ❌ 引用了不存在的 section: S{ref}"

    @pytest.mark.parametrize("code", list(EXPECTED_SECTIONS.keys()))
    def test_no_circular_logic_errors(self, code, section_files):
        """检测明显的循环逻辑错误关键词"""
        f = section_files[code]
        if f.get("missing"):
            pytest.skip("文件不存在")
        content = f["content"]
        # 禁止：同一段落内无限递归引用自身
        lines = content.split("\n")
        for i, line in enumerate(lines):
            # 简单检测：同一行内多次出现同一 section 引用
            refs = re.findall(rf"\bS{code[1:]}\b", line)
            if len(refs) > 2:
                pytest.fail(f"[T3-{code}] ⚠️  第{i+1}行可能存在循环引用: {line.strip()[:80]}")


# ============================================================================
# T4: 与 SKILL.md 引用对齐
# ============================================================================

class TestSkillMdAlignment:
    """T4: 验证与 SKILL.md 章节目录引用完全对齐"""

    @pytest.mark.parametrize("code", list(EXPECTED_SECTIONS.keys()))
    def test_skill_md_references_section(self, code, section_files, skill_md):
        """验证 SKILL.md 章节目录中引用了所有 section"""
        filename = section_files[code]["filename"]
        # SKILL.md 应包含 {code} 和 {filename}
        assert code in skill_md, f"[T4-{code}] ❌ SKILL.md 未引用章节代码 {code}"
        assert filename in skill_md, f"[T4-{code}] ❌ SKILL.md 未引用文件名 {filename}"

    @pytest.mark.parametrize("code", list(EXPECTED_SECTIONS.keys()))
    def test_token_consumption_reasonable(self, code, section_files):
        """验证 token 消耗在合理范围内（防止占位符未填充）"""
        f = section_files[code]
        if f.get("missing"):
            pytest.skip("文件不存在")
        # 检查文件不为空（基本完整性检查）
        assert len(f["content"].strip()) > 200, (
            f"[T4-{code}] ❌ 文件内容过少（<200字符），可能是占位符"
        )

    def test_skill_md_section_table_complete(self, skill_md):
        """验证 SKILL.md 中章节目录表格 S1-S12 全部列出"""
        # 提取所有 S+数字 的引用
        found_codes = set(re.findall(r"\b(S\d{1,2})\b", skill_md))
        expected_codes = set(EXPECTED_SECTIONS.keys())
        missing_in_skill = expected_codes - found_codes
        assert len(missing_in_skill) == 0, (
            f"[T4] ❌ SKILL.md 缺少以下章节引用: {sorted(missing_in_skill)}"
        )


# ============================================================================
# T5: footer 版本号
# ============================================================================

class TestFooterVersion:
    """T5: 验证所有 section 文件 footer 包含版本号"""

    FOOTER_PATTERN = re.compile(r"\bv\d+\.\d+\.\d+\b")

    @pytest.mark.parametrize("code", list(EXPECTED_SECTIONS.keys()))
    def test_footer_has_version(self, code, section_files):
        f = section_files[code]
        if f.get("missing"):
            pytest.skip("文件不存在")
        # footer 应在文件末尾200字符内
        content = f["content"]
        footer_area = content[-200:] if len(content) > 200 else content
        versions = self.FOOTER_PATTERN.findall(footer_area)
        assert len(versions) >= 1, (
            f"[T5-{code}] ❌ footer 区域未找到版本号 v数字.数字.数字"
        )


# ============================================================================
# 测试报告汇总
# ============================================================================

def test_summary_report(section_files):
    """汇总报告：所有 section 文件健康状态"""
    report = []
    for code in sorted(EXPECTED_SECTIONS.keys()):
        f = section_files[code]
        status = "✅" if not f.get("missing") else "❌"
        filename = f["filename"]
        content = f.get("content", "")
        lines = len(content.split("\n")) if content else 0
        report.append(f"  {status} [{code}] {filename} ({lines}行)")

    print("\n\n" + "=" * 55)
    print("  Section 文件完整性报告")
    print("=" * 55)
    print("\n".join(report))
    print("=" * 55)

    missing = [code for code, f in section_files.items() if f.get("missing")]
    assert len(missing) == 0, f"有 {len(missing)} 个文件缺失"
