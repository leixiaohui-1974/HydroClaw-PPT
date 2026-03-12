Loaded cached credentials.
基于您提供的团队PPT风格数据，我为您整理了一份结构化的PPT设计规范文档。为了满足“方便程序读取”的需求，文档采用了高度模块化的标准结构，并在文末提供了一份对应的 `JSON` 格式配置字典，可直接作为程序的配置输入。

---

# 团队 PPT 自动化生成设计规范

## 1. 字体搭配方案 (Font Pairing Scheme)

根据高频字体数据（微软雅黑占绝对主导，Geist/Arial/TNR紧随其后），推荐以下中英文搭配组合：

*   **方案 A（现代科技风 - 推荐用于HydroClaw产品发布/展示）**
    *   **中文**: 微软雅黑 (Microsoft YaHei) / PingFang SC
    *   **英文**: Geist / Geist Bold
    *   **适用场景**: 强调AI、认知智能、操作系统等前沿科技概念。
*   **方案 B（严谨学术风 - 推荐用于三引擎评审/项目报告）**
    *   **中文**: 微软雅黑 (Microsoft YaHei)
    *   **英文**: Times New Roman / Arial
    *   **适用场景**: 侧重控制论、模型公式、学术研究内容的汇报。
*   **方案 C（通用商务风 - 推荐用于常规汇报）**
    *   **中文**: 微软雅黑 (Microsoft YaHei)
    *   **英文**: Calibri / Trebuchet MS
    *   **适用场景**: 内部沟通、团队汇报。

**字号规范 (基于使用频率统计)：**
*   **主标题**: 40pt - 44pt
*   **副标题/章节标题**: 28pt - 32pt
*   **正文一级**: 20pt - 24pt
*   **正文二级**: 16pt - 18pt
*   **图表辅助文本/注释**: 12pt - 14pt

---

## 2. 版式设计规范 (Layout Specifications)

基于高频尺寸（13.33x7.5英寸，即16:9宽屏）和版式类型数据，推荐5种标准版式及其布局参数（坐标系以左上角为 `[0,0]`，宽度100%，高度100%计算）：

1.  **混合内容版式 (Mixed Content - 占比56.7%)**
    *   **用途**: 左字右图/图表，或上字下两图。
    *   **参数**: 标题 `[5%, 5%, 90%, 15%]`；左侧文本区 `[5%, 20%, 42.5%, 70%]`；右侧图表区 `[52.5%, 20%, 42.5%, 70%]`。
2.  **多文本版式 (Text Heavy - 占比29.9%)**
    *   **用途**: 原理阐述、科学问题与研究内容列举（平均元素达15.3个，说明文本块较多）。
    *   **参数**: 标题 `[5%, 5%, 90%, 15%]`；主文本区 `[5%, 20%, 90%, 75%]`（建议开启多列或使用多个段落块）。
3.  **标准列表版式 (Standard - 占比10.9%)**
    *   **用途**: 核心结论、并列要点提取（如“四层单向依赖”）。
    *   **参数**: 标题 `[5%, 5%, 90%, 15%]`；单列居中列表区 `[15%, 25%, 70%, 65%]`。
4.  **过渡/标题版式 (Title Only - 占比2.3%)**
    *   **用途**: 章节切换、抛出核心叩问（如“这意味着什么？”）。
    *   **参数**: 主标题居中 `[10%, 40%, 80%, 20%]`，文本对齐设为 `center`。
5.  **全图/大图展示版式 (Image Gallery - 占比较小但重要)**
    *   **用途**: 总体架构图、数字孪生场景展示。
    *   **参数**: 图像区域满版或居中大画幅 `[5%, 5%, 90%, 90%]`，如果包含说明文本，可置于底部浮层 `[10%, 85%, 80%, 10%]`。

---

## 3. 文字表述风格总结 (Text Expression Style)

*   **措辞风格 (Tone & Voice)**:
    *   **宏大叙事与断言**: 喜欢使用绝对、前沿的词汇（如“时刻已经到来”、“根本性差异”、“不可跳过”、“认知跃迁”）。
    *   **结构化/对比化**: 大量使用“XX vs XX”（如“通用Agent vs 水网垂直Agent”），强调传统与创新的对比。
    *   **符号化强调**: 频繁使用特殊符号打头和编号（如 `✔`、`>>` (100次)、`01`、`02`、`⭐⭐⭐⭐⭐`）来增强视觉引导和逻辑层级。
*   **专业术语特点 (Terminology)**:
    *   **高度复合/跨学科**: 深度融合水利专业与AI术语（如 `HydroClaw`, `HydroMAS`, `HydroOS`, `xIL`, `ODD运行设计域`, `S2`, `L1/L2`）。
    *   **系统工程化**: 强调层次和架构（“认知决策层”、“技能编排层”、“计算引擎层”、“四层单向依赖”）。
*   **标题范式**: 建议程序在生成时遵守以下三种标题构造正则/模式：
    1.  `[编号] [核心观点/概念]` (例：`01 控制跃迁：SIM→HDC`)
    2.  `[概念/实体]：[定义/动作]` (例：`HydroClaw：在xIL保护下的第五代认知智能层`)
    3.  `[核心结论前置]` (例：`水网领域不需要“会说水利话的ChatGPT”，而是一个完整的水网领域操作系统`)

---

## 4. 整体设计规范建议 (Overall Design Specifications)

1.  **高密度信息的秩序感 (Spacing & Density)**: 由于平均每页高达15.3个元素，且多为 `mixed_content`，**必须**依赖严格的网格系统。建议设置水平与垂直间距（Gutter/Margin）不小于页面的 `5%`，避免内容拥挤。
2.  **对齐规范 (Alignment)**:
    *   标题统一**左对齐**。
    *   长段落正文采用**两端对齐 (Justify)**，短要点采用**左对齐**。
    *   逻辑推进类的图文（如跨越三个时代）使用**水平或垂直居中对齐**。
3.  **留白原则 (Whitespace)**:
    *   对于抛出观点的页面（如“这意味着什么？”），留白率需达到 `70%` 以上。
    *   对于架构图/复杂图表页，四周留白（Margin）保持在 `5%` 即可，最大化图表展示面积。

---

## 附：程序读取用 JSON 配置字典 (Program-Readable Configuration)

```json
{
  "presentation_config": {
    "page_size": {
      "ratio": "16:9",
      "width_inches": 13.33,
      "height_inches": 7.5
    },
    "typography": {
      "fonts": {
        "title": ["Microsoft YaHei", "PingFang SC"],
        "body_cn": ["Microsoft YaHei"],
        "body_en": ["Geist", "Arial", "Times New Roman"],
        "code": ["Consolas"]
      },
      "sizes_pt": {
        "title_main": 44,
        "title_sub": 32,
        "body_level_1": 24,
        "body_level_2": 18,
        "body_level_3": 14,
        "caption": 12
      }
    },
    "layouts": {
      "mixed_content": {
        "title_box": {"x": 0.05, "y": 0.05, "w": 0.90, "h": 0.15},
        "content_left": {"x": 0.05, "y": 0.20, "w": 0.425, "h": 0.70},
        "content_right": {"x": 0.525, "y": 0.20, "w": 0.425, "h": 0.70}
      },
      "text_heavy": {
        "title_box": {"x": 0.05, "y": 0.05, "w": 0.90, "h": 0.15},
        "content_body": {"x": 0.05, "y": 0.20, "w": 0.90, "h": 0.75}
      },
      "title_only": {
        "title_box": {"x": 0.10, "y": 0.40, "w": 0.80, "h": 0.20, "align": "center"}
      }
    },
    "style_guides": {
      "bullet_points": ["✔", ">>", "01", "02"],
      "alignment": {
        "title": "left",
        "body_short": "left",
        "body_long": "justify"
      },
      "margins": {
        "global_margin_percent": 0.05
      }
    },
    "text_generation_patterns": [
      "{number} {concept}: {explanation}",
      "{concept} vs {concept}: {comparison}",
      "{conclusion_first_clause}, {explanation_clause}"
    ]
  }
}
```
