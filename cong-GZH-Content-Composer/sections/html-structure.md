---
name: HTML结构+输出格式验证
version: v8.5.0
description: >
  S6：HTML结构+输出格式验证
  公众号内容智能生成器 Section文件
---

# HTML结构详细定义

> **章节代码**：S6
> **适用场景**：生成排版，输出公众号兼容HTML
> **Token消耗**：~5,500字（仅加载此文件）
> **v8.5.0更新**：组件从10个扩展到18个，新增step-header/priority-card/warning-card/cta-card/case-card/checklist-card/comparison-card/summary-card；表格新增斑马纹+圆角规范

---

## 核心架构

**强制规则**：所有内容必须使用 `<section>` 标签作为块级容器。

**为什么使用`<section>`**：
- 公众号编辑器对`<div>`支持不完善
- `<section>`标签兼容性更好
- 内联样式在`<section>`中更稳定

---

## HTML结构模板

### 完整文章结构

```html
<!-- 文章标题 -->
<section style="padding: 20px; background: {极浅背景}; border-radius: 8px;">
  <section style="font-size: 20px; font-weight: bold; text-align: center; margin-bottom: 15px; color: {主题色};">
    {文章标题}
  </section>
</section>

<!-- 小标题 -->
<section style="margin: 20px 0 10px 0; padding-left: 10px; border-left: 3px solid {主题色};">
  <section style="font-size: 16px; font-weight: bold; color: {主题色};">
    {小标题}
  </section>
</section>

<!-- 正文段落 -->
<section style="margin-bottom: 15px; font-size: 15px; line-height: 2; color: #3f3f3f;">
  {正文段落}
</section>

<!-- 数字高亮卡片 -->
<section style="margin: 15px 0; padding: 15px; background: {极浅背景}; border-radius: 8px;">
  <section style="font-size: 18px; font-weight: bold; color: {主题色}; text-align: center;">
    {数字}
  </section>
  <section style="font-size: 14px; color: #666; text-align: center;">
    {说明文字}
  </section>
</section>

<!-- 引用/金句卡片 -->
<section style="margin: 15px 0; padding: 15px; border-left: 5px solid {主题色}; font-style: italic; color: #666;">
  <section>
    "{引用内容}"
  </section>
</section>

<!-- 列表 -->
<section style="margin: 15px 0; padding-left: 20px;">
  <section style="margin-bottom: 8px; font-size: 15px; line-height: 1.8;">
    • {列表项1}
  </section>
  <section style="margin-bottom: 8px; font-size: 15px; line-height: 1.8;">
    • {列表项2}
  </section>
</section>

<!-- 对比表格（斑马纹+圆角） -->
<section style="margin: 28px 0;">
  <table style="width: 100%; border-collapse: separate; border-spacing: 0; border-radius: 8px; overflow: hidden; font-size: 14px; border: 1px solid #e0e0e0;">
    <tr style="background: {主题色}; color: white;">
      <th style="padding: 12px 15px; text-align: left; font-weight: bold;">{表头1}</th>
      <th style="padding: 12px 15px; text-align: left; font-weight: bold;">{表头2}</th>
      <th style="padding: 12px 15px; text-align: left; font-weight: bold;">{表头3}</th>
    </tr>
    <tr style="background: #fff;">
      <td style="padding: 12px 15px; border-bottom: 1px solid #eee;">{单元格1}</td>
      <td style="padding: 12px 15px; border-bottom: 1px solid #eee;">{单元格2}</td>
      <td style="padding: 12px 15px; border-bottom: 1px solid #eee;">{单元格3}</td>
    </tr>
    <tr style="background: {极浅背景};">
      <td style="padding: 12px 15px; border-bottom: 1px solid #eee;">{单元格4}</td>
      <td style="padding: 12px 15px; border-bottom: 1px solid #eee;">{单元格5}</td>
      <td style="padding: 12px 15px; border-bottom: 1px solid #eee;">{单元格6}</td>
    </tr>
  </table>
</section>

<!-- 图片占位 -->
<section style="margin: 28px 0; text-align: center;">
  <section style="display: inline-block; padding: 20px; background: #f5f5f5; border-radius: 8px; color: #999;">
    [图片：{图片描述}，建议比例{宽}:{高}]
  </section>
</section>

<!-- 结尾引导区 -->
<section style="margin: 20px 0; padding: 20px; background: {极浅背景}; border-radius: 8px; text-align: center;">
  <section style="font-size: 15px; color: #666; margin-bottom: 10px;">
    {引导文字}
  </section>
  <section style="font-size: 14px; color: {主题色};">
    {关注引导/互动提问}
  </section>
</section>

<!-- ===== v8.5.0 新增组件（8个）===== -->

<!-- 步骤标题（step-header）：带序号的大步骤标题 -->
<section style="margin: 38px 0 20px 0; padding: 12px 20px; background: {主题色}; border-radius: 8px 8px 0 0;">
  <section style="font-size: 16px; font-weight: bold; color: white;">
    步骤{n}：{步骤标题}
  </section>
</section>

<!-- 优先级卡片（priority-card）：重要信息强调 -->
<section style="margin: 28px 0; padding: 18px; background: {极浅背景}; border-left: 4px solid {主题色}; border-radius: 0 8px 8px 0;">
  <section style="font-size: 14px; color: {主题色}; font-weight: bold; margin-bottom: 8px;">⭐ {优先级标签}</section>
  <section style="font-size: 15px; color: #3f3f3f; line-height: 1.8;">
    {重要信息内容}
  </section>
</section>

<!-- 警告卡片（warning-card）：风险/注意事项 -->
<section style="margin: 28px 0; padding: 18px; background: #fdf6ec; border-left: 4px solid #e6a23c; border-radius: 0 8px 8px 0;">
  <section style="font-size: 14px; color: #e6a23c; font-weight: bold; margin-bottom: 8px;">⚠️ {警告标签}</section>
  <section style="font-size: 14px; color: #3f3f3f; line-height: 1.8;">
    {风险/注意内容}
  </section>
</section>

<!-- CTA三件套卡片（cta-card）：行动引导 -->
<section style="margin: 38px 0; padding: 25px; background: {主题色}; border-radius: 8px; text-align: center;">
  <section style="font-size: 18px; font-weight: bold; color: white; margin-bottom: 12px;">
    {行动主标题}
  </section>
  <section style="font-size: 14px; color: rgba(255,255,255,0.9); margin-bottom: 20px;">
    {行动说明}
  </section>
  <section style="display: inline-block; padding: 10px 30px; background: white; color: {主题色}; border-radius: 20px; font-weight: bold; font-size: 15px;">
    {按钮文字}
  </section>
  <section style="font-size: 12px; color: rgba(255,255,255,0.7); margin-top: 15px;">
    {行动补充说明（低门槛/限时等）}
  </section>
</section>

<!-- 案例卡片（case-card）：真实案例/故事 -->
<section style="margin: 28px 0; padding: 20px; background: #fafafa; border-radius: 8px; border: 1px solid #eee;">
  <section style="font-size: 13px; color: #999; margin-bottom: 10px;">📋 {案例标签：真实案例/失败教训/成功经验}</section>
  <section style="font-size: 15px; color: #3f3f3f; line-height: 2; font-style: italic;">
    "{案例内容}"
  </section>
  <section style="font-size: 13px; color: #666; margin-top: 10px; text-align: right;">
    —— {来源/人物}
  </section>
</section>

<!-- 清单卡片（checklist-card）：可勾选的步骤清单 -->
<section style="margin: 28px 0; padding: 20px; background: {极浅背景}; border-radius: 8px;">
  <section style="font-size: 16px; font-weight: bold; color: {主题色}; margin-bottom: 15px;">
    ✅ {清单标题}
  </section>
  <section style="margin-bottom: 10px; font-size: 15px; color: #3f3f3f; line-height: 1.8;">
    ☐ {清单项1}
  </section>
  <section style="margin-bottom: 10px; font-size: 15px; color: #3f3f3f; line-height: 1.8;">
    ☐ {清单项2}
  </section>
  <section style="margin-bottom: 10px; font-size: 15px; color: #3f3f3f; line-height: 1.8;">
    ☐ {清单项3}
  </section>
</section>

<!-- 对比卡片（comparison-card）：正反/优劣对比 -->
<section style="margin: 28px 0;">
  <section style="padding: 15px; background: #fef0f0; border-radius: 8px 8px 0 0; border: 1px solid #fde2e2;">
    <section style="font-size: 14px; font-weight: bold; color: #f56c6c; margin-bottom: 8px;">❌ {对比反面标签}</section>
    <section style="font-size: 14px; color: #3f3f3f; line-height: 1.8;">{反面描述}</section>
  </section>
  <section style="padding: 15px; background: #f0f9eb; border-radius: 0 0 8px 8px; border: 1px solid #e1f3d8; border-top: none;">
    <section style="font-size: 14px; font-weight: bold; color: #67c23a; margin-bottom: 8px;">✅ {对比正面标签}</section>
    <section style="font-size: 14px; color: #3f3f3f; line-height: 1.8;">{正面描述}</section>
  </section>
</section>

<!-- 总结卡片（summary-card）：章节/全文总结 -->
<section style="margin: 38px 0; padding: 20px; background: {极浅背景}; border-radius: 8px; border: 2px solid {主题色};">
  <section style="font-size: 16px; font-weight: bold; color: {主题色}; margin-bottom: 12px; text-align: center;">
    📝 {总结标题}
  </section>
  <section style="font-size: 15px; color: #3f3f3f; line-height: 2;">
    {总结内容}
  </section>
</section>
```

---

## 强制校验闭环

**校验流程**：

1. **AI完成自检**：生成HTML后，AI必须逐行扫描全文
2. **检查要点**：
   - 所有块级元素是否都用`<section>`包裹
   - 所有样式是否都是内联样式（无`<style>`标签）
   - 是否有未闭合的标签
   - 是否有敏感词漏检
   - 是否有图片占位符未替换
   - 是否有超过2行的段落（可读性检查）
   - 是否有中英文混排不规范（中英文间缺少空格）
3. **全部通过后才呈现给用户**
4. **存在问题时自动修正**（见下方自动修正机制）

### 自动修正机制

**检测到问题时，AI自动执行以下修正**：

| 检测项 | 自动修正规则 | 无法自动修正 |
|--------|-------------|------------|
| `<div>`标签 | 替换为`<section>` | 无 |
| `<style>`标签 | 转换为内联样式 | 复杂CSS（提示用户） |
| 未闭合标签 | 自动补全 | 嵌套错误（提示用户） |
| 图片占位符未替换 | 标记为⚠️提示 | 无 |
| 超长段落（>5行） | 在合适位置插入`<section>`分段 | 无 |
| 中英文间距 | 自动添加空格 | 无 |
| CSS语法错误 | 自动修正常见错误 | 复杂错误（提示用户） |
| 颜色格式不规范 | 统一为`#RRGGBB` | 无 |

### 输出格式验证报告（升级版）

**校验报告格式**：

> **📋 输出格式验证报告**
>
> | 检查项 | 状态 | 说明 |
> |--------|------|------|
> | `<section>`标签使用 | ✅ 通过 | 所有块级元素正确使用`<section>` |
> | 内联样式 | ✅ 通过 | 无`<style>`标签 |
> | 标签闭合 | ✅ 通过 | 所有标签正确闭合 |
> | 敏感词检查 | ✅ 通过 | 无敏感词 |
> | 图片占位符 | ⚠️ {N}处 | 请替换占位符（行号：{X},{Y}） |
> | 段落可读性 | ✅ 通过 | 无超长段落 |
> | 中英文间距 | ✅ 通过 | 中英文间距规范 |
> | CSS语法 | ✅ 通过 | 颜色格式统一 |
>
> **结论**：HTML结构{全部合规/存在N处警告}，{可直接使用/建议修正后再使用}。
>
> **自动修正记录**：
> - {修正项1}：{修正前} → {修正后}
> - {修正项2}：{修正前} → {修正后}

### Markdown格式验证

**输出Markdown时也进行格式验证**：

| 检查项 | 检查规则 |
|--------|---------|
| 标题层级 | `#` > `##` > `###`，不能跳级 |
| 列表格式 | 列表项以`- `或`1. `开头 |
| 表格格式 | 表格必须有表头分隔行（`---`） |
| 链接格式 | `[文字](URL)` 格式正确 |
| 代码块 | 行内代码用`` ` ``，代码块用``` ``` ``` |
| 空行规范 | 标题前后必须有空行 |

---

## 样式组件预览

**预览文件**：`examples/style-preview.html`

**组件清单（共18个，v8.5.0扩展）**：

**基础组件（10个）**：
1. `section-title`：文章标题
2. `section-subtitle`：小标题
3. `section-body`：正文段落
4. `section-data-card`：数字高亮卡片
5. `section-quote`：引用/金句卡片
6. `section-list`：列表
7. `section-separator`：分割线
8. `section-table`：对比表格（斑马纹+圆角）
9. `section-image`：图片
10. `section-closing`：结尾引导区

**扩展组件（v8.5.0新增8个）**：
11. `section-step-header`：步骤标题（带序号，主题色背景白字）
12. `section-priority-card`：优先级卡片（重要信息强调）
13. `section-warning-card`：警告卡片（风险/注意事项，琥珀色系）
14. `section-cta-card`：CTA三件套卡片（物理行动+社交行动+回访行动）
15. `section-case-card`：案例卡片（真实案例/故事容器）
16. `section-checklist-card`：清单卡片（可勾选步骤清单）
17. `section-comparison-card`：对比卡片（红绿正反对比）
18. `section-summary-card`：总结卡片（章节/全文总结）

---

## 常见问题与解决

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 公众号编辑器样式丢失 | 使用了`<div>`或`<style>`标签 | 改为`<section>`+内联样式 |
| 图片显示不正常 | 图片宽度超过屏幕 | 添加`max-width:100%` |
| 文字颜色太浅 | 使用了`#999`以下颜色 | 改为`#3f3f3f`（正文）或`#666`（说明） |
| 行高太小，文字拥挤 | `line-height`<1.5 | 设置为`line-height:2`（正文） |

---

## Token优化说明

- 本文件（html-structure.md）包含HTML结构的**完整详细定义**
- SKILL.md中只保留**摘要（300-500字）** + 本文件引用
- **Token节省**：从读取完整SKILL.md（~16,000字）到只读取本文件（~3,500字），**节省约80%**

---

*HTML结构详细定义 v8.5.0*
*最后更新：2026-05-14*
*优化说明：v8.5.0扩展组件10→18（新增step-header/priority/warning/cta/case/checklist/comparison/summary）；表格新增斑马纹+圆角规范；所有组件margin统一为留白梯度规范值*
