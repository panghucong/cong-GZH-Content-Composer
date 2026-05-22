# -*- coding: utf-8 -*-
"""
新行业自动化生成脚手架
自动生成新行业所需的全部骨架文件，确保版本号自动同步

生成文件：
  1. profiles/{industry}.md         — 行业Profile（含L2豁免规则）
  2. compliance/{industry}-terms.md  — L1行业合规词库
  3. templates/{industry}-guide.md  — 高质量内容模板

用法：
  python scripts/new_industry_generator.py <行业名>
  python scripts/new_industry_generator.py "新能源" --code "new-energy"
  python scripts/new_industry_generator.py --list           # 列出已有行业
  python scripts/new_industry_generator.py --template      # 查看生成模板

示例：
  python scripts/new_industry_generator.py "餐饮"
  python scripts/new_industry_generator.py "宠物" --code "pet"

公众号内容智能生成器 v8.4.1
"""
import re
import sys
from pathlib import Path
from datetime import datetime


# ============================================================================
# 配置
# ============================================================================

SKILL_ROOT = Path(__file__).parent.parent.resolve()
CURRENT_VERSION = "v8.4.1"
TODAY = datetime.now().strftime("%Y-%m-%d")

EXISTING_INDUSTRIES = {
    "insurance":  "保险",
    "healthcare": "医疗健康",
    "finance":    "金融理财",
    "education":  "教育培训",
    "tech":       "科技互联网",
    "real-estate":"房地产",
    "auto":       "汽车",
    "travel":     "旅游",
}


# ============================================================================
# 文件模板生成器
# ============================================================================

class IndustryGenerator:
    """新行业文件生成器"""

    def __init__(self, industry_name: str, industry_code: str = None):
        self.industry_name = industry_name
        self.industry_code = industry_code or self._normalize_code(industry_name)
        self.version = CURRENT_VERSION
        self.date = TODAY

    @staticmethod
    def _normalize_code(name: str) -> str:
        """将行业名转换为代码（如：新能源 → new-energy）"""
        # 简单转拼音/英文逻辑
        code_map = {
            "新能源": "new-energy", "宠物": "pet", "餐饮": "catering",
            "美妆": "beauty", "母婴": "maternal", "服装": "fashion",
            "家居": "home", "健身": "fitness", "法律": "legal",
            "咨询": "consulting",
        }
        if name in code_map:
            return code_map[name]
        # 通用：中文转拼音首字母或英文小写
        import re
        return re.sub(r"[^\u4e00-\u9fa5a-z0-9-]", "", name.lower())

    def _frontmatter(self, name: str, desc: str) -> str:
        return f"""---
name: {name}
version: {self.version}
description: {desc}
---

# {name}

> **版本**：{self.version}
> **生成时间**：{self.date}
> **行业代码**：{self.industry_code}
> **框架详细定义**：见 `../frameworks.md`
> **共享定义**：见 `../shared-definitions.md`

---

## 一、基本信息

| 字段 | 值 |
|------|-----|
| 行业代码 | {self.industry_code} |
| 目标用户 | 目标用户画像（待填写） |
| 默认色调 | 浅蓝（可根据行业调整） |
| 默认预设 | P2（干货科普） |
| 合规严格度 | 中（根据行业监管要求调整） |

---

## 二、写作框架映射

**完整框架定义**：见 `../frameworks.md`（F1-F10详细说明）

| 内容类型 | 首选框架ID | 备选框架ID | 框架参数 |
|----------|------------|------------|---------|
| 干货科普 | F1（决策路径） | F4/F8 | 决策节点3-5个 |
| 产品种草 | F2（FABE） | F5 | 证据需含数据或案例 |
| 情感共鸣 | F3（英雄之旅） | F9 | 角色=目标用户，转变=获得价值 |
| 活动通知 | F6（利益前置） | F10 | 利益点放在首段前2句 |
| 热点评论 | F4（正反辩证） | F7/F8 | 正反各≥2个论据 |

---

## 三、评分权重

**自适应评分规则**：见 `../shared-definitions.md` 第三章

| 维度 | 默认 | 干货科普 | 产品种草 | 情感共鸣 | 活动通知 |
|------|------|---------|---------|---------|---------|
| 专业度 | 30% | 35% | 25% | 20% | 20% |
| 传播力 | 25% | 20% | 30% | 35% | 35% |
| 用户适配 | 30% | 30% | 30% | 30% | 30% |
| SEO | 15% | 15% | 15% | 15% | 15% |

---

## 四、排版配色注入

**排版预设参数**：见 `../shared-definitions.md` 第七章
**色调参数**：见 `../shared-definitions.md` 第八章

| 场景 | 主题色 | 极浅背景 | 特殊调整 |
|------|--------|----------|---------|
| 默认 | #2c5aa0 | #f0f5ff | 无 |

---

## 五、写作风格人设

| 参数 | 值 |
|------|-----|
| 语气基调 | 专业可信+亲切（待调整） |
| 人称视角 | 第一人称朋友+第三人称专业混合 |
| 专业术语密度 | 中 |
| 情感浓度 | 中 |
| 说服策略 | 数据驱动+案例佐证 |
| 禁忌语气 | 夸大承诺式、恐吓式 |

---

## 六、钩子模板库（压缩版）

| 类型 | 模板 | 适用类型 |
|------|------|---------|
| 痛点 | "你有没有想过...?" | 干货科普、种草 |
| 数据 | "最新数据：X%的{人群}..." | 干货科普、评论 |
| 故事 | "上周一位{客户}找到我..." | 共鸣、种草 |

---

## 七、话术合规专区

| 场景 | 标准话术模板 | 风险 |
|------|------------|------|
| 效果承诺 | "效果因人而异，具体请咨询专业人士" | 中 |
| 价格描述 | "价格仅供参考，以实际为准" | 低 |

---

## 八、语境豁免规则（L2层）

**合规扫描流程**：见 `../shared-definitions.md` 第二章

| 豁免语境 | 可豁免词 | 豁免条件 | 必须附加提示语 |
|----------|---------|---------|--------------|
| 专业对比评测 | {待补充敏感词} | 需同时：①≥2款产品 ②客观数据 ③非绝对化表述 | "以上对比仅供参考，以实际情况为准" |
| 行业数据引用 | {待补充敏感词} | 需注明数据来源+统计周期 | "数据来源：XX机构XX年度统计" |
| 专家引用 | {待补充敏感词} | 需注明专家身份+来源 | "专家观点仅供参考" |

---

## 九、发布引导

| 项目 | 覆盖值 |
|------|-------|
| 默认标签 | #{industry_name}科普 #如何选择 #{行业关键词} |
| 封面图方向 | 清晰大字标题+{industry_name}相关场景图 |
| 摘要模板 | "{目标用户}必看！{核心利益点}→" |
| 发布时机 | 工作日 12:00-13:00 / 20:00-22:00（待行业验证） |

---

## 十、预设映射覆盖

| 内容类型 | 默认预设 | 色调覆盖 | 特殊调整 |
|----------|---------|---------|---------|
| 干货科普 | P2 | 浅蓝 | 无 |
| 产品种草 | P2 | 浅蓝 | 数字卡片加大 |
| 情感共鸣 | P3 | 米白 | 圆角加大 |
| 活动通知 | P4 | 橙色 | 无 |
| 热点评论 | P2 | 浅蓝 | 无 |

---

## 十一、合规词库引用

**L1行业层词库**：见 `../compliance/{self.industry_code}-terms.md`
**L0通用层词库**：见 `../compliance/universal.md`
"""

    def _compliance_template(self) -> str:
        return f"""---
name: {self.industry_name}L1合规词库
version: {self.version}
description: {self.industry_name}行业专属合规敏感词（L1层）
---

# {self.industry_name}行业L1合规词库（动态加载）

> **版本**：{self.version}
> **生成时间**：{self.date}
> **启用条件**：行业代码={self.industry_code}时启用
> **作用**：补充通用层（L0）未覆盖的{self.industry_name}行业专属敏感词
> **风险等级定义**：见 `../shared-definitions.md` 第一章
> **合规扫描流程**：见 `../shared-definitions.md` 第二章

---

## 一、高风险敏感词（强制替换）

| 敏感词/表述 | 问题说明 | 建议替换 |
|-----------|---------|---------|
| 【待补充】保证类承诺 | 绝对化表述 | "追求..." / "致力于..." |
| 【待补充】效果夸大 | 夸大产品/服务效果 | "有效改善..." / "大部分用户反馈..." |

---

## 二、中风险敏感词（提示修改）

| 敏感词/表述 | 问题说明 | 建议替换 |
|-----------|---------|---------|
| 【待补充】唯一/第一 | 广告法绝对化 | "领先" / "知名" / "优选" |

---

## 三、低风险敏感词（仅提示）

| 敏感词/表述 | 问题说明 | 建议替换 |
|-----------|---------|---------|
| 【待补充】 | 需加数据来源 | "根据XX数据显示..." |

---

## 四、行业专属风险提示

**待补充{self.industry_name}行业的特有风险场景**：

| 场景 | 风险描述 | 合规建议 |
|------|---------|---------|
| 待补充 | 待补充 | 待补充 |

---

## 五、使用说明

**合规扫描流程**：见 `../shared-definitions.md` 第二章

**风险等级处理**：
- 🔴 高风险：强制替换，AI自动替换
- 🟡 中风险：提示修改，用户可选择保留
- 🟢 低风险：仅提示，不强制修改

**文件加载顺序**：
1. 加载 `universal.md`（L0通用层）
2. 加载本文件（L1行业层）
3. 读取 `profiles/{self.industry_code}.md` 检查L2语境豁免规则

**⚠️ 使用前必做**：
1. 根据{self.industry_name}行业监管规定，补充各风险等级的敏感词（标记【待补充】处）
2. 根据行业实际情况，补充"行业专属风险提示"
3. 运行 `python tests/test_runner.py` 验证文件格式正确
"""

    def _template_template(self) -> str:
        return f"""---
name: {self.industry_name}行业内容模板
version: {self.version}
description: {self.industry_name}行业高质量内容模板（T-{self.industry_code.upper()[:4]}-001）
---

# {self.industry_name}行业内容模板

> **版本**：{self.version}
> **生成时间**：{self.date}
> **适用场景**：{self.industry_name}行业干货科普/产品种草
> **推荐框架**：F1决策路径 / F2 FABE / F3英雄之旅

---

## 模板一：干货科普型（F1决策路径）

### 适用场景
- 帮助用户了解{self.industry_name}基础知识
- 引导用户做决策

### 标题模板
`{self.industry_name}入门指南：X个你必须知道的关键点`

### 正文结构

**开头（痛点切入）**：
你是不是也遇到过...？（痛点场景描述，50字以内）

**主体（决策路径）**：

**第1点：基础概念**（200字以内）
{self.industry_name}是什么？有什么用？

**第2点：核心要点**（300字以内）
选择{self.industry_name}时，最重要的X个指标是什么？

**第3点：避坑提示**（200字以内）
很多人踩过的X个坑，看看你中了几个？

**结尾（行动引导）**：
如果你还有疑问，评论区告诉我，或者点击下方...

---

## 模板二：产品种草型（F2 FABE）

### 适用场景
推荐具体{self.industry_name}产品/服务

### 标题模板
`实测X个月，这款{self.industry_name}产品到底怎么样？`

### 正文结构

**F - Feature（特征）**：
这款产品的核心参数是...

**A - Advantage（优势）**：
相比其他产品，它的核心优势是...

**B - Benefit（利益）**：
用完之后，你将获得...（具体可感知的收益）

**E - Evidence（证据）**：
X位用户真实反馈，平均满意度X%

---

## 模板三：情感共鸣型（F3英雄之旅）

### 适用场景
讲述{self.industry_name}相关人物故事，引发情感共鸣

### 标题模板
`从月薪3000到{self.industry_name}达人，她经历了什么？`

### 正文结构

**起点**：普通人的困境（100字）
**挑战**：遇到的困难和阻碍（150字）
**转折**：关键决定/方法（200字）
**成长**：收获和改变（150字）
**行动**：鼓励读者行动（50字）

---

*模板版本：{self.version}*
*最后更新：{self.date}*
"""

    def generate_all(self, dry_run: bool = False):
        """生成所有新行业文件"""
        files = [
            (f"profiles/{self.industry_code}.md", self._frontmatter(), "Profile"),
            (f"compliance/{self.industry_code}-terms.md", self._compliance_template(), "合规词库"),
            (f"templates/{self.industry_code}-guide.md", self._template_template(), "内容模板"),
        ]

        created = []
        skipped = []

        for relative_path, content, desc in files:
            full_path = SKILL_ROOT / relative_path
            if full_path.exists():
                skipped.append((relative_path, desc, "文件已存在"))
                continue

            if dry_run:
                skipped.append((relative_path, desc, "预览模式"))
                print(f"\n📄 [预览] 将创建: {relative_path}")
                print(f"   大小: ~{len(content)}字符")
                continue

            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            created.append((relative_path, desc))

        return created, skipped


# ============================================================================
# 主函数
# ============================================================================

def print_header():
    print(f"\n{'=' * 55}")
    print(f"  新行业自动化生成工具 v{CURRENT_VERSION}")
    print("=" * 55)


def print_usage():
    print("""
用法：
  python scripts/new_industry_generator.py <行业名> [--code <行业代码>]
  python scripts/new_industry_generator.py --list          # 列出已有行业
  python scripts/new_industry_generator.py --template     # 查看Profile模板

示例：
  python scripts/new_industry_generator.py "新能源" --code "new-energy"
  python scripts/new_industry_generator.py "宠物" --code "pet"
  python scripts/new_industry_generator.py "餐饮"
""")


def main():
    print_header()

    if len(sys.argv) < 2:
        print("❌ 请提供行业名称")
        print_usage()
        sys.exit(1)

    if "--list" in sys.argv:
        print("已有行业：")
        for code, name in sorted(EXISTING_INDUSTRIES.items()):
            path = SKILL_ROOT / "profiles" / f"{code}.md"
            status = "✅" if path.exists() else "❌"
            print(f"  {status} [{code}] {name}")
        return

    if "--template" in sys.argv:
        gen = IndustryGenerator("示例行业", "example")
        print(gen._frontmatter("示例行业", "示例描述"))
        return

    # 获取行业名
    industry_name = sys.argv[1]
    industry_code = None

    if "--code" in sys.argv:
        code_idx = sys.argv.index("--code")
        if code_idx + 1 < len(sys.argv):
            industry_code = sys.argv[code_idx + 1]

    dry_run = "--dry-run" in sys.argv or "--preview" in sys.argv

    print(f"\n📌 行业名称: {industry_name}")
    print(f"📌 行业代码: {industry_code or '自动推断'}")
    print(f"📌 版本号:   {CURRENT_VERSION}")

    # 检查是否已存在
    if industry_code and (SKILL_ROOT / f"profiles/{industry_code}.md").exists():
        print(f"\n⚠️  行业代码 '{industry_code}' 的Profile已存在！")
        print("   如需重新生成，请先删除现有文件。")
        sys.exit(1)

    gen = IndustryGenerator(industry_name, industry_code)
    created, skipped = gen.generate_all(dry_run=dry_run)

    print(f"\n{'=' * 55}")
    print("  生成结果")
    print("=" * 55)

    if dry_run:
        if skipped:
            for path, desc, reason in skipped:
                print(f"  ⏭️  跳过: {path}（{reason}）")
        print("\n  💡 以上为预览模式，使用不带 --dry-run 参数执行实际生成")
    else:
        if created:
            print(f"  ✅ 成功创建 {len(created)} 个文件：")
            for path, desc in created:
                print(f"    ✅ {desc}: {path}")
        if skipped:
            for path, desc, reason in skipped:
                print(f"    ⏭️  跳过: {path}（{reason}）")

        if created:
            print(f"\n  📋 下一步：")
            print(f"    1. 编辑 compliance/{gen.industry_code}-terms.md 补充敏感词")
            print(f"    2. 编辑 profiles/{gen.industry_code}.md 完善行业信息")
            print(f"    3. 运行 python tests/test_runner.py 验证格式")
            print(f"    4. 运行 python scripts/version_checker.py 检查版本")


if __name__ == "__main__":
    main()
