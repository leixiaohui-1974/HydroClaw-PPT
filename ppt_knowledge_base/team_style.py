"""
HydroClaw 团队PPT风格配置模块
基于11个团队PPT样本（559页）的风格提炼 + Gemini设计评审优化
可直接被 python-pptx 脚本 import 使用

使用方法:
    from ppt_knowledge_base.team_style import *
    # 或
    from ppt_knowledge_base.team_style import COLOR_PALETTE, FONT_CONFIG, LAYOUT_PRESETS
"""
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN


# ============================================================
# 1. 配色方案 COLOR_PALETTE
# 来源：团队PPT频率分析 + Gemini配色评审优化
# 风格定义："深海科技蓝" — 契合水利+AI双重属性
# ============================================================
COLOR_PALETTE = {
    # 主色系
    "primary":       RGBColor(0x00, 0x5B, 0xAC),  # 智源海蓝 — 品牌主色、大面积色块
    "secondary":     RGBColor(0x00, 0xB4, 0xD8),  # 数字浅葱 — 高亮文字、核心图标
    "accent":        RGBColor(0xF2, 0x64, 0x19),  # 警示亮橙 — 极少量使用、关键数据强调
    "accent_green":  RGBColor(0x00, 0xC9, 0xA7),  # 活力青绿 — 正面指标、成功状态

    # 背景色
    "bg_dark":       RGBColor(0x0B, 0x13, 0x20),  # 深渊夜空蓝 — 深色背景
    "bg_card":       RGBColor(0x1E, 0x2D, 0x40),  # 深海岩灰 — 卡片/分区背景
    "bg_light":      RGBColor(0xF0, 0xF4, 0xF8),  # 云雾灰白 — 浅色背景
    "bg_white":      RGBColor(0xFF, 0xFF, 0xFF),  # 纯白

    # 文字色
    "text_on_dark":  RGBColor(0xE2, 0xE8, 0xF0),  # 云母灰白 — 深色背景上的正文
    "text_on_light": RGBColor(0x2D, 0x3A, 0x4A),  # 墨蓝灰 — 浅色背景上的正文
    "text_gray":     RGBColor(0x6B, 0x7B, 0x8D),  # 中灰 — 次要信息/注释
    "text_white":    RGBColor(0xFF, 0xFF, 0xFF),  # 纯白标题

    # 分隔/装饰
    "divider_dark":  RGBColor(0x1E, 0x2D, 0x40),  # 分隔线（深色模式）
    "divider_light": RGBColor(0xD0, 0xD8, 0xE0),  # 分隔线（浅色模式）

    # 团队原有高频色（保留兼容）
    "legacy_blue":   RGBColor(0x00, 0x49, 0x92),  # 原始高频蓝
    "legacy_navy":   RGBColor(0x0D, 0x1B, 0x2A),  # 原始深蓝背景
    "legacy_gold":   RGBColor(0xED, 0x7D, 0x31),  # 原始金橙色
}

# 快捷别名
PRIMARY = COLOR_PALETTE["primary"]
SECONDARY = COLOR_PALETTE["secondary"]
ACCENT = COLOR_PALETTE["accent"]
DARK = COLOR_PALETTE["bg_dark"]
WHITE = COLOR_PALETTE["bg_white"]
LIGHT_BG = COLOR_PALETTE["bg_light"]
TEXT_DARK = COLOR_PALETTE["text_on_light"]
TEXT_LIGHT = COLOR_PALETTE["text_on_dark"]
TEXT_GRAY = COLOR_PALETTE["text_gray"]

# 预设配色主题
THEME_DARK = {
    "background": COLOR_PALETTE["bg_dark"],
    "card": COLOR_PALETTE["bg_card"],
    "title": COLOR_PALETTE["text_white"],
    "body": COLOR_PALETTE["text_on_dark"],
    "accent": COLOR_PALETTE["secondary"],
    "divider": COLOR_PALETTE["divider_dark"],
}

THEME_LIGHT = {
    "background": COLOR_PALETTE["bg_white"],
    "card": COLOR_PALETTE["bg_light"],
    "title": COLOR_PALETTE["text_on_light"],
    "body": COLOR_PALETTE["text_on_light"],
    "accent": COLOR_PALETTE["primary"],
    "divider": COLOR_PALETTE["divider_light"],
}


# ============================================================
# 2. 字体方案 FONT_CONFIG
# 来源：23种字体分析 + Gemini字体评审
# 微软雅黑占绝对主导，配合Geist/Arial英文字体
# ============================================================
FONT_CONFIG = {
    # 方案A：现代科技风（推荐用于HydroClaw产品发布）
    "modern": {
        "title_cn": "Microsoft YaHei",
        "title_en": "Geist",
        "body_cn":  "Microsoft YaHei",
        "body_en":  "Geist",
    },
    # 方案B：严谨学术风（项目报告/答辩）
    "academic": {
        "title_cn": "Microsoft YaHei",
        "title_en": "Arial",
        "body_cn":  "Microsoft YaHei",
        "body_en":  "Times New Roman",
    },
    # 方案C：通用商务风
    "business": {
        "title_cn": "Microsoft YaHei",
        "title_en": "Calibri",
        "body_cn":  "Microsoft YaHei",
        "body_en":  "Calibri",
    },

    # 字号规范（基于频率统计）
    "sizes": {
        "title_main":   Pt(44),    # 封面/章节大标题
        "title_sub":    Pt(32),    # 副标题/章节标题
        "title_slide":  Pt(30),    # 内容页标题
        "body_level_1": Pt(24),    # 正文一级
        "body_level_2": Pt(18),    # 正文二级
        "body_level_3": Pt(14),    # 正文三级/辅助文字
        "caption":      Pt(12),    # 图注/来源标注
    },

    # 默认方案
    "default_font": "Microsoft YaHei",
}

# 快捷字号
TITLE_SIZE = Pt(30)
SUBTITLE_SIZE = Pt(22)
BODY_SIZE = Pt(18)
SMALL_SIZE = Pt(14)
CAPTION_SIZE = Pt(12)


# ============================================================
# 3. 版式预设 LAYOUT_PRESETS
# 来源：559页版式分析 + Gemini版式规范
# 基准幻灯片尺寸：13.33 x 7.5 英寸（16:9宽屏）
# ============================================================
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

LAYOUT_PRESETS = {
    # 封面/标题页
    "cover": {
        "description": "封面标题页 — 深色背景、大标题居中偏左",
        "background": "dark",
        "elements": {
            "accent_bar":  {"left": Inches(0),   "top": Inches(0),     "width": Inches(0.15), "height": SLIDE_HEIGHT},
            "title":       {"left": Inches(1.5), "top": Inches(2.0),   "width": Inches(10),   "height": Inches(2)},
            "subtitle":    {"left": Inches(1.5), "top": Inches(4.2),   "width": Inches(10),   "height": Inches(1.5)},
            "bottom_line": {"left": Inches(1.5), "top": Inches(6.5),   "width": Inches(3),    "height": Inches(0.04)},
        },
    },

    # 章节分隔页
    "chapter": {
        "description": "章节分隔页 — 主色背景、章号+大标题",
        "background": "primary",
        "elements": {
            "chapter_num": {"left": Inches(1.5), "top": Inches(1.5),   "width": Inches(10),  "height": Inches(1)},
            "title":       {"left": Inches(1.5), "top": Inches(2.5),   "width": Inches(10),  "height": Inches(2)},
            "subtitle":    {"left": Inches(1.5), "top": Inches(4.8),   "width": Inches(10),  "height": Inches(1)},
            "bottom_line": {"left": Inches(1.5), "top": Inches(6.2),   "width": Inches(2),   "height": Inches(0.04)},
        },
    },

    # 标准内容页（text_heavy — 29.9%）
    "content": {
        "description": "标准内容页 — 白色背景、标题+正文列表",
        "background": "white",
        "elements": {
            "top_bar":    {"left": Inches(0),   "top": Inches(0),     "width": SLIDE_WIDTH,  "height": Inches(0.06)},
            "title":      {"left": Inches(0.8), "top": Inches(0.4),   "width": Inches(11),   "height": Inches(0.8)},
            "separator":  {"left": Inches(0.8), "top": Inches(1.25),  "width": Inches(2),    "height": Inches(0.03)},
            "body":       {"left": Inches(0.8), "top": Inches(1.6),   "width": Inches(11),   "height": Inches(5)},
            "footer":     {"left": Inches(0.8), "top": Inches(6.8),   "width": Inches(11),   "height": Inches(0.5)},
        },
    },

    # 双栏对比页（mixed_content — 56.7%）
    "two_column": {
        "description": "双栏对比页 — 左右对比布局",
        "background": "white",
        "elements": {
            "top_bar":     {"left": Inches(0),   "top": Inches(0),     "width": SLIDE_WIDTH,  "height": Inches(0.06)},
            "title":       {"left": Inches(0.8), "top": Inches(0.4),   "width": Inches(11),   "height": Inches(0.8)},
            "separator":   {"left": Inches(0.8), "top": Inches(1.25),  "width": Inches(2),    "height": Inches(0.03)},
            "left_bg":     {"left": Inches(0.6), "top": Inches(1.6),   "width": Inches(5.5),  "height": Inches(5.2)},
            "left_title":  {"left": Inches(0.9), "top": Inches(1.8),   "width": Inches(5),    "height": Inches(0.6)},
            "left_body":   {"left": Inches(0.9), "top": Inches(2.5),   "width": Inches(5),    "height": Inches(4)},
            "right_bg":    {"left": Inches(6.6), "top": Inches(1.6),   "width": Inches(5.5),  "height": Inches(5.2)},
            "right_title": {"left": Inches(6.9), "top": Inches(1.8),   "width": Inches(5),    "height": Inches(0.6)},
            "right_body":  {"left": Inches(6.9), "top": Inches(2.5),   "width": Inches(5),    "height": Inches(4)},
        },
    },

    # 高亮/强调页
    "highlight": {
        "description": "高亮强调页 — 深色背景、大字核心观点",
        "background": "dark",
        "elements": {
            "label":    {"left": Inches(1.5), "top": Inches(1.5),   "width": Inches(10),  "height": Inches(1)},
            "title":    {"left": Inches(1.5), "top": Inches(2.5),   "width": Inches(10),  "height": Inches(3)},
            "subtitle": {"left": Inches(1.5), "top": Inches(5.5),   "width": Inches(10),  "height": Inches(1.5)},
        },
    },

    # 数据统计页
    "stats": {
        "description": "数据统计页 — 大数字+说明标签",
        "background": "white",
        "max_columns": 4,
        "elements": {
            "top_bar":   {"left": Inches(0),   "top": Inches(0),     "width": SLIDE_WIDTH, "height": Inches(0.06)},
            "title":     {"left": Inches(0.8), "top": Inches(0.4),   "width": Inches(11),  "height": Inches(0.8)},
            "separator": {"left": Inches(0.8), "top": Inches(1.25),  "width": Inches(2),   "height": Inches(0.03)},
            # 数据卡片区域动态计算
            "cards_area": {"left": Inches(1.0), "top": Inches(2.0), "width": Inches(10.5), "height": Inches(4.0)},
        },
    },
}


# ============================================================
# 4. 文字表述风格 TEXT_STYLE
# 来源：3047个标题分析 + 200个关键词 + Gemini文案评审
# ============================================================
TEXT_STYLE = {
    # 标题模式（三种主要范式）
    "title_patterns": [
        "{number} {concept}：{explanation}",           # 01 控制跃迁：SIM→HDC
        "{concept} — {definition}",                     # HydroMAS — 多智能体中枢层
        "{conclusion}",                                 # 核心结论前置
    ],

    # 标题常用动词
    "title_verbs": [
        "构建", "实现", "优化", "驱动", "融合",
        "突破", "赋能", "引领", "覆盖", "支撑",
    ],

    # 领域核心术语TOP30
    "domain_terms": [
        "水网", "认知", "智能", "调度", "水资源",
        "HydroClaw", "MCP", "Agent", "多智能体", "知识图谱",
        "数字孪生", "预报", "防洪", "水质", "生态",
        "模型", "优化", "监测", "巡检", "应急",
        "Ray", "Transformer", "RAG", "向量检索", "分布式",
        "水文", "流域", "水库群", "闸泵", "管网",
    ],

    # 措辞风格要点（Gemini总结）
    "tone_guidelines": [
        "宏大叙事 — 使用'全球首个'、'认知跃迁'等前沿词汇",
        "结构化对比 — 'XX vs XX'、'从...到...'模式",
        "符号化强调 — 使用 >>、✔、01/02 等视觉引导符号",
        "结论前置 — 标题直接呈现核心观点，不绕弯",
    ],

    # 常用短语模板
    "phrase_templates": [
        "从{old}走向{new}",
        "{concept}不仅是{thing}，更是{bigger_thing}",
        "让每一个{role}都拥有{capability}",
        "{number}+{unit}的{metric}",
        "效率提升{percent}%",
        "时间从{old_time}缩短到{new_time}",
    ],

    # 编号风格
    "numbering_styles": [
        "01 / 02 / 03",     # 两位数编号（科技风）
        "Phase A / B / C",   # 英文阶段编号
        "L0 / L1 / L2",     # 层级编号
        "第一章 / 第二章",    # 中文章节
    ],
}


# ============================================================
# 5. 图片素材索引 IMAGE_ASSETS
# 来源：858张图片提取分类
# ============================================================
IMAGE_ASSETS = {
    "base_dir": "D:/cowork/ppt/ppt_knowledge_base/images",
    "categories": {
        "backgrounds": "背景图片（大面积图片、渐变底图）",
        "diagrams":    "架构图、流程图、示意图（564张）",
        "photos":      "实景照片（水库、大坝、监控中心等）",
        "icons":       "图标和小元素（268张）",
        "charts":      "数据图表（柱状图、折线图等）",
    },
    "total_images": 858,
    "sources": [
        "智慧水利团队V5(4).pptx — 团队介绍、项目照片",
        "自主运行水网理论 — 架构图、技术示意图",
        "京津冀复杂水网 — 答辩图表、实验数据",
        "HydroClaw_Gamma_80p — AI生成的现代风格图",
    ],
}


# ============================================================
# 6. 设计规范 DESIGN_RULES
# 来源：Gemini设计评审建议
# ============================================================
DESIGN_RULES = {
    "spacing": {
        "margin_percent": 0.05,           # 页面边距比例（5%）
        "paragraph_spacing": Pt(6),       # 段落间距
        "bullet_spacing": Pt(4),          # 列表项间距
        "section_gap": Inches(0.3),       # 板块间距
    },
    "alignment": {
        "title": PP_ALIGN.LEFT,           # 标题左对齐
        "body_short": PP_ALIGN.LEFT,      # 短要点左对齐
        "body_long": PP_ALIGN.JUSTIFY,    # 长段落两端对齐
        "stats_number": PP_ALIGN.CENTER,  # 数据统计居中
        "footer": PP_ALIGN.LEFT,          # 页脚左对齐
    },
    "whitespace": {
        "highlight_page_min": 0.70,       # 强调页最低留白率70%
        "content_page_margin": 0.05,      # 内容页四周留白5%
    },
    "transitions": {
        "chapter_every_n_slides": 10,     # 每10页左右一个章节分隔
        "max_bullets_per_slide": 8,       # 每页最多8个要点
        "max_text_per_bullet": 50,        # 每个要点最多50字
    },
}
