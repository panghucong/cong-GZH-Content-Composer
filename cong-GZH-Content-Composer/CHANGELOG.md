# CHANGELOG

> 公众号内容智能生成器 版本变更记录

---

## v8.5.0 (2026-05-21) — 工程质量修复版

### 🔴 P0 修复（阻塞项）
- `shared-definitions.md`: 正文标题版本号 v8.4.1 → v8.5.0，与 frontmatter 对齐
- `SKILL.md`: 正文标题 v8.5 → v8.5.0（补全 .0）
- `sections/quick-mode.md`: 质量门控逻辑改为引用 shared-definitions.md 第十章，消除"最多3次" vs "最多2次"冲突
- `profiles/insurance.md`: 评分权重增加第5维度"视觉排版"（28/24/25/13/10），新增2个保险专属视觉评分子项

### 🟡 P1 修复（质量项）
- `scripts/version_checker.py`: MAIN_VERSION → v8.5.0；新增 V8 检查项（正文标题 vs frontmatter 版本一致性）；移除重复 get_version() 函数
- `compliance/real-estate-terms.md`: **新增** 房地产行业L1合规词库（4类29条）
- `compliance/auto-terms.md`: **新增** 汽车行业L1合规词库（4类20条）
- `compliance/travel-terms.md`: **新增** 旅游行业L1合规词库（4类22条）

### 📁 全文件版本同步
- 12 个 section 文件：v8.4.0 → v8.5.0（S1-S4,S7-S11）
- 8 个 profile 文件：v8.0.0 或 v8.4.0 → v8.5.0
- 6 个 compliance 文件：v8.0.0 或 v8.4.0 → v8.5.0
- `frameworks.md`: v8.4.0 → v8.5.0

---

## v8.5.0 (2026-05-14) — 第四代增强版

### 新增功能
- 3色系统：主题色 + 警告色（#e6a23c）+ 灰色层级
- HTML组件从10个扩展到18个：新增步骤标题/优先级卡片/警告卡片/CTA卡片/案例卡片/清单卡片/对比卡片/总结卡片
- 留白梯度规范：模块28px/章节38px/分割12px 三级留白
- 视觉排版评分维度：评分体系从4维升级为5维（+视觉排版）
- Pain→Relief叙事规则：负面案例先于正面案例，CTA三件套
- `examples/style-preview.html`：重构为 section-only + inline-style 架构
- 结构化迭代检查清单：改写模式从自由判断改为10项逐项检查
- SKILL.md 主文件新增18项增强汇总表

### 文件变更
- `SKILL.md`
- `shared-definitions.md`（新增视觉排版评分子项、质量门控规则定义）
- `sections/layout-presets.md`（新增3色系统、留白梯度规范）
- `sections/html-structure.md`（组件10→18扩展）
- `sections/emotional-resonance.md`（新增 Pain→Relief 规则）
- `sections/rewrite-mode.md`（新增结构化迭代检查清单）
- `examples/style-preview.html`（重构为 section-only 架构）

---

## v8.4.1 (2026-05-11)

### 修复与增强
- 质量门控规则正式定义（shared-definitions.md 第十章）：初稿<80分自动重写，最多2次，目标92分
- 评分体系统一为5档（S/A/B/C/D）
- 新增测试套件（test_runner.py + 3个测试文件）
- 新增工程化工具脚本（version_checker.py / l2_context_generator.py / new_industry_generator.py）

### 文件变更
- `shared-definitions.md`
- `tests/test_runner.py`、`tests/test_section_loading.py`、`tests/test_compliance_scanner.py`、`tests/test_scoring_consistency.py`
- `scripts/version_checker.py`、`scripts/l2_context_generator.py`、`scripts/new_industry_generator.py`

---

## v8.4.0 (2026-05-10) — 第四代优化版

### 核心架构
- 分章节加载架构：SKILL.md 作为目录级入口，12个独立 section 文件按需加载
- 共享定义库：shared-definitions.md 统一所有重复定义
- 数字编码系统：F/P/T/I/C/S/L/R/E/U/W 编码压缩 token 约18%

### 新增功能
- 7种入口模式（快速/标准/仅排版/改写/批量/切换行业/快捷模式）
- 5种排版预设（P1-P5）+ 10种色调
- 8个行业 Profile + 5个行业合规词库 + 10个高质量模板
- 3个写作视角（专业/用户/传播）
- 10个写作框架（F1-F10）

### 文件变更
- `SKILL.md`、`shared-definitions.md`、`frameworks.md`
- `sections/` 下 12 个文件
- `profiles/` 下 8 个文件
- `compliance/` 下 6 个文件
- `templates/` 下 10 个文件
- `examples/style-preview.html`

---

*CHANGELOG.md v8.5.0*
*创建者：阿聪*
*最后更新：2026-05-21*
