---
name: 排版预设详细参数
version: v8.5.0
description: >
  S5：排版预设详细参数
  公众号内容智能生成器 Section文件
---

# 排版预设详细参数

> **章节代码**：S5
> **适用场景**：排版环节，生成公众号兼容HTML
> **Token消耗**：~4,500字（仅加载此文件）
> **v8.5.0更新**：3色系统（信息蓝+警告琥珀+灰色层级）、留白梯度规范

---

## 三色系统（v8.5.0新增）

**核心升级**：从 `{主题色}+{极浅背景}` 2色系统升级为3色系统，新增 `{警告色}` 用于风险提示、注意事项、对比负面项。

| 颜色变量 | 色值 | 用途 | 使用场景 |
|---------|------|------|---------|
| `{主题色}` | 随色调方案（默认 #2c5aa0） | 信息/正面/强调 | 标题、小标题边框、数字高亮、链接、CTA按钮 |
| `{警告色}` | #e6a23c（琥珀色，固定） | 警告/风险/注意 | 风险提示卡片、注意事项、对比表格中的劣势项、避坑提醒 |
| `{正文色}` | #3f3f3f（深灰，固定） | 主要文本 | 段落正文、表格内容 |
| `{说明色}` | #666（中灰，固定） | 辅助说明 | 注释、脚注、次要信息 |
| `{极浅背景}` | 随色调方案（默认 #e8f1f8） | 卡片底色 | 数据卡片、引用块背景 |
| `{警告浅背景}` | #fdf6ec（浅琥珀，固定） | 警告卡片底色 | 风险提示、避坑提醒、注意事项背景 |

**3色系统使用原则**：
1. **{主题色}** 占主导（60-70%），承载信息传递和正面引导
2. **{警告色}** 用于强调（15-20%），制造视觉锚点，引导关注风险/注意事项
3. **灰阶文字** 构成层级（15-25%），通过 #3f3f3f / #666 / #999 三档建立阅读节奏

**警告色使用场景示例**：
```html
<!-- 风险提示卡片 -->
<section style="padding: 15px; background: #fdf6ec; border-left: 4px solid #e6a23c; border-radius: 8px;">
  <section style="font-size: 14px; color: #e6a23c; font-weight: bold; margin-bottom: 8px;">⚠️ 注意</section>
  <section style="font-size: 14px; color: #3f3f3f; line-height: 1.8;">此处填写风险提示内容</section>
</section>
```

---

## 留白梯度规范（v8.5.0新增）

**核心原则**：通过3级留白建立阅读节奏感，避免信息过密或过度空旷。

| 留白层级 | 间距 | 使用场景 | 说明 |
|---------|------|---------|------|
| 模块间距 | 26-32px（推荐28px） | 同一章节内组件之间 | 数据卡片、列表、引用块之间的margin-bottom |
| 章节分隔 | 36-40px（推荐38px） | 不同章节/模块之间 | 大标题之间、主题切换处的margin-top |
| 分割线 | 12px margin | 分割线两侧 | section-separator 的 margin: 12px 0 |

**留白使用规范**：
1. **正文段落**：margin-bottom: 15px（约1行高度）
2. **小标题前后**：margin-top: 28px, margin-bottom: 12px
3. **卡片组件**：padding: 15-20px, margin-bottom: 28px
4. **章节大标题**：margin-top: 38px, margin-bottom: 20px
5. **全文首尾**：首段无margin-top，尾段后留20px
6. **分割线**：margin: 12px 0

---

## 排版矩阵化（G10）

排版选择是**风格×色调×行业**三维矩阵：

| 维度 | 选项 | 来源 |
|------|------|------|
| 风格 | 简约清新/活泼吸睛/专业严谨/温馨治愈 | 用户选择 or 行业Profile |
| 色调 | 10种色调（见下文） | 用户选择 or 行业Profile |
| 行业调参 | 行业专属样式调整 | 行业Profile |

---

## 色调参数表

| 色调代码 | 色调名称 | 主题色 | 极浅背景 | 适用行业 |
|---------|---------|--------|----------|---------|
| T1 | 浅蓝 | #2c5aa0 | #e8f1f8 | 保险/教育/科技 |
| T2 | 米白 | #8b7355 | #faf8f5 | 通用/情感/品牌 |
| T3 | 浅粉 | #c45c7a | #fce4ec | 美妆/母婴/情感 |
| T4 | 浅灰 | #4a4a4a | #f5f5f5 | 科技/职场/金融 |
| T5 | 浅绿 | #2d8a5e | #e8f5e9 | 医疗/健康/生活 |
| T6 | 深蓝 | #1a3a5c | #e3f2fd | 金融/科技/企业 |
| T7 | 橙色 | #d4762c | #fff3e0 | 活动/促销/美食 |
| T8 | 亮粉 | #e91e63 | #fce4ec | 美妆/时尚/母婴 |
| T9 | 亮橙 | #ff9800 | #fff3e0 | 活动/促销/餐饮 |
| T10 | 明黄 | #ffc107 | #fffde7 | 教育/亲子/生活 |

---

## 排版预设参数定义

### P1：保险种草

**适用场景**：保险产品推荐、方案对比

**参数设置**：

| 参数 | 值 |
|------|-----|
| 整体风格 | 专业严谨 |
| 主色调 | T1（浅蓝） |
| 警告色 | #e6a23c（固定） |
| 标题字号 | 20px，加粗 |
| 正文字号 | 15px，行高2 |
| 小标题样式 | 左边框3px solid 主题色 |
| 卡片背景 | 极浅背景色 |
| 警告卡片背景 | #fdf6ec（浅琥珀） |
| 数字高亮 | 主题色，加粗，18px |
| 引用样式 | 左边框5px solid 主题色，斜体 |
| 模块间距 | 28px |
| 章节分隔 | 38px |

**HTML结构示例**（3色系统）：

```html
<!-- 标题区 -->
<section style="padding: 20px; background: #e8f1f8; border-radius: 8px;">
  <section style="font-size: 20px; font-weight: bold; text-align: center; margin-bottom: 15px;">
    {标题}
  </section>
</section>

<!-- 正文段落（28px模块间距） -->
<section style="margin-bottom: 28px; font-size: 15px; line-height: 2; color: #3f3f3f;">
  {正文}
</section>

<!-- 风险提示卡片（警告色系） -->
<section style="margin-bottom: 28px; padding: 15px; background: #fdf6ec; border-left: 4px solid #e6a23c; border-radius: 8px;">
  <section style="font-size: 14px; color: #e6a23c; font-weight: bold; margin-bottom: 8px;">⚠️ 注意事项</section>
  <section style="font-size: 14px; color: #3f3f3f; line-height: 1.8;">
    {风险/注意内容}
  </section>
</section>
```

### P2：干货科普

**适用场景**：知识分享、教程攻略

**参数设置**：

| 参数 | 值 |
|------|-----|
| 整体风格 | 简约清新 |
| 主色调 | T1（浅蓝）或T5（浅绿） |
| 警告色 | #e6a23c（固定） |
| 标题字号 | 18px，加粗 |
| 正文字号 | 15px，行高1.8 |
| 小标题样式 | 数字编号+主题色 |
| 卡片背景 | 极浅背景色 |
| 警告卡片背景 | #fdf6ec（浅琥珀） |
| 代码块样式 | 深色背景+白色文字 |
| 列表样式 | 主题色圆点 |
| 模块间距 | 28px |
| 章节分隔 | 38px |

### P3：品牌宣传

**适用场景**：企业新闻、品牌故事

**参数设置**：

| 参数 | 值 |
|------|-----|
| 整体风格 | 专业严谨 |
| 主色调 | T2（米白）或T6（深蓝） |
| 警告色 | #e6a23c（固定） |
| 标题字号 | 22px，加粗 |
| 正文字号 | 16px，行高1.8 |
| 小标题样式 | 居中+底线 |
| 卡片背景 | 白色卡片+阴影 |
| 警告卡片背景 | #fdf6ec（浅琥珀） |
| 引用样式 | 大字号引用+主题色 |
| 模块间距 | 28px |
| 章节分隔 | 38px |

### P4：活动促销

**适用场景**：优惠活动、限时福利

**参数设置**：

| 参数 | 值 |
|------|-----|
| 整体风格 | 活泼吸睛 |
| 主色调 | T7（橙色）或T9（亮橙） |
| 警告色 | #e6a23c（固定） |
| 标题字号 | 24px，加粗，红色 |
| 正文字号 | 16px，行高1.6 |
| 小标题样式 | 爆炸边框/高亮背景 |
| 卡片背景 | 渐变背景 |
| 警告卡片背景 | #fdf6ec（浅琥珀） |
| 按钮样式 | 圆角按钮，主题色背景 |
| 模块间距 | 26px |
| 章节分隔 | 36px |

### P5：自定义

**适用场景**：不限，完全自定义

**参数设置**：用户自定义所有参数

---

## 语义化组件标签体系

| 组件名 | HTML结构 | 样式要点 |
|--------|----------|----------|
| `section-title` | 外层section(居中) > 内层section(标题文字) | font-size:20px, font-weight:bold |
| `section-subtitle` | 外层section > 内层section(小标题文字) | border-left:3px solid {主题色} |
| `section-body` | 外层section > 内层section(正文) | font-size:15px, line-height:2 |
| `section-data-card` | section(卡片容器) > 内层section×2 | background:{极浅背景} |
| `section-quote` | section(引用容器) > 内层section(引用文字) | border-left:5px solid {主题色}, font-style:italic |
| `section-list` | section(列表容器) > section(列表项)×N | list-style: disc inside |
| `section-separator` | section(分割线) | border-top:1px solid #eee, margin:20px 0 |
| `section-table` | section(表格容器) > table | border:1px solid #ddd, width:100% |
| `section-image` | section(图片容器) > img | max-width:100%, height:auto |
| `section-closing` | section(结尾容器) > 内层section(引导文字) | text-align:center, color:{说明色} |

---

## 行业×预设×色调快速映射表

| 行业 | 干货科普 | 产品种草 | 情感共鸣 | 活动通知 | 热点评论 |
|------|---------|----------|---------|---------|----------|
| 保险 | P2/T1 | P1/T1 | P3/T3 | P4/T7 | P2/T1 |
| 医疗 | P2/T5 | P2/T5 | P3/T3 | P4/T7 | P2/T5 |
| 金融 | P2/T1 | P2/T1 | P3/T2 | P4/T7 | P2/T1 |
| 教育 | P2/T1 | P2/T1 | P3/T2 | P4/T7 | P2/T1 |
| 科技 | P2/T4 | P2/T4 | P3/T2 | P4/T7 | P2/T4 |
| 通用 | P2/T1 | P2/T1 | P3/T2 | P4/T7 | P2/T1 |

---

## Token优化说明

- 本文件（layout-presets.md）包含排版预设的**完整详细参数**
- SKILL.md中只保留**摘要（300-500字）** + 本文件引用
- **Token节省**：从读取完整SKILL.md（~16,000字）到只读取本文件（~4,000字），**节省约75%**

---

*排版预设详细参数 v8.5.0*
*最后更新：2026-05-14*
*优化说明：v8.5.0新增3色系统（信息蓝+警告琥珀+灰色层级）、留白梯度规范（模块28px/章节38px/分割12px）、所有预设参数同步更新*
