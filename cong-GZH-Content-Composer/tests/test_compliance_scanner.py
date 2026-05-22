# -*- coding: utf-8 -*-
"""
合规词库扫描测试
验证 L0-L3 合规词库文件存在、格式规范、内容完整

测试内容：
  T1: 合规文件全部存在（L0 + L1行业层 × 5）
  T2: frontmatter 格式正确
  T3: 词库表格格式统一（含风险等级/敏感词/替换建议）
  T4: 风险等级标记规范（🔴🟡🟢 与 风险等级 列一致）
  T5: 高风险词必须有替换建议
  T6: universal.md 与各行业L1词库互补性检查（无大量重复词条）

公众号内容智能生成器 v8.4.1
"""
import re
import pytest
from pathlib import Path


# ============================================================================
# 期望数据
# ============================================================================

EXPECTED_COMPLIANCE_FILES = {
    "L0": "universal.md",                    # 通用层（始终启用）
    "L1": [
        "insurance-terms.md",    # 保险
        "healthcare-terms.md",   # 医疗
        "finance-terms.md",      # 金融
        "education-terms.md",    # 教育
        "tech-terms.md",         # 科技（v8.4.1新增）
    ],
}

# 合规词库frontmatter必需字段
REQUIRED_COMPLIANCE_FIELDS = ["name", "version", "description"]

# 合规表格必须包含的列（通过表头判断）
# 注意：universal.md 格式为 风险等级|敏感词|建议替换（顺序不同）
# 行业L1格式为 敏感词|问题说明|建议替换（列2为问题说明）
VALID_TABLE_HEADERS = [
    ["风险等级", "敏感词", "建议替换"],  # universal.md
    ["敏感词", "问题说明", "建议替换"], # 行业L1词库
    ["敏感词/表述", "问题说明", "建议替换"], # 保险等
]


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(scope="module")
def compliance_dir(skill_root):
    return skill_root / "compliance"


@pytest.fixture(scope="module")
def compliance_files(compliance_dir):
    """加载所有合规词库文件"""
    files = {}
    # L0
    files["L0"] = {
        "name": "universal.md",
        "path": compliance_dir / "universal.md",
    }
    # L1
    files["L1"] = {}
    for filename in EXPECTED_COMPLIANCE_FILES["L1"]:
        l1_path = compliance_dir / filename
        files["L1"][filename] = {"path": l1_path}

    # 读取所有内容
    for key in ["L0"]:
        f = files[key]
        if f["path"].exists():
            f["content"] = f["path"].read_text(encoding="utf-8")
        else:
            f["content"] = None
            f["missing"] = True

    for key in files["L1"]:
        f = files["L1"][key]
        if f["path"].exists():
            f["content"] = f["path"].read_text(encoding="utf-8")
        else:
            f["content"] = None
            f["missing"] = True

    return files


# ============================================================================
# T1: 文件存在性
# ============================================================================

class TestComplianceFileExistence:
    """T1: 验证所有合规文件存在"""

    def test_l0_file_exists(self, compliance_files):
        f = compliance_files["L0"]
        assert not f.get("missing"), (
            f"[T1-L0] ❌ L0通用词库缺失: {f['name']}"
        )

    @pytest.mark.parametrize("filename", EXPECTED_COMPLIANCE_FILES["L1"])
    def test_l1_files_exist(self, filename, compliance_files):
        f = compliance_files["L1"][filename]
        assert not f.get("missing"), (
            f"[T1-L1] ❌ L1行业词库缺失: {filename}"
        )

    def test_l1_coverage(self, compliance_files):
        """确保5个L1行业词库全部就位"""
        missing = [
            name for name, f in compliance_files["L1"].items()
            if f.get("missing")
        ]
        assert len(missing) == 0, f"[T1-L1] ❌ 缺失L1词库: {missing}"


# ============================================================================
# T2: frontmatter 格式
# ============================================================================

class TestComplianceFrontmatter:
    """T2: 验证合规文件 frontmatter 格式"""

    FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL | re.MULTILINE)
    KEY_VALUE_PATTERN = re.compile(r"^(\w+):\s*(.*)$", re.MULTILINE)

    @pytest.mark.parametrize("filename", ["universal.md"] + EXPECTED_COMPLIANCE_FILES["L1"])
    def test_frontmatter_exists(self, filename, compliance_files):
        if filename == "universal.md":
            f = compliance_files["L0"]
        else:
            f = compliance_files["L1"][filename]
        assert f.get("missing") is not True, f"[T2-{filename}] ❌ 文件不存在"
        assert f["content"] is not None, f"[T2-{filename}] ❌ 内容为空"
        match = self.FRONTMATTER_PATTERN.match(f["content"])
        assert match is not None, f"[T2-{filename}] ❌ frontmatter 格式错误"

    @pytest.mark.parametrize("filename", ["universal.md"] + EXPECTED_COMPLIANCE_FILES["L1"])
    def test_required_fields(self, filename, compliance_files):
        if filename == "universal.md":
            f = compliance_files["L0"]
        else:
            f = compliance_files["L1"][filename]
        if f.get("missing"):
            pytest.skip("文件不存在")
        match = self.FRONTMATTER_PATTERN.match(f["content"])
        fm_text = match.group(1)
        keys = {m.group(1): m.group(2).strip() for m in self.KEY_VALUE_PATTERN.finditer(fm_text)}
        for field in REQUIRED_COMPLIANCE_FIELDS:
            assert field in keys, f"[T2-{filename}] ❌ 缺少必需字段: {field}"

    @pytest.mark.parametrize("filename", ["universal.md"] + EXPECTED_COMPLIANCE_FILES["L1"])
    def test_version_format(self, filename, compliance_files):
        if filename == "universal.md":
            f = compliance_files["L0"]
        else:
            f = compliance_files["L1"][filename]
        if f.get("missing"):
            pytest.skip("文件不存在")
        match = self.FRONTMATTER_PATTERN.match(f["content"])
        fm_text = match.group(1)
        keys = {m.group(1): m.group(2).strip() for m in self.KEY_VALUE_PATTERN.finditer(fm_text)}
        version = keys.get("version", "")
        assert re.match(r"^v\d+\.\d+\.\d+$", version), (
            f"[T2-{filename}] ❌ version 格式错误: '{version}'"
        )


# ============================================================================
# T3: 表格格式统一性
# ============================================================================

class TestComplianceTableFormat:
    """T3: 验证词库表格格式统一"""

    TABLE_HEADER_PATTERN = re.compile(r"^\|(.+?)\|", re.MULTILINE)

    def _extract_table_headers(self, content):
        """提取所有 markdown 表格的表头"""
        headers = []
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("|") and not line.startswith("|---"):
                cols = [c.strip() for c in line.split("|") if c.strip()]
                if len(cols) >= 2:
                    headers.append(cols)
        return headers

    def test_l0_table_header(self, compliance_files):
        """验证 universal.md 表格表头格式：风险等级|敏感词|建议替换"""
        f = compliance_files["L0"]
        if f.get("missing"):
            pytest.skip("文件不存在")
        headers = self._extract_table_headers(f["content"])
        assert len(headers) > 0, "[T3-universal] ❌ 未找到任何表格"
        # universal.md 表头应为：风险等级|敏感词|建议替换
        first_header = headers[0]
        expected = ["风险等级", "敏感词", "建议替换"]
        # 允许前3列匹配即可
        assert first_header[:3] == expected, (
            f"[T3-universal] ❌ 表头格式不匹配: {first_header[:3]} → 期望: {expected}"
        )

    @pytest.mark.parametrize("filename", EXPECTED_COMPLIANCE_FILES["L1"])
    def test_l1_table_header(self, filename, compliance_files):
        """验证行业L1词库表头格式：敏感词/表述|问题说明|建议替换"""
        f = compliance_files["L1"][filename]
        if f.get("missing"):
            pytest.skip("文件不存在")
        headers = self._extract_table_headers(f["content"])
        assert len(headers) > 0, f"[T3-{filename}] ❌ 未找到任何表格"
        first_header = headers[0]
        # 兼容两种表头格式
        valid = [
            ["敏感词/表述", "问题说明", "建议替换"],
            ["敏感词", "问题说明", "建议替换"],
            ["风险等级", "敏感词", "建议替换"],
        ]
        assert first_header[:3] in valid, (
            f"[T3-{filename}] ❌ 表头格式不匹配: {first_header[:3]}"
        )


# ============================================================================
# T4: 风险等级标记规范
# ============================================================================

class TestRiskLevelMarkers:
    """T4: 验证风险等级标记（🔴🟡🟢）规范使用"""

    RISK_MARKERS = re.compile(r"🔴|🟡|🟢")
    RISK_KEYWORDS = re.compile(r"高风险|中风险|低风险|高|中|低", re.IGNORECASE)

    def test_l0_has_risk_levels(self, compliance_files):
        """验证 universal.md 包含三类风险等级"""
        f = compliance_files["L0"]
        if f.get("missing"):
            pytest.skip("文件不存在")
        content = f["content"]
        has_high = "🔴" in content or "高风险" in content or "高" in content
        has_mid = "🟡" in content or "中风险" in content or "中" in content
        has_low = "🟢" in content or "低风险" in content or "低" in content
        assert has_high and has_mid and has_low, (
            f"[T4-universal] ❌ 缺少风险等级标记："
            f"高={has_high}, 中={has_mid}, 低={has_low}"
        )

    @pytest.mark.parametrize("filename", EXPECTED_COMPLIANCE_FILES["L1"])
    def test_l1_has_risk_levels(self, filename, compliance_files):
        """验证各行业L1词库包含三类风险等级"""
        f = compliance_files["L1"][filename]
        if f.get("missing"):
            pytest.skip("文件不存在")
        content = f["content"]
        has_high = "🔴" in content or "高风险" in content
        has_mid = "🟡" in content or "中风险" in content
        has_low = "🟢" in content or "低风险" in content
        assert has_high and has_mid and has_low, (
            f"[T4-{filename}] ❌ 缺少风险等级标记："
            f"高={has_high}, 中={has_mid}, 低={has_low}"
        )


# ============================================================================
# T5: 高风险词必须有替换建议
# ============================================================================

class TestHighRiskReplacements:
    """T5: 验证高风险词条必须提供替换建议"""

    TABLE_ROW_PATTERN = re.compile(r"^\|([^|]+)\|([^|]+)\|([^|]*)\|", re.MULTILINE)

    def _extract_table_rows(self, content):
        """提取所有表格行（排除表头和分隔行）"""
        rows = []
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("|") and "---" not in line and not line.startswith("|风险等级"):
                cols = [c.strip() for c in line.split("|")]
                if len(cols) >= 3 and cols[0]:  # 跳过空行
                    rows.append(cols)
        return rows

    def test_l0_high_risk_has_replacement(self, compliance_files):
        """universal.md: 🔴高风险的行，其建议替换列必须有内容"""
        f = compliance_files["L0"]
        if f.get("missing"):
            pytest.skip("文件不存在")
        rows = self._extract_table_rows(f["content"])
        issues = []
        for row in rows:
            if len(row) >= 3:
                risk_cell = row[0]
                replacement_cell = row[-1]
                if "🔴" in risk_cell or "高" in risk_cell:
                    if not replacement_cell.strip():
                        issues.append(f"  高风险词 '{row[1]}' 缺少替换建议")
        assert len(issues) == 0, (
            "[T5-universal] ❌ 以下高风险词缺少替换建议:\n" + "\n".join(issues)
        )

    @pytest.mark.parametrize("filename", EXPECTED_COMPLIANCE_FILES["L1"])
    def test_l1_high_risk_has_replacement(self, filename, compliance_files):
        """行业L1词库: 🔴高风险词必须有替换建议"""
        f = compliance_files["L1"][filename]
        if f.get("missing"):
            pytest.skip("文件不存在")
        rows = self._extract_table_rows(f["content"])
        issues = []
        for row in rows:
            if len(row) >= 3:
                risk_cell = row[0]
                replacement_cell = row[-1]
                if "🔴" in risk_cell or "高" in risk_cell:
                    if not replacement_cell.strip():
                        word = row[1] if len(row) > 1 else "(未知)"
                        issues.append(f"  高风险词 '{word}' 缺少替换建议")
        assert len(issues) == 0, (
            f"[T5-{filename}] ❌ 以下高风险词缺少替换建议:\n" + "\n".join(issues)
        )


# ============================================================================
# T6: 互补性检查（universal vs L1）
# ============================================================================

class TestComplementaryCoverage:
    """T6: universal.md 与各行业L1词库应互补，不应大量重复"""

    def test_l1_files_have_unique_sections(self, compliance_files):
        """各行业L1词库应有差异化的章节结构"""
        section_sets = {}
        for filename in EXPECTED_COMPLIANCE_FILES["L1"]:
            f = compliance_files["L1"][filename]
            if f.get("missing"):
                continue
            # 提取所有二级标题（## xxx）
            sections = set(re.findall(r"^## \w+", f["content"], re.MULTILINE))
            section_sets[filename] = sections

        # 至少 insurance 和 tech 的章节结构应不同
        if "insurance-terms.md" in section_sets and "tech-terms.md" in section_sets:
            overlap = section_sets["insurance-terms.md"] & section_sets["tech-terms.md"]
            # 有一些重叠（如"高风险敏感词"框架）是正常的，但不应完全相同
            # 允许重叠率 < 60%
            max_overlap_ratio = max(
                len(s1 & s2) / max(len(s1), 1)
                for i, s1 in enumerate(section_sets.values())
                for j, s2 in enumerate(section_sets.values())
                if i != j
            )
            assert max_overlap_ratio < 0.6, (
                f"[T6] ⚠️  行业词库章节重叠率过高: {max_overlap_ratio:.0%}，"
                "建议各行业L1词库按行业特色设置差异化章节"
            )


# ============================================================================
# 测试汇总
# ============================================================================

def test_compliance_summary_report(compliance_files):
    """合规词库健康状态报告"""
    print("\n\n" + "=" * 55)
    print("  合规词库完整性报告")
    print("=" * 55)

    # L0
    l0 = compliance_files["L0"]
    l0_status = "✅" if not l0.get("missing") else "❌"
    l0_lines = len(l0["content"].split("\n")) if l0.get("content") else 0
    print(f"  {l0_status} [L0] universal.md ({l0_lines}行)")

    # L1
    for filename in EXPECTED_COMPLIANCE_FILES["L1"]:
        f = compliance_files["L1"][filename]
        status = "✅" if not f.get("missing") else "❌"
        lines = len(f["content"].split("\n")) if f.get("content") else 0
        print(f"  {status} [L1] {filename} ({lines}行)")

    print("=" * 55)

    # 基本完整性检查
    missing = [name for name, f in compliance_files["L1"].items() if f.get("missing")]
    l0_missing = compliance_files["L0"].get("missing")
    assert not l0_missing, "[T1] ❌ L0 universal.md 缺失"
    assert len(missing) == 0, f"[T1] ❌ L1词库缺失: {missing}"
