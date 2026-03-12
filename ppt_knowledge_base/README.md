# PPT风格知识库 — 总览

## 分析范围

- **HydroClaw_发布会_V4.pptx** — 80页, 13.33x7.5
- **HydroClaw_发布会_V3.pptx** — 51页, 13.33x7.5
- **HydroClaw_认知智能方案_v2.pptx** — 30页, 10.0x5.62
- **HydroClaw_50页完整版_最终.pptx** — 15页, 10.0x5.62
- **HydroClaw_50页高质量版_V2.pptx** — 15页, 10.0x5.62
- **HydroClaw_Gamma_80p.pptx** — 80页, 16.0x9.0
- **智慧水利团队V5(4).pptx** — 94页, 13.33x7.5
- **自主运行水网理论、技术与应用260121@雷晓辉.pptx** — 84页, 13.33x7.5
- **环境与生态领域-重点-河北工程大学-0916.pptx** — 40页, 13.33x7.5
- **流域水库群智能化运行与精准调控关键技术及应用PPT-1109 修改版(1)(2)(1).pptx** — 36页, 10.0x7.5
- **京津冀复杂水网运行控制关键技术与测控平台研发-答辩.pptx** — 34页, 13.33x7.5

## 知识库结构

| 模块 | 文件 | 说明 |
|------|------|------|
| 配色方案 | `colors/配色方案.md` | 推荐配色板 + 颜色频率分析 |
| 字体方案 | `fonts/字体方案.md` | 推荐字体 + 字号分布 |
| 版式分析 | `layouts/版式分析.md` | 版式类型分布 + 样本布局 |
| 文字表述 | `text/文字表述库.md` | 标题文案 + 领域关键词 |
| 图片素材 | `images/图片素材索引.md` | 分类图片资源 |

## 使用方式

### 用于 python-pptx 生成
```python
import json
# 加载配色方案
with open('ppt_knowledge_base/colors/color_analysis.json') as f:
    colors = json.load(f)
# 使用推荐配色
primary = colors['recommended_palette']['主色调（强调色）'][0][0]
```

### 用于 Presenton
将知识库内容作为 `instructions` 参数传入生成请求，
指导AI按团队风格生成内容。
