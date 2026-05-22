# -*- coding: utf-8 -*-
"""
L2语境层结构化提取脚本
从各行业Profile文件中提取L2语境豁免规则，生成结构化输出，便于：
  1. 验证各行业L2规则完整性
  2. 对比不同行业L2规则差异
  3. 快速检查新行业是否缺少L2规则

输出：
  - 控制台表格（按行业分组）
  - JSON格式的结构化数据（可选 --json 参数）

用法：
  python scripts/l2_context_generator.py
  python scripts/l2_context_generator.py --json  # 输出JSON格式

公众号内容智能生成器 v8.4.1
"""
import re
import sys
import json
from pathlib import Path
from typing import Optional


# ============================================================================
# 配置
# ============================================================================

SKILL_ROOT = Path(__file__).parent.parent.resolve()
PROFILES_DIR = SKILL_ROOT / "profiles"

PROFILE_NAMES = [
    "insurance", "healthcare", "finance", "education", "tech",
    "real-estate", "auto", "travel"
]


# ============================================================================
# L2规则提取器
# ============================================================================

class L2ContextExtractor:
    """从Profile文件中提取L2语境豁免规则"""

    # L2豁免规则章节标识
    L2_SECTION_PATTERNS = [
        r"##\s*八[、.]\s*语境豁免规则",   # 保险格式
        r"##\s*\d+[、.]\s*语境(?:层)?豁免",  # 通用格式
        r"##\s*L2.*?语境",                  # L2显式标记
        r"豁免规则",                          # 兜底
    ]

    # L2豁免规则表格列（顺序可能有变）
    TABLE_COL_PATTERN = re.compile(r"^\|(.+?)\|(.+?)\|(.+?)\|", re.MULTILINE)
    TABLE_SKIP_PATTERN = re.compile(r"^\|[-| :]+\|$")

    def extract(self, profile_name: str) -> dict:
        """提取指定Profile的L2规则"""
        path = PROFILES_DIR / f"{profile_name}.md"
        if not path.exists():
            return {"error": f"Profile不存在: {profile_name}"}

        content = path.read_text(encoding="utf-8")

        # 定位L2豁免章节
        section_content = self._find_l2_section(content)
        if not section_content:
            return {
                "profile": profile_name,
                "found": False,
                "rules": [],
                "summary": "未找到L2语境豁免规则章节"
            }

        # 提取表格规则
        rules = self._extract_table_rules(section_content)

        return {
            "profile": profile_name,
            "found": True,
            "rules": rules,
            "rule_count": len(rules),
            "summary": f"找到 {len(rules)} 条L2豁免规则"
        }

    def _find_l2_section(self, content: str) -> Optional[str]:
        """找到L2豁免规则章节的内容"""
        lines = content.split("\n")
        in_section = False
        section_lines = []
        heading_count = 0

        for line in lines:
            if re.match(r"##\s+\d+[、.]\s*", line):
                heading_count += 1
                if in_section:
                    break  # 遇到下一个章节，停止
                for pattern in self.L2_SECTION_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        in_section = True
                        section_lines.append(line)
                        break
            elif in_section:
                section_lines.append(line)

        return "\n".join(section_lines) if section_lines else None

    def _extract_table_rules(self, section_content: str) -> list:
        """从章节内容中提取表格规则"""
        rules = []
        rows = []

        for line in section_content.split("\n"):
            line = line.strip()
            if not line or self.TABLE_SKIP_PATTERN.match(line):
                continue
            if line.startswith("|") and "豁免语境" not in line:
                # 解析表格行
                cols = [c.strip() for c in line.split("|")]
                if len(cols) >= 3:
                    rows.append(cols[1:-1])  # 去掉首尾空列

        # 确定列映射
        for row in rows:
            if len(row) >= 3:
                rule = {
                    "context": row[0],
                    "exempted_terms": row[1],
                    "condition": row[2],
                    "required_note": row[3] if len(row) > 3 else "",
                }
                rules.append(rule)

        return rules


# ============================================================================
# 输出格式
# ============================================================================

def print_text_report(results: list):
    """打印文本格式报告"""
    print("\n" + "=" * 60)
    print("  L2 语境豁免规则 — 全行业结构化报告")
    print("=" * 60)

    total_rules = 0
    found_profiles = 0

    for r in results:
        profile = r["profile"]
        print(f"\n【{profile}】")
        if not r.get("found"):
            print(f"  ⚠️  {r.get('summary', '未找到L2规则')}")
            print("  💡 建议：在Profile文件中添加'## 八、语境豁免规则（L2层）'章节")
            continue

        found_profiles += 1
        rules = r["rules"]
        total_rules += len(rules)
        print(f"  ✅ 找到 {len(rules)} 条豁免规则：")
        print(f"  {'豁免语境':<18} | {'可豁免词':<18} | {'豁免条件'}")
        print(f"  {'-'*18}-+-{'-'*18}-+-{'-'*20}")

        for rule in rules:
            ctx = rule["context"][:16]
            term = rule["exempted_terms"][:16]
            cond = rule["condition"][:20]
            print(f"  {ctx:<18} | {term:<18} | {cond}")

    # 汇总
    print("\n" + "=" * 60)
    print("  汇总")
    print("=" * 60)
    print(f"  📊 Profile总数: {len(results)}")
    print(f"  ✅ 含L2规则: {found_profiles}")
    print(f"  ⚠️  缺L2规则: {len(results) - found_profiles}")
    print(f"  📝 规则总数: {total_rules}")

    # 识别缺失行业
    missing = [r["profile"] for r in results if not r.get("found")]
    if missing:
        print(f"\n  ⚠️  缺少L2规则的行业: {', '.join(missing)}")
        print("  💡 建议：为这些行业添加标准L2豁免规则章节")


def print_json_report(results: list):
    """打印JSON格式报告"""
    output = {
        "version": "v8.4.1",
        "generated_at": Path(__file__).stat().st_mtime,
        "summary": {
            "total_profiles": len(results),
            "with_l2_rules": sum(1 for r in results if r.get("found")),
            "without_l2_rules": sum(1 for r in results if not r.get("found")),
            "total_rules": sum(len(r["rules"]) for r in results if r.get("found")),
        },
        "profiles": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def print_structure_template():
    """打印标准L2豁免规则章节模板"""
    print("\n" + "=" * 60)
    print("  L2豁免规则章节模板（可直接复制到Profile文件）")
    print("=" * 60)
    template = """
## 八、语境豁免规则（L2层）

**合规扫描流程**：见 `../shared-definitions.md` 第二章

| 豁免语境 | 可豁免词 | 豁免条件 | 必须附加提示语 |
|----------|---------|---------|--------------|
| 专业对比评测 | {敏感词} | 需同时：①≥2款产品对比 ②客观数据支撑 ③非绝对化表述 | "以上对比仅供参考，以条款原文为准" |
| 条款解读 | {敏感词} | 需注明条款原文出处+保险公司+备案编号 | "以条款原文为准" |
| 行业数据引用 | {敏感词} | 需注明数据来源+统计周期+样本范围 | "数据来源：XX机构XX年度统计" |
"""
    print(template)


# ============================================================================
# 主函数
# ============================================================================

def main():
    print(f"🔍 L2语境豁免规则提取工具 — v8.4.1")
    print(f"   根目录: {SKILL_ROOT}\n")

    extractor = L2ContextExtractor()
    results = []

    for profile_name in PROFILE_NAMES:
        r = extractor.extract(profile_name)
        results.append(r)

    if "--json" in sys.argv:
        print_json_report(results)
    elif "--template" in sys.argv:
        print_structure_template()
    else:
        print_text_report(results)
        print_structure_template()

    # 检查一致性
    print("\n" + "=" * 60)
    print("  L2规则一致性检查")
    print("=" * 60)
    profiles_with_rules = [r for r in results if r.get("found")]
    if len(profiles_with_rules) < len(PROFILE_NAMES):
        print(f"  ⚠️  {len(profiles_with_rules)}/{len(PROFILE_NAMES)} 的Profile包含L2规则")
        print("  💡 使用 python scripts/l2_context_generator.py --template 查看标准模板")


if __name__ == "__main__":
    main()
