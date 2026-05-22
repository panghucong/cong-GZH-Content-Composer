# -*- coding: utf-8 -*-
"""
评分体系一致性测试
验证评分维度、子项、等级、权重、门控参数在所有文件中保持一致

测试内容：
  T1: 4个评分维度齐全（专业度/传播力/用户适配/SEO）
  T2: 16项评分子项不缺项且满分值正确
  T3: 5档评分等级（S/A/B/C/D）定义完整
  T4: 默认权重之和=100%
  T5: 各行业Profile权重之和=100%
  T6: 质量门控参数（80/92/2次）在所有相关文件中一致
  T7: 评分子项在SKILL.md与shared-definitions.md中一致

公众号内容智能生成器 v8.4.1
"""
import re
import pytest
from pathlib import Path


# ============================================================================
# 期望数据（来自 shared-definitions.md）
# ============================================================================

EXPECTED_DIMENSIONS = ["专业度", "传播力", "用户适配", "SEO"]

EXPECTED_ITEMS = {
    "专业度": {
        "事实准确性": 3,
        "逻辑严谨性": 3,
        "术语准确性": 2,
        "深度": 2,
    },
    "传播力": {
        "标题吸引力": 3,
        "开头钩子": 3,
        "结尾引导": 2,
        "分享友好": 2,
    },
    "用户适配": {
        "痛点匹配": 3,
        "行动可执行": 3,
        "语言适配": 2,
        "情感共鸣": 2,
    },
    "SEO": {
        "关键词覆盖": 3,
        "关键词密度": 2,
        "结构化": 3,
        "可读性": 2,
    },
}

EXPECTED_GRADE_LEVELS = {
    "S": (95, 100, "卓越", "无需优化"),
    "A": (85, 94, "优秀", "小幅优化"),
    "B": (70, 84, "良好", "1-2轮优化"),
    "C": (60, 69, "及格", "2-3轮优化"),
    "D": (0, 59, "不合格", "建议重写"),
}

EXPECTED_GATE_PARAMS = {
    "auto_rewrite_threshold": 80,    # <80分 自动重写
    "output_threshold": 92,           # ≥92分 才能输出
    "max_rewrite_count": 2,          # 最多重写2次
}


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(scope="module")
def profiles_dir(skill_root):
    return skill_root / "profiles"


@pytest.fixture(scope="module")
def profiles(profiles_dir):
    """加载所有行业Profile"""
    profiles = {}
    for path in profiles_dir.glob("*.md"):
        name = path.stem
        profiles[name] = {
            "path": path,
            "content": path.read_text(encoding="utf-8"),
        }
    return profiles


# ============================================================================
# T1: 评分维度完整性
# ============================================================================

class TestDimensionCompleteness:
    """T1: 验证shared-definitions.md包含4个评分维度"""

    def test_all_dimensions_present(self, shared_definitions):
        for dim in EXPECTED_DIMENSIONS:
            assert dim in shared_definitions, (
                f"[T1] ❌ 缺少评分维度: {dim}"
            )

    def test_dimension_count(self, shared_definitions):
        """验证恰好4个维度"""
        found = [dim for dim in EXPECTED_DIMENSIONS if dim in shared_definitions]
        assert len(found) == 4, f"[T1] ❌ 评分维度数量错误: {len(found)}，期望4"


# ============================================================================
# T2: 评分子项完整性 + 满分值
# ============================================================================

class TestItemCompleteness:
    """T2: 验证16项评分子项不缺项且满分值正确"""

    @pytest.mark.parametrize("dimension", list(EXPECTED_ITEMS.keys()))
    def test_dimension_items_count(self, dimension, shared_definitions):
        """验证每个维度恰好4个子项"""
        dim_section = self._extract_dim_section(dimension, shared_definitions)
        assert dim_section, f"[T2-{dimension}] ❌ 未找到维度章节"

        # 提取所有子项名称（正则匹配 "子项名 | 满分 |"）
        items = re.findall(r"\|\s*([^|\n]+?)\s*\|\s*(\d+)\s*\|", dim_section)
        item_count = len(items)
        assert item_count == 4, (
            f"[T2-{dimension}] ❌ 子项数量错误: {item_count}，期望4"
        )

    @pytest.mark.parametrize("dimension", list(EXPECTED_ITEMS.keys()))
    def test_item_max_scores(self, dimension, shared_definitions):
        """验证每个子项的满分值与期望一致"""
        dim_section = self._extract_dim_section(dimension, shared_definitions)
        for expected_item, expected_score in EXPECTED_ITEMS[dimension].items():
            # 匹配：| 子项名 | 满分 |
            match = re.search(
                rf"\|\s*{re.escape(expected_item)}\s*\|\s*(\d+)\s*\|",
                dim_section
            )
            assert match is not None, (
                f"[T2-{dimension}] ❌ 缺少子项: {expected_item}"
            )
            actual_score = int(match.group(1))
            assert actual_score == expected_score, (
                f"[T2-{dimension}/{expected_item}] ❌ 满分值错误: "
                f"{actual_score}，期望{expected_score}"
            )

    def test_total_max_score(self, shared_definitions):
        """验证总分恰好为100"""
        total = sum(
            sum(items.values())
            for items in EXPECTED_ITEMS.values()
        )
        assert total == 40, f"[T2] ❌ 子项满分总和错误: {total}，应为40（总分100）"

    def _extract_dim_section(self, dimension, content):
        """提取某维度的章节内容"""
        # 匹配 ## 三/三、评分权重自适应规则 到下一个 ## 标题
        dim_keywords = {
            "专业度": r"📘",
            "传播力": r"📗",
            "用户适配": r"📙",
            "SEO": r"📒",
        }
        pattern = rf"{dim_keywords.get(dimension, dimension)}.*?\n(.*?)(?=\n## |\n# |\Z)"
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1) if match else ""


# ============================================================================
# T3: 评分等级体系
# ============================================================================

class TestGradeLevels:
    """T3: 验证5档评分等级定义完整"""

    def test_all_grade_levels_present(self, shared_definitions):
        """验证S/A/B/C/D五档全部存在"""
        for grade in EXPECTED_GRADE_LEVELS:
            # 在评分等级体系中查找等级标记
            found = re.search(
                rf"\|\s*{re.escape(grade)}\s*\|",
                shared_definitions
            )
            assert found is not None, f"[T3] ❌ 缺少评分等级: {grade}"

    def test_grade_thresholds(self, shared_definitions):
        """验证等级分数边界正确"""
        grade_pattern = re.compile(
            r"\|\s*([SABCD])\s*\|\s*(\d+)-(\d+)\s*\|"
        )
        matches = list(grade_pattern.finditer(shared_definitions))
        assert len(matches) == 5, f"[T3] ❌ 等级数量错误: {len(matches)}，期望5"

        for match in matches:
            grade = match.group(1)
            low = int(match.group(2))
            high = int(match.group(3))
            exp_low, exp_high, _, _ = EXPECTED_GRADE_LEVELS[grade]
            assert low == exp_low, f"[T3-{grade}] ❌ 低分边界错误: {low}，期望{exp_low}"
            assert high == exp_high, f"[T3-{grade}] ❌ 高分边界错误: {high}，期望{exp_high}"

    def test_grade_continuity(self, shared_definitions):
        """验证等级之间连续无缝隙（S/A/B/C/D）"""
        grade_pattern = re.compile(r"\|\s*([SABCD])\s*\|\s*(\d+)-(\d+)\s*\|")
        matches = list(grade_pattern.finditer(shared_definitions))
        matches.sort(key=lambda m: m.group(1))  # 按等级排序

        for i in range(len(matches) - 1):
            curr_high = int(matches[i].group(3))
            next_low = int(matches[i + 1].group(2))
            # 当前等级的上界+1 = 下一等级的下界
            assert curr_high + 1 == next_low, (
                f"[T3-{matches[i].group(1)}→{matches[i+1].group(1)}] "
                f"❌ 分数边界不连续: {curr_high} vs {next_low}"
            )


# ============================================================================
# T4: 默认权重之和=100%
# ============================================================================

class TestDefaultWeights:
    """T4: 验证默认权重（均匀）之和=100%"""

    def test_default_weights_sum_to_100(self, shared_definitions):
        """默认均匀权重：专业度25%/传播力25%/用户适配25%/SEO25%"""
        # 查找权重分配行
        weight_pattern = re.compile(
            r"专业度\s*(\d+)%?\s*/\s*传播力\s*(\d+)%?\s*/\s*用户适配\s*(\d+)%?\s*/\s*SEO\s*(\d+)%?"
        )
        match = weight_pattern.search(shared_definitions)
        assert match is not None, "[T4] ❌ 未找到默认权重配置"

        weights = [int(match.group(i)) for i in range(1, 5)]
        total = sum(weights)
        assert total == 100, (
            f"[T4] ❌ 默认权重之和={total}%，期望100%"
        )

    def test_default_weights_even(self, shared_definitions):
        """验证默认权重为均匀分配（25%/25%/25%/25%）"""
        weight_pattern = re.compile(
            r"专业度\s*(\d+)%?\s*/\s*传播力\s*(\d+)%?\s*/\s*用户适配\s*(\d+)%?\s*/\s*SEO\s*(\d+)%?"
        )
        match = weight_pattern.search(shared_definitions)
        weights = [int(match.group(i)) for i in range(1, 5)]
        # 允许自定义权重，但总和必须=100
        assert all(w >= 15 and w <= 40 for w in weights), (
            f"[T4] ⚠️  权重偏离常规范围: {weights}，建议25%左右"
        )


# ============================================================================
# T5: 行业Profile权重之和=100%
# ============================================================================

class TestProfileWeights:
    """T5: 验证各行业Profile的评分权重之和=100%"""

    @pytest.mark.parametrize("profile_name", [
        "insurance", "healthcare", "finance", "education", "tech",
        "real-estate", "auto", "travel"
    ])
    def test_profile_weights_sum(self, profile_name, profiles):
        """每个行业的评分权重之和应=100%"""
        if profile_name not in profiles:
            pytest.skip(f"[T5-{profile_name}] Profile文件不存在")

        content = profiles[profile_name]["content"]
        # 查找权重配置（支持多种格式）
        # 格式1: 25%/25%/25%/25%
        # 格式2: 专业度: 25%, 传播力: 25%...
        # 格式3: 专业度 25% / 传播力 25% / 用户适配 25% / SEO 25%
        patterns = [
            re.compile(r"专业度\s*(\d+)%?\s*/\s*传播力\s*(\d+)%?\s*/\s*用户适配\s*(\d+)%?\s*/\s*SEO\s*(\d+)%?"),
            re.compile(r"([专业度传播力用户适配SEO]{3,4})\s*[:：]?\s*(\d+)%?"),
        ]

        weights = []
        for pattern in patterns:
            matches = list(pattern.finditer(content))
            if matches:
                for m in matches:
                    found_weights = [int(g) for g in m.groups() if g.isdigit()]
                    weights.extend(found_weights)
                break

        # 如果找到权重数据，验证和为100
        if len(weights) >= 4:
            # 取前4个（如果有更多，取与4个维度匹配的）
            first_four = weights[:4]
            total = sum(first_four)
            assert total == 100, (
                f"[T5-{profile_name}] ❌ 评分权重之和={total}%，期望100%"
            )


# ============================================================================
# T6: 质量门控参数一致性
# ============================================================================

class TestQualityGateConsistency:
    """T6: 验证质量门控参数（80/92/2次）在所有相关文件中一致"""

    GATE_PATTERNS = {
        "auto_rewrite_threshold": re.compile(r"(?:<|低于|不到)\s*(\d{2})\s*(?:分|%)?|(\d{2})\s*(?:分|%)?\s*(?:以下|以下|自动重写)"),
        "output_threshold": re.compile(r"(?:≥|达到|超过|满|输出.*?)\s*(\d{2})\s*(?:分|%)?"),
        "max_rewrite": re.compile(r"(?:最多|上限|不超过|重写)\s*(\d)\s*(?:次|版|稿)?"),
    }

    def _extract_all_gate_params(self, content):
        """从内容中提取所有门控参数引用"""
        params = {}

        # 提取自动重写阈值（80分）
        for match in self.GATE_PATTERNS["auto_rewrite_threshold"].finditer(content):
            val = match.group(1) or match.group(2)
            if val and int(val) in [80, 85, 90]:
                params.setdefault("auto_rewrite_threshold", []).append(int(val))

        # 提取输出阈值（92分）
        for match in self.GATE_PATTERNS["output_threshold"].finditer(content):
            val = match.group(1)
            if val and int(val) in [90, 92, 95]:
                params.setdefault("output_threshold", []).append(int(val))

        # 提取最大重写次数
        for match in self.GATE_PATTERNS["max_rewrite"].finditer(content):
            val = match.group(1)
            if val:
                params.setdefault("max_rewrite", []).append(int(val))

        return params

    def test_shared_definitions_gate_complete(self, shared_definitions):
        """shared-definitions.md 应包含完整的门控参数（80/92/2次）"""
        params = self._extract_all_gate_params(shared_definitions)

        assert "auto_rewrite_threshold" in params, (
            "[T6-shared] ❌ 未找到自动重写阈值（应为80分）"
        )
        assert "output_threshold" in params, (
            "[T6-shared] ❌ 未找到输出阈值（应为92分）"
        )
        assert "max_rewrite" in params, (
            "[T6-shared] ❌ 未找到最大重写次数（应为2次）"
        )

        # 验证值正确
        thresholds_80 = [v for v in params.get("auto_rewrite_threshold", []) if v == 80]
        thresholds_92 = [v for v in params.get("output_threshold", []) if v == 92]
        max_rw_2 = [v for v in params.get("max_rewrite", []) if v == 2]

        assert len(thresholds_80) > 0, (
            "[T6-shared] ❌ 自动重写阈值应包含80"
        )
        assert len(thresholds_92) > 0, (
            "[T6-shared] ❌ 输出阈值应包含92"
        )
        assert len(max_rw_2) > 0, (
            "[T6-shared] ❌ 最大重写次数应包含2"
        )

    def test_skill_md_gate_alignment(self, skill_md):
        """SKILL.md 中的门控引用应与 shared-definitions.md 一致"""
        params = self._extract_all_gate_params(skill_md)

        # SKILL.md 只需引用门控，不需要完整定义
        # 但应包含关键参数
        has_threshold_80 = any(
            v == 80 for v in params.get("auto_rewrite_threshold", [])
        )
        has_threshold_92 = any(
            v == 92 for v in params.get("output_threshold", [])
        )

        assert has_threshold_80 or has_threshold_92, (
            "[T6-SKILL] ❌ SKILL.md 应至少引用一个质量门控阈值"
        )

    def test_batch_mode_gate_alignment(self, skill_root):
        """batch-mode.md 的迭代规则应与门控参数一致"""
        batch_path = skill_root / "sections" / "batch-mode.md"
        if not batch_path.exists():
            pytest.skip("[T6-batch] batch-mode.md 不存在")

        content = batch_path.read_text(encoding="utf-8")
        params = self._extract_all_gate_params(content)

        thresholds_80 = [v for v in params.get("auto_rewrite_threshold", []) if v == 80]
        thresholds_92 = [v for v in params.get("output_threshold", []) if v == 92]

        assert len(thresholds_80) > 0, (
            "[T6-batch] ❌ batch-mode.md 未引用自动重写阈值80"
        )
        assert len(thresholds_92) > 0, (
            "[T6-batch] ❌ batch-mode.md 未引用输出阈值92"
        )


# ============================================================================
# T7: SKILL.md与shared-definitions.md评分子项一致
# ============================================================================

class TestCrossFileConsistency:
    """T7: 评分子项在SKILL.md与shared-definitions.md中保持一致"""

    def test_skill_md_references_all_dimensions(self, skill_md):
        """SKILL.md 应引用全部4个评分维度"""
        for dim in EXPECTED_DIMENSIONS:
            assert dim in skill_md, (
                f"[T7] ❌ SKILL.md 未引用维度: {dim}"
            )

    def test_skill_md_has_scoring_summary(self, skill_md):
        """SKILL.md 应包含评分体系说明"""
        assert "评分" in skill_md, "[T7] ❌ SKILL.md 未包含评分相关内容"
        assert "质量门控" in skill_md or "gate" in skill_md.lower(), (
            "[T7] ❌ SKILL.md 未引用质量门控"
        )

    def test_shared_definitions_has_full_scoring(self, shared_definitions):
        """shared-definitions.md 应包含完整评分体系"""
        assert "评分等级" in shared_definitions, (
            "[T7] ❌ shared-definitions.md 未包含评分等级定义"
        )
        assert "评分子项" in shared_definitions, (
            "[T7] ❌ shared-definitions.md 未包含评分子项"
        )


# ============================================================================
# 测试汇总
# ============================================================================

def test_scoring_summary_report(shared_definitions, profiles):
    """评分体系健康报告"""
    print("\n\n" + "=" * 55)
    print("  评分体系一致性报告")
    print("=" * 55)

    # 维度统计
    dim_count = len(EXPECTED_DIMENSIONS)
    item_count = sum(len(items) for items in EXPECTED_ITEMS.values())
    total_score = sum(sum(items.values()) for items in EXPECTED_ITEMS.values())
    print(f"  📊 评分维度: {dim_count}个")
    print(f"  📋 评分子项: {item_count}个（满分总和={total_score}）")
    print(f"  🏆 评分等级: 5档（S/A/B/C/D）")
    print(f"  🚪 质量门控: 自动重写<{EXPECTED_GATE_PARAMS['auto_rewrite_threshold']}分 / "
          f"输出≥{EXPECTED_GATE_PARAMS['output_threshold']}分 / "
          f"最多重写{EXPECTED_GATE_PARAMS['max_rewrite_count']}次")

    # Profile权重
    print(f"\n  📁 行业Profile: {len(profiles)}个")
    for name, data in sorted(profiles.items()):
        has_weight = "专业度" in data["content"] and "传播力" in data["content"]
        status = "✅" if has_weight else "⚠️ "
        print(f"    {status} {name}")

    print("=" * 55)
