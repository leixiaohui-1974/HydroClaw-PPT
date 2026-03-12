"""
HydroClaw PPT — 基于 Presenton 渲染引擎的智能PPT生成工具

核心能力：
  1. 复用团队现有素材（架构图、照片、图标）
  2. 继承团队PPT风格（深海科技蓝配色 + 微软雅黑字体）
  3. 自动匹配图片到对应幻灯片
  4. 预留 image_prompt 字段供 nano/banana AI图片生成

用法:
    python presenton_cli.py --demo                        # 内置HydroClaw发布会演示
    python presenton_cli.py -i slides.json -o output.pptx # 从JSON生成
    python presenton_cli.py --schema                      # 导出JSON schema

架构:
    素材知识库 + JSON内容 → SlideBuilder → PptxPresentationModel → Presenton渲染 → PPTX
"""
import sys
import os
import asyncio
import argparse
import tempfile
import json
import glob as glob_mod

# 将 Presenton FastAPI 目录加入 sys.path
PRESENTON_DIR = os.path.join(os.path.dirname(__file__), "presenton", "servers", "fastapi")
sys.path.insert(0, PRESENTON_DIR)

os.environ.setdefault("APP_DATA_DIRECTORY", os.path.join(os.path.dirname(__file__), "presenton", "app_data"))

from models.pptx_models import (
    PptxPresentationModel, PptxSlideModel, PptxTextBoxModel,
    PptxAutoShapeBoxModel, PptxConnectorModel, PptxPictureBoxModel,
    PptxPositionModel, PptxFontModel, PptxFillModel, PptxParagraphModel,
    PptxSpacingModel, PptxStrokeModel, PptxShadowModel, PptxTextRunModel,
    PptxPictureModel, PptxObjectFitModel, PptxObjectFitEnum,
)
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from services.pptx_presentation_creator import PptxPresentationCreator

# ============================================================
# 常量
# ============================================================
SW, SH = 1280, 720  # Presenton 坐标系 (pt)
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "ppt_knowledge_base", "images")


# ============================================================
# 素材索引 — 关键词 → 图片路径 映射
# ============================================================
class AssetIndex:
    """团队素材知识库索引，按关键词自动匹配图片"""

    # 手工标注的核心素材（高质量、与HydroClaw直接相关）
    CURATED = {
        # Gamma AI生成的科技感照片
        "cover_dam":       "photos/HydroClaw_Gamma_80p.pptx_s0_75ec2073.png",    # 科技水坝夜景
        "cover_river":     "photos/HydroClaw_Gamma_80p.pptx_s2_3cd76b73.png",    # 蓝色河流山谷
        "ai_brain":        "photos/HydroClaw_Gamma_80p.pptx_s4_e9babea1.png",    # AI大脑网络
        "water_network":   "photos/HydroClaw_Gamma_80p.pptx_s5_10546a2a.png",    # 数字水网城市鸟瞰
        "smart_water":     "photos/HydroClaw_Gamma_80p.pptx_s9_9704e5e6.png",    # 智慧水利场景

        # 50页完整版的专业图表
        "comparison_chart": "diagrams/HydroClaw_50页完整版_最终.pptx_s3_6e05a0a4.png",   # 传统vs HC对比
        "kpi_dashboard":    "diagrams/HydroClaw_50页完整版_最终.pptx_s4_7eab9d8c.png",   # KPI指标卡片
        "four_layers":      "diagrams/HydroClaw_50页完整版_最终.pptx_s11_fca21bc7.png",  # 四层架构图(简)
        "decision_flow":    "diagrams/HydroClaw_50页完整版_最终.pptx_s13_5db57668.png",  # 决策流程图

        # 发布会V4的高质量素材
        "v4_arch":    "photos/HydroClaw_发布会_V4.pptx_s12_5eff916c.png",  # 四层架构(深色版)
        "v4_scene1":  "photos/HydroClaw_发布会_V4.pptx_s20_5eee083a.png",
        "v4_scene2":  "photos/HydroClaw_发布会_V4.pptx_s24_9b002fa6.png",
        "v4_scene3":  "photos/HydroClaw_发布会_V4.pptx_s28_12903159.png",
        "v4_scene4":  "photos/HydroClaw_发布会_V4.pptx_s38_0eb94fc9.png",
        "v4_scene5":  "photos/HydroClaw_发布会_V4.pptx_s55_78a5d68e.png",
        "v4_deploy":  "photos/HydroClaw_发布会_V4.pptx_s58_dc31afa0.png",
        "v4_team":    "photos/HydroClaw_发布会_V4.pptx_s62_7f74ac07.png",
        "v4_future":  "photos/HydroClaw_发布会_V4.pptx_s63_c1ea08c8.png",
        "v4_end":     "photos/HydroClaw_发布会_V4.pptx_s69_5d5ab1c6.png",
    }

    def __init__(self, base_dir=ASSETS_DIR):
        self.base_dir = base_dir

    def get(self, key):
        """按标注key获取绝对路径"""
        rel = self.CURATED.get(key)
        if rel:
            path = os.path.join(self.base_dir, rel)
            if os.path.exists(path):
                return path
        return None

    def resolve(self, image_ref):
        """解析图片引用：支持 asset:key、绝对路径、相对路径"""
        if not image_ref:
            return None
        if image_ref.startswith("asset:"):
            return self.get(image_ref[6:])
        if os.path.isabs(image_ref) and os.path.exists(image_ref):
            return image_ref
        # 相对于素材目录
        path = os.path.join(self.base_dir, image_ref)
        if os.path.exists(path):
            return path
        # 相对于工作目录
        if os.path.exists(image_ref):
            return os.path.abspath(image_ref)
        return None

    def search(self, keyword):
        """按关键词在素材目录中搜索（简单文件名匹配）"""
        results = []
        for subdir in ["photos", "diagrams", "icons"]:
            d = os.path.join(self.base_dir, subdir)
            if not os.path.isdir(d):
                continue
            for f in os.listdir(d):
                if keyword.lower() in f.lower():
                    results.append(os.path.join(d, f))
        return results


ASSETS = AssetIndex()


# ============================================================
# 团队风格配色
# ============================================================
class T:
    """团队风格主题 — 深海科技蓝"""
    PRIMARY    = "005BAC"
    SECONDARY  = "00B4D8"
    ACCENT     = "F26419"
    GREEN      = "00C9A7"
    BG_DARK    = "0B1320"
    BG_CARD    = "1E2D40"
    BG_LIGHT   = "F0F4F8"
    BG_WHITE   = "FFFFFF"
    TEXT_WHITE  = "FFFFFF"
    TEXT_LIGHT  = "E2E8F0"
    TEXT_DARK   = "2D3A4A"
    TEXT_GRAY   = "6B7B8D"
    TEXT_HINT   = "A0B0C0"
    FONT_CN    = "Microsoft YaHei"


# ============================================================
# 构建辅助函数
# ============================================================

def font(size=16, color=T.TEXT_DARK, bold=False, italic=False, name=T.FONT_CN):
    return PptxFontModel(name=name, size=size, color=color,
                         font_weight=700 if bold else 400, italic=italic)

def para(text, size=16, color=T.TEXT_DARK, bold=False, align=None,
         spacing_top=0, spacing_bottom=0, line_height=None):
    return PptxParagraphModel(
        text=text, font=font(size, color, bold), alignment=align,
        spacing=PptxSpacingModel(top=spacing_top, bottom=spacing_bottom)
            if (spacing_top or spacing_bottom) else None,
        line_height=line_height)

def textbox(left, top, width, height, paragraphs, fill=None, margin=None):
    return PptxTextBoxModel(
        position=PptxPositionModel(left=left, top=top, width=width, height=height),
        paragraphs=paragraphs if isinstance(paragraphs, list) else [paragraphs],
        fill=PptxFillModel(color=fill) if isinstance(fill, str) else fill,
        margin=margin)

def autoshape(left, top, width, height, fill=None, stroke=None, shadow=None,
              border_radius=None, paragraphs=None,
              shape_type=MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE):
    return PptxAutoShapeBoxModel(
        type=shape_type,
        position=PptxPositionModel(left=left, top=top, width=width, height=height),
        fill=PptxFillModel(color=fill) if isinstance(fill, str) else fill,
        stroke=PptxStrokeModel(color=stroke[0], thickness=stroke[1]) if stroke else None,
        shadow=shadow, border_radius=border_radius, paragraphs=paragraphs)

def picture(left, top, width, height, image_path, object_fit="cover", border_radius=None):
    """创建图片元素"""
    return PptxPictureBoxModel(
        position=PptxPositionModel(left=left, top=top, width=width, height=height),
        picture=PptxPictureModel(is_network=False, path=image_path),
        clip=True,
        object_fit=PptxObjectFitModel(fit=PptxObjectFitEnum(object_fit)) if object_fit else None,
        border_radius=border_radius)

def connector(left, top, width, height=0, color=T.SECONDARY, thickness=2):
    return PptxConnectorModel(
        position=PptxPositionModel(left=left, top=top, width=width, height=height),
        color=color, thickness=thickness)

def slide(shapes, bg=T.BG_WHITE, note=None):
    return PptxSlideModel(background=PptxFillModel(color=bg), shapes=shapes, note=note)


# ============================================================
# 幻灯片模板 — 10 种类型
# ============================================================

def cover_slide(title, subtitle="", author="", image=None):
    """封面页 — 深色背景，可选右侧大图"""
    img_path = ASSETS.resolve(image) if image else None
    shapes = []

    if img_path:
        # 右侧放图片（圆角裁切）
        shapes.append(picture(680, 40, 560, 640, img_path, "cover", border_radius=[20, 20, 20, 20]))
        text_w = 600
    else:
        text_w = 1100

    shapes += [
        autoshape(0, 0, 8, SH, fill=T.SECONDARY, border_radius=0,
                  shape_type=MSO_AUTO_SHAPE_TYPE.RECTANGLE),
        textbox(80, 180, text_w, 180, [
            para(title, size=48, color=T.TEXT_WHITE, bold=True)]),
        textbox(80, 380, text_w, 120, [
            para(subtitle, size=22, color=T.SECONDARY, line_height=1.5)]),
        connector(80, 560, 250, color=T.SECONDARY, thickness=3),
    ]
    if author:
        shapes.append(textbox(80, 580, 500, 50, [
            para(author, size=14, color=T.TEXT_HINT)]))
    return slide(shapes, bg=T.BG_DARK)


def chapter_slide(chapter_num, title, subtitle="", image=None):
    """章节分隔页 — 主色背景，可选右侧图片"""
    img_path = ASSETS.resolve(image) if image else None
    shapes = []

    if img_path:
        shapes.append(picture(780, 80, 440, 560, img_path, "cover", border_radius=[16, 16, 16, 16]))
        text_w = 700
    else:
        text_w = 1080

    shapes += [
        textbox(100, 150, text_w, 80, [
            para(f"第{chapter_num}章", size=24, color="80D0FF")]),
        textbox(100, 240, text_w, 180, [
            para(title, size=44, color=T.TEXT_WHITE, bold=True)]),
        connector(100, 560, 200, color=T.TEXT_WHITE, thickness=3),
    ]
    if subtitle:
        shapes.append(textbox(100, 440, text_w, 80, [
            para(subtitle, size=20, color="B0E0FF")]))
    return slide(shapes, bg=T.PRIMARY)


def content_slide(title, bullets, note="", image=None):
    """标准内容页 — 可选右侧图片"""
    img_path = ASSETS.resolve(image) if image else None

    shapes = [
        autoshape(0, 0, SW, 5, fill=T.PRIMARY, shape_type=MSO_AUTO_SHAPE_TYPE.RECTANGLE),
        textbox(60, 35, 1100, 65, [para(title, size=30, color=T.BG_DARK, bold=True)]),
        connector(60, 105, 180, color=T.SECONDARY, thickness=2),
    ]

    if img_path:
        # 左文右图布局
        shapes.append(textbox(60, 125, 640, 530, [
            para(b, size=17, color=T.TEXT_DARK, spacing_bottom=4, line_height=1.4) for b in bullets]))
        shapes.append(picture(730, 130, 510, 510, img_path, "cover", border_radius=[12, 12, 12, 12]))
    else:
        shapes.append(textbox(60, 125, 1150, 530, [
            para(b, size=18, color=T.TEXT_DARK, spacing_bottom=4, line_height=1.4) for b in bullets]))

    if note:
        shapes.append(textbox(60, 670, 1150, 40, [para(note, size=11, color=T.TEXT_GRAY)]))
    return slide(shapes, bg=T.BG_WHITE, note=note)


def two_column_slide(title, left_title, left_items, right_title, right_items):
    """双栏页"""
    shapes = [
        autoshape(0, 0, SW, 5, fill=T.PRIMARY, shape_type=MSO_AUTO_SHAPE_TYPE.RECTANGLE),
        textbox(60, 35, 1100, 65, [para(title, size=30, color=T.BG_DARK, bold=True)]),
        connector(60, 105, 180, color=T.SECONDARY, thickness=2),
        autoshape(40, 125, 575, 540, fill=T.BG_LIGHT, border_radius=10),
        textbox(65, 140, 520, 50, [para(left_title, size=20, color=T.PRIMARY, bold=True)]),
        textbox(65, 200, 520, 440, [
            para(i, size=16, color=T.TEXT_DARK, spacing_bottom=4, line_height=1.4) for i in left_items]),
        autoshape(645, 125, 575, 540, fill=T.BG_LIGHT, border_radius=10),
        textbox(670, 140, 520, 50, [para(right_title, size=20, color=T.PRIMARY, bold=True)]),
        textbox(670, 200, 520, 440, [
            para(i, size=16, color=T.TEXT_DARK, spacing_bottom=4, line_height=1.4) for i in right_items]),
    ]
    return slide(shapes, bg=T.BG_WHITE)


def highlight_slide(label, main_text, sub_text="", image=None):
    """高亮强调页 — 可选背景图"""
    img_path = ASSETS.resolve(image) if image else None
    shapes = []

    if img_path:
        # 半透明暗色遮罩 + 图片背景效果：右侧放图
        shapes.append(picture(700, 0, 580, SH, img_path, "cover"))
        # 左侧半透明遮罩保证文字可读
        shapes.append(autoshape(660, 0, 100, SH,
                                fill=PptxFillModel(color=T.BG_DARK, opacity=0.7),
                                shape_type=MSO_AUTO_SHAPE_TYPE.RECTANGLE))

    shapes += [
        textbox(100, 140, 580 if img_path else 1080, 80, [
            para(label, size=22, color=T.SECONDARY)]),
        textbox(100, 230, 580 if img_path else 1080, 280, [
            para(main_text, size=36, color=T.TEXT_WHITE, bold=True, line_height=1.5)]),
    ]
    if sub_text:
        shapes.append(textbox(100, 520, 580 if img_path else 1080, 120, [
            para(sub_text, size=18, color=T.TEXT_HINT, line_height=1.4)]))
    return slide(shapes, bg=T.BG_DARK)


def stats_slide(title, stats):
    """数据统计页"""
    n = len(stats)
    card_w = min(260, (SW - 120) // n - 20)
    total_w = n * card_w + (n - 1) * 20
    start_x = (SW - total_w) // 2
    shapes = [
        autoshape(0, 0, SW, 5, fill=T.PRIMARY, shape_type=MSO_AUTO_SHAPE_TYPE.RECTANGLE),
        textbox(60, 35, 1100, 65, [para(title, size=30, color=T.BG_DARK, bold=True)]),
        connector(60, 105, 180, color=T.SECONDARY, thickness=2),
    ]
    for i, (num, label) in enumerate(stats):
        x = start_x + i * (card_w + 20)
        shapes += [
            autoshape(x, 180, card_w, 400, fill=T.BG_LIGHT, border_radius=12),
            textbox(x, 240, card_w, 120, [para(num, size=48, color=T.PRIMARY, bold=True, align=PP_ALIGN.CENTER)]),
            textbox(x, 380, card_w, 120, [para(label, size=15, color=T.TEXT_DARK, align=PP_ALIGN.CENTER, line_height=1.4)]),
        ]
    return slide(shapes, bg=T.BG_WHITE)


def numbered_list_slide(title, items):
    """编号列表页"""
    shapes = [
        autoshape(0, 0, SW, 5, fill=T.PRIMARY, shape_type=MSO_AUTO_SHAPE_TYPE.RECTANGLE),
        textbox(60, 35, 1100, 65, [para(title, size=30, color=T.BG_DARK, bold=True)]),
        connector(60, 105, 180, color=T.SECONDARY, thickness=2),
    ]
    y = 130
    row_h = min(70, 520 // max(len(items), 1))
    for i, item in enumerate(items):
        shapes += [
            autoshape(60, y + 5, 36, 36, fill=T.PRIMARY, border_radius=18,
                      paragraphs=[para(f"{i+1:02d}", size=14, color=T.TEXT_WHITE, bold=True, align=PP_ALIGN.CENTER)]),
            textbox(110, y, 1100, row_h, [para(item, size=17, color=T.TEXT_DARK, line_height=1.3)]),
        ]
        y += row_h
    return slide(shapes, bg=T.BG_WHITE)


def three_card_slide(title, cards):
    """三卡片页"""
    card_w, gap = 370, 20
    total_w = 3 * card_w + 2 * gap
    start_x = (SW - total_w) // 2
    colors = [T.PRIMARY, T.SECONDARY, T.GREEN]
    shapes = [
        autoshape(0, 0, SW, 5, fill=T.PRIMARY, shape_type=MSO_AUTO_SHAPE_TYPE.RECTANGLE),
        textbox(60, 35, 1100, 65, [para(title, size=30, color=T.BG_DARK, bold=True)]),
        connector(60, 105, 180, color=T.SECONDARY, thickness=2),
    ]
    for i, (card_title, card_body) in enumerate(cards):
        x = start_x + i * (card_w + gap)
        shapes += [
            autoshape(x, 135, card_w, 520, fill=T.BG_LIGHT, border_radius=12),
            autoshape(x + 15, 145, card_w - 30, 5, fill=colors[i % 3],
                      shape_type=MSO_AUTO_SHAPE_TYPE.RECTANGLE),
            textbox(x + 20, 165, card_w - 40, 50, [para(card_title, size=20, color=colors[i % 3], bold=True)]),
            textbox(x + 20, 225, card_w - 40, 410, [
                para(line, size=15, color=T.TEXT_DARK, spacing_bottom=3, line_height=1.35)
                for line in (card_body if isinstance(card_body, list) else [card_body])]),
        ]
    return slide(shapes, bg=T.BG_WHITE)


def image_slide(title="", image=None, caption="", image_prompt=None):
    """全幅图片页 — 图片铺满，标题叠加在底部
    image_prompt: 预留给 nano/banana AI图片生成"""
    img_path = ASSETS.resolve(image) if image else None
    shapes = []

    if img_path:
        shapes.append(picture(0, 0, SW, SH, img_path, "cover"))
        # 底部渐变遮罩区域
        shapes.append(autoshape(0, SH - 180, SW, 180,
                                fill=PptxFillModel(color=T.BG_DARK, opacity=0.75),
                                shape_type=MSO_AUTO_SHAPE_TYPE.RECTANGLE))
    if title:
        shapes.append(textbox(60, SH - 160, 1160, 70, [
            para(title, size=32, color=T.TEXT_WHITE, bold=True)]))
    if caption:
        shapes.append(textbox(60, SH - 80, 1160, 50, [
            para(caption, size=16, color=T.TEXT_HINT)]))

    # 如果没有图片但有 image_prompt，显示占位提示
    if not img_path and image_prompt:
        shapes.insert(0, autoshape(100, 100, SW - 200, SH - 300, fill=T.BG_CARD, border_radius=20,
                                    paragraphs=[
                                        para("[AI Image Placeholder]", size=24, color=T.TEXT_GRAY, align=PP_ALIGN.CENTER),
                                        para(image_prompt, size=14, color=T.TEXT_HINT, align=PP_ALIGN.CENTER),
                                    ]))

    return slide(shapes, bg=T.BG_DARK)


def image_content_slide(title, bullets, image=None, image_side="right", image_prompt=None):
    """图文混排页 — 一侧文字、一侧图片（最常用版式，占团队PPT 56.7%）"""
    img_path = ASSETS.resolve(image) if image else None
    shapes = [
        autoshape(0, 0, SW, 5, fill=T.PRIMARY, shape_type=MSO_AUTO_SHAPE_TYPE.RECTANGLE),
        textbox(60, 35, 1100, 65, [para(title, size=30, color=T.BG_DARK, bold=True)]),
        connector(60, 105, 180, color=T.SECONDARY, thickness=2),
    ]

    if img_path:
        if image_side == "right":
            shapes.append(textbox(60, 125, 600, 530, [
                para(b, size=17, color=T.TEXT_DARK, spacing_bottom=4, line_height=1.4) for b in bullets]))
            shapes.append(picture(700, 130, 540, 520, img_path, "cover", border_radius=[12, 12, 12, 12]))
        else:
            shapes.append(picture(40, 130, 540, 520, img_path, "cover", border_radius=[12, 12, 12, 12]))
            shapes.append(textbox(620, 125, 600, 530, [
                para(b, size=17, color=T.TEXT_DARK, spacing_bottom=4, line_height=1.4) for b in bullets]))
    else:
        # 没有图片时退化为标准 content 布局
        shapes.append(textbox(60, 125, 1150, 530, [
            para(b, size=18, color=T.TEXT_DARK, spacing_bottom=4, line_height=1.4) for b in bullets]))
        if image_prompt:
            shapes.append(autoshape(750, 150, 460, 460, fill=T.BG_LIGHT, border_radius=16,
                                    paragraphs=[
                                        para("[AI图片待生成]", size=16, color=T.TEXT_GRAY, align=PP_ALIGN.CENTER),
                                        para(image_prompt, size=12, color=T.TEXT_HINT, align=PP_ALIGN.CENTER),
                                    ]))

    return slide(shapes, bg=T.BG_WHITE)


# ============================================================
# HydroClaw 发布会内容 — 带素材关联
# ============================================================

def build_hydroclaw_slides():
    slides = []

    # === 封面 ===
    slides.append(cover_slide(
        "HydroClaw",
        "水网认知智能体系发布会\n中国水利水电科学研究院 · 2026年4月",
        "HydroClaw Team | hydroclaw@iwhr.com",
        image="asset:cover_dam"
    ))

    # === 目录 ===
    slides.append(numbered_list_slide("目 录", [
        "第一章  愿景与定位 — 水利行业的AI革命",
        "第二章  三层产品架构 — HydroOS + HydroMAS + HydroTouch",
        "第三章  五层技术纵深 — L0-L4全栈架构",
        "第四章  应用场景 — 十大核心场景",
        "第五章  技术优势 — 开源、易用、专业",
        "第六章  发展路线图 — 从MVP到行业引领",
        "第七章  团队与合作 — 开放共赢的生态",
    ]))

    # ===== 第一章 =====
    slides.append(chapter_slide("一", "愿景与定位", "水利行业的AI革命",
                                image="asset:cover_river"))

    slides.append(highlight_slide("行业背景",
        "中国水网管理面临前所未有的挑战",
        "15万+水利工程 · 跨流域调度复杂性 · 极端气候频发",
        image="asset:water_network"))

    slides.append(three_card_slide("水利行业三大痛点", [
        ("数据孤岛", ["各水利工程系统独立", "数据格式不统一", "跨部门共享困难", "历史数据利用率低"]),
        ("决策滞后", ["传统模型计算耗时长", "无法实时响应极端事件", "人工经验依赖性强", "多目标冲突难以平衡"]),
        ("人才短缺", ["高水平工程师供不应求", "培养周期长（5-10年）", "经验知识传承断层", "新技术学习成本高"]),
    ]))

    slides.append(image_content_slide("AI大模型时代的历史性机遇", [
        ">> 大语言模型（LLM）的突破性进展",
        ">> 多智能体系统（MAS）的成熟应用",
        ">> AI Agent 技术的实际落地",
        ">> GPU 算力的指数级增长",
        ">> 水利行业数字化转型的政策驱动",
        ">> 「数字孪生流域」国家战略的推进",
    ], image="asset:ai_brain"))

    slides.append(highlight_slide("HydroClaw 是什么",
        "全球首个面向水网运行管理的\n认知智能体系",
        "Cognitive Intelligence System for Water Network Operations",
        image="asset:smart_water"))

    slides.append(content_slide("HydroClaw 核心定位", [
        "不是简单的「AI+水利」叠加",
        "而是深度融合的认知决策平台",
        "",
        "核心理念：",
        "让每一个水利从业者都拥有一个「AI首席工程师」",
        "",
        "从经验驱动 → 智能认知驱动",
    ]))

    slides.append(two_column_slide("使命与愿景",
        "使命", ["用AI重新定义水网运行管理方式", "打造万人万用的水网认知操作系统", "5年内覆盖中国50%重要水利工程"],
        "愿景", ["成为全球水利行业的「大脑」", "让水利从「靠经验」到「靠智能」", "让决策从「事后处理」到「事前预判」"]))

    slides.append(numbered_list_slide("产品六大版本", [
        "HydroClaw Lite — 个人助理版（面向个人水利工程师）",
        "HydroClaw Pro — 专业版（面向水利设计/咨询企业）",
        "HydroClaw Enterprise — 企业版（面向水利管理局/大型水务集团）",
        "HydroClaw Cloud — 云服务版（SaaS模式，按需付费）",
        "HydroClaw Edge — 边缘版（面向物联网/现场设备）",
        "HydroClaw Open — 开源社区版（推动行业生态）",
    ]))

    slides.append(two_column_slide("Lite vs Pro",
        "Lite — 个人助理版", ["面向个人水利工程师", "AI助手问答", "基础数据查询", "简单报告生成", "免费使用"],
        "Pro — 专业版", ["面向设计/咨询企业", "多Agent协同", "专业模型运行", "高级数据分析", "团队协作功能"]))

    # ===== 第二章 =====
    slides.append(chapter_slide("二", "三层产品架构", "HydroOS + HydroMAS + HydroTouch",
                                image="asset:v4_arch"))

    slides.append(highlight_slide("架构总览",
        "如果HydroClaw是一个人\nHydroOS是躯体，HydroMAS是大脑\nHydroTouch是五官和四肢",
        "三层架构是HydroClaw的核心创新"))

    slides.append(three_card_slide("三层架构概览", [
        ("HydroOS — 计算底座层", ["21个MCP Server", "Ray分布式计算", "知识图谱+向量检索", "数据湖统一管理", "提供数据、算力、工具"]),
        ("HydroMAS — 多智能体中枢层", ["15个专业Agent", "17个可组合Skill", "IntentRouter智能路由", "认知决策引擎", "四阶认知循环"]),
        ("HydroTouch — 多端接入层", ["Web专业工作台", "飞书深度集成", "Tauri桌面+Flutter移动", "AR眼镜巡检", "开放API/MCP接口"]),
    ]))

    # HydroOS
    slides.append(image_content_slide("HydroOS 核心能力", [
        ">> 21个MCP Server — 水文数据、GIS、气象、水质等",
        ">> Ray分布式计算 — 千核级并行模拟",
        ">> 知识图谱 — 百万级水利实体",
        ">> 向量检索 — 专业RAG系统",
        ">> 数据湖 — 多源异构统一管理",
    ], image="asset:four_layers"))

    slides.append(numbered_list_slide("8大水文MCP", [
        "hydro_data_mcp — 水文数据采集与管理",
        "hydro_model_mcp — 水文模型调度",
        "hydro_gis_mcp — GIS空间分析",
        "hydro_forecast_mcp — 水文预报",
        "hydro_quality_mcp — 水质监测分析",
        "hydro_iot_mcp — 物联网设备管理",
        "hydro_knowledge_mcp — 知识图谱查询",
        "hydro_optimize_mcp — 优化调度",
    ]))

    slides.append(two_column_slide("HydroOS 技术栈",
        "计算与存储", ["计算框架：Ray + CUDA", "关系数据库：PostgreSQL + PostGIS", "图数据库：Neo4j", "缓存：Redis", "对象存储：MinIO"],
        "基础设施", ["消息队列：RabbitMQ + Kafka", "容器化：Docker + Kubernetes", "监控：Prometheus + Grafana", "日志：ELK Stack", "CI/CD：GitHub Actions"]))

    # HydroMAS
    slides.append(image_content_slide("HydroMAS 核心能力", [
        ">> 15个专业Agent",
        ">> 17个Skill",
        ">> IntentRouter 智能意图路由",
        ">> AgentCoordinator 多Agent协同",
        ">> 认知决策引擎 — 四阶认知循环",
    ], image="asset:decision_flow"))

    slides.append(three_card_slide("三大核心Agent", [
        ("FloodGuardAgent", ["实时监测降雨/水位/流量", "AI预测洪水演进", "自动生成调度建议", "多方案比选与风险评估", "预报提前6小时+"]),
        ("WaterAllocAgent", ["跨流域水资源优化", "多目标优化（供水/灌溉/生态/发电）", "自动生成调度方案", "What-if情景模拟", "利用率提升15%+"]),
        ("QualityPatrolAgent", ["实时监测pH/溶解氧/COD", "异常检测自动识别", "知识图谱污染溯源", "自动巡检报告", "发现时间24h→30min"]),
    ]))

    slides.append(content_slide("认知决策引擎", [
        "四阶认知循环：感知 → 理解 → 决策 → 行动",
        "",
        "核心技术：",
        "✔ 多模态融合：文本 + 图像 + 时序 + 空间数据",
        "✔ 上下文管理：长期记忆 + 工作记忆 + 情景记忆",
        "✔ 不确定性推理：贝叶斯网络 + 模糊逻辑",
        "✔ 可解释AI：决策过程透明可追溯",
    ]))

    # HydroTouch
    slides.append(numbered_list_slide("六大接入方式", [
        "Web端 — React + Ant Design 专业工作台",
        "飞书集成 — 6大场景深度对接企业协作",
        "Tauri桌面端 — 轻量级跨平台原生应用",
        "Flutter移动端 — 现场巡检与应急响应",
        "AR眼镜 — 增强现实辅助巡检维护",
        "API / MCP Server — 开放接口供第三方调用",
    ]))

    # ===== 第三章 =====
    slides.append(chapter_slide("三", "五层技术纵深", "L0-L4 全栈架构"))

    slides.append(three_card_slide("L0-L2 基础层", [
        ("L0 Data Layer", ["多源异构数据统一管理", "时序数据高效存储", "空间数据GIS原生支持", "数据血缘和质量管理", "PB级存储能力"]),
        ("L1 Compute Layer", ["Ray集群弹性伸缩", "GPU加速深度学习", "统一模型训练推理", "Kafka Streams实时处理", "Spark大规模批处理"]),
        ("L2 MCP Tools Layer", ["21个标准化MCP Server", "统一认证鉴权", "自动API文档", "流式响应+长任务", "可热插拔独立部署"]),
    ]))

    slides.append(two_column_slide("L3-L4 智能层",
        "L3 Skills Layer", ["17个可组合原子技能", "技能编排引擎", "声明式定义和注册", "版本管理和灰度发布", "性能监控自动优化"],
        "L4 Agents Layer", ["15个自主决策智能体", "A2A通信协议", "任务分解多Agent协同", "自主学习经验积累", "Agent市场可扩展"]))

    slides.append(content_slide("14个核心算法模块", [
        "01 水文时间序列预测 — LSTM / Transformer",
        "02 洪水演进模拟 — Saint-Venant方程",
        "03 水资源优化调度 — 多目标遗传算法",
        "04 水质扩散模型 — WASP / QUAL2K",
        "05 降雨径流模型 — 新安江 / SCS-CN",
        "06 水库群联合调度 — 动态规划 + 强化学习",
        "07 知识图谱推理 — TransE / RotatE嵌入",
    ]))

    slides.append(image_slide("传统方法 vs HydroClaw 对比",
                              image="asset:comparison_chart",
                              caption="数据来源：团队内部测试 | 4个维度全面领先"))

    slides.append(stats_slide("测试与质量保障", [
        ("1851", "自动化测试"), (">80%", "代码覆盖率"),
        ("3层", "测试体系\n(单元/集成/E2E)"), ("24/7", "CI/CD流水线"),
    ]))

    # ===== 第四章 =====
    slides.append(chapter_slide("四", "应用场景", "十大核心场景",
                                image="asset:v4_scene1"))

    slides.append(three_card_slide("场景1-3：核心调度", [
        ("防洪调度", ["痛点：极端降雨频发", "方案：FloodGuard+Simulation", "预报提前6小时", "决策4h→30min", "损失减少40%+"]),
        ("水资源调配", ["痛点：跨流域多目标冲突", "方案：WaterAlloc+多目标优化", "利用率提升15%", "方案3天→2小时", "年节水效益数千万"]),
        ("水质监测", ["痛点：污染发现滞后", "方案：QualityPatrol+知识图谱", "发现24h→30min", "溯源准确率90%+", "自动生成应急方案"]),
    ]))

    slides.append(three_card_slide("场景4-6：现场与应急", [
        ("智能巡检", ["痛点：人力成本高", "方案：Inspection+AR+IoT", "效率提升300%", "隐患发现率+50%", "报告自动生成"]),
        ("应急响应", ["痛点：响应链条长", "方案：Alert+Coordinator+飞书", "响应2h→15min", "建议自动推送", "全流程可追溯"]),
        ("知识管理", ["痛点：知识碎片化", "方案：Knowledge+图谱+RAG", "上手6月→1月", "检索效率10倍", "行业最大知识库"]),
    ]))

    slides.append(image_slide("HydroClaw 核心效果指标",
                              image="asset:kpi_dashboard",
                              caption="能耗降低15% · 效率提升3-5x · 漏损降低30% · 培养周期缩短70%"))

    slides.append(stats_slide("十大场景效果总览", [
        ("6h+", "洪水预报\n提前时间"), ("15%", "水资源\n利用率提升"),
        ("300%", "巡检效率\n提升"), ("90%", "遗漏率\n降低"),
    ]))

    # ===== 第五章 =====
    slides.append(chapter_slide("五", "技术优势", "开源 · 易用 · 专业"))

    slides.append(highlight_slide("全栈开源",
        "代码 · 文档 · 模型权重\n全部开放",
        "许可证：MIT License  |  GitHub Stars 1000+"))

    slides.append(content_slide("开源优势", [
        "✔ 透明可信 — 代码完全公开，可审计可验证",
        "✔ 社区驱动 — 汇聚全球水利AI开发者",
        "✔ 快速迭代 — 社区贡献加速产品进化",
        "✔ 生态丰富 — 第三方插件和扩展",
        "✔ 无厂商锁定 — 自主可控，数据安全",
        "✔ 学术合作 — 支持科研和教育",
    ]))

    slides.append(content_slide("Docker一键部署", [
        "docker compose up -d",
        "",
        "✔ 5分钟完成全栈部署",
        "✔ 支持CPU / GPU双模式",
        "✔ 自动配置数据库、消息队列、存储",
        "✔ 包含监控和日志系统",
        "✔ 支持单机和集群模式",
    ]))

    slides.append(highlight_slide("知识飞轮效应",
        "数据 → 模型 → 决策 → 反馈 → 更多数据",
        "越用越智能的自学习系统 · 用户越多系统越强 · 形成正向反馈闭环"))

    slides.append(two_column_slide("安全与合规",
        "数据安全", ["端到端加密传输", "静态数据加密存储", "细粒度权限控制", "数据脱敏处理", "审计日志全记录"],
        "合规认证", ["等保三级认证", "ISO 27001", "水利行业标准合规", "隐私计算支持", "国产化适配"]))

    # ===== 第六章 =====
    slides.append(chapter_slide("六", "发展路线图", "从MVP到行业引领"))

    slides.append(content_slide("Phase A（2026 Q1-Q2）：MVP", [
        ">> 核心Agent上线：FloodGuard、WaterAlloc、QualityPatrol",
        ">> 基础MCP Tools完成（8个核心MCP）",
        ">> Web端和飞书端开放",
        ">> 基础知识图谱构建",
        ">> 首批3家试点单位接入",
    ]))

    slides.append(content_slide("Phase B-C（2026 Q3 - 2027）", [
        "Phase B 增强（2026 Q3-Q4）：",
        "  · 全部15个Agent上线 · 认知决策引擎优化",
        "  · Tauri桌面端+Flutter移动端 · 知识图谱百万级",
        "",
        "Phase C 生态（2027）：",
        "  · 开发者平台 · 第三方插件市场",
        "  · AR/IoT深度集成 · Agent市场开放",
    ]))

    slides.append(two_column_slide("Phase D-E 远景",
        "Phase D（2028）规模化", ["覆盖50+重要水利工程", "多语言国际化", "行业标准制定参与", "SaaS商业化", "年收入突破亿元"],
        "Phase E（2029+）引领", ["全球水利AI标准", "数字孪生流域全覆盖", "自主进化认知系统", "覆盖全球", "水利行业操作系统"]))

    # ===== 第七章 =====
    slides.append(chapter_slide("七", "团队与合作", "开放共赢的生态",
                                image="asset:v4_team"))

    slides.append(content_slide("中国水利水电科学研究院", [
        "国家级水利科研机构 · 70+年水利科技积累",
        "水利行业最权威的技术支撑单位",
        "",
        "技术团队：",
        "✔ AI研究组 — 大模型、多Agent系统、知识图谱",
        "✔ 水利专家组 — 水文、水资源、水环境、水工程",
        "✔ 工程团队 — 全栈开发、DevOps、质量保障",
    ]))

    slides.append(content_slide("开放合作", [
        ">> 学术合作 — 高校联合研究",
        ">> 产业合作 — 水务企业联合创新",
        ">> 生态合作 — 开发者社区共建",
        ">> 标准合作 — 行业标准共同制定",
        "",
        "联系方式：hydroclaw@iwhr.com",
        "GitHub: github.com/leixiaohui-1974/HydroClaw",
    ]))

    # === 闭幕 ===
    slides.append(highlight_slide("AI赋能水网，认知驱动未来",
        "HydroClaw不仅是一个产品\n更是一种全新的水利工作方式",
        "当AI真正理解水，世界将变得不同。",
        image="asset:cover_dam"))

    shapes = [
        textbox(0, 230, SW, 150, [para("谢 谢", size=72, color=T.TEXT_WHITE, bold=True, align=PP_ALIGN.CENTER)]),
        textbox(0, 430, SW, 80, [para("hydroclaw@iwhr.com  |  github.com/leixiaohui-1974/HydroClaw",
                                       size=18, color="B0E0FF", align=PP_ALIGN.CENTER)]),
    ]
    slides.append(slide(shapes, bg=T.PRIMARY))

    return slides


# ============================================================
# JSON → Slides 通用解析器
# ============================================================

SLIDE_TYPE_MAP = {
    "cover": cover_slide, "chapter": chapter_slide, "content": content_slide,
    "two_column": two_column_slide, "highlight": highlight_slide, "stats": stats_slide,
    "numbered_list": numbered_list_slide, "three_card": three_card_slide,
    "image": image_slide, "image_content": image_content_slide,
}

def build_slides_from_json(json_data):
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    slides_list = []
    for i, s in enumerate(json_data.get("slides", [])):
        stype = s.get("type", "content")
        if stype not in SLIDE_TYPE_MAP:
            print(f"  Warning: Unknown slide type '{stype}' at index {i}")
            continue
        try:
            # 通用参数提取
            kw = {k: v for k, v in s.items() if k != "type"}
            # 特殊处理 stats 和 cards 字段（JSON数组→tuple）
            if "stats" in kw:
                kw["stats"] = [tuple(x) for x in kw["stats"]]
            if "cards" in kw:
                kw["cards"] = [(c[0], c[1]) for c in kw["cards"]]
            slides_list.append(SLIDE_TYPE_MAP[stype](**kw))
        except Exception as e:
            print(f"  Error building slide {i} ({stype}): {e}")
    return slides_list


# ============================================================
# 主程序
# ============================================================

async def generate_pptx(output_path, slides_list, title="Presentation"):
    model = PptxPresentationModel(name=title, slides=slides_list)
    with tempfile.TemporaryDirectory() as tmp:
        creator = PptxPresentationCreator(model, tmp)
        await creator.create_ppt()
        out_dir = os.path.dirname(os.path.abspath(output_path))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        creator.save(output_path)
    print(f"Done! Generated {len(slides_list)} slides → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="HydroClaw PPT — 基于Presenton渲染引擎的智能PPT生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python presenton_cli.py --demo                    # 内置HydroClaw发布会\n"
               "  python presenton_cli.py -i slides.json            # 从JSON生成\n"
               "  python presenton_cli.py --schema                  # 导出JSON schema\n"
               "  python presenton_cli.py --list-assets             # 列出可用素材\n")
    parser.add_argument("-i", "--input", help="输入JSON文件路径")
    parser.add_argument("-o", "--output", default="output.pptx", help="输出PPTX路径")
    parser.add_argument("-t", "--title", default="", help="演示文稿标题")
    parser.add_argument("--demo", action="store_true", help="使用内置HydroClaw内容")
    parser.add_argument("--schema", action="store_true", help="导出JSON schema")
    parser.add_argument("--list-assets", action="store_true", help="列出素材库中的可用资源")
    args = parser.parse_args()

    if args.schema:
        schema = {
            "slide_types": {
                "cover":         {"params": "title, subtitle?, author?, image?"},
                "chapter":       {"params": "chapter_num, title, subtitle?, image?"},
                "content":       {"params": "title, bullets[], note?, image?"},
                "two_column":    {"params": "title, left_title, left_items[], right_title, right_items[]"},
                "highlight":     {"params": "label, main_text, sub_text?, image?"},
                "stats":         {"params": "title, stats[[num,label],...]"},
                "numbered_list": {"params": "title, items[]"},
                "three_card":    {"params": "title, cards[[title,[lines]],...]"},
                "image":         {"params": "title?, image, caption?, image_prompt?"},
                "image_content": {"params": "title, bullets[], image?, image_side?, image_prompt?"},
            },
            "image_refs": "asset:key | 绝对路径 | 相对路径 (相对于素材目录)",
            "image_prompt": "预留给 nano/banana AI图片生成（当前显示占位符）",
        }
        print(json.dumps(schema, ensure_ascii=False, indent=2))
        return

    if args.list_assets:
        print("=== 素材库资源 ===")
        print(f"目录: {ASSETS_DIR}\n")
        print("--- 标注素材 (asset:key) ---")
        for key, rel in sorted(AssetIndex.CURATED.items()):
            path = os.path.join(ASSETS_DIR, rel)
            exists = "OK" if os.path.exists(path) else "MISSING"
            print(f"  asset:{key:20s} [{exists}] {rel}")
        print(f"\n--- 分类统计 ---")
        for subdir in ["photos", "diagrams", "icons"]:
            d = os.path.join(ASSETS_DIR, subdir)
            if os.path.isdir(d):
                count = len(os.listdir(d))
                print(f"  {subdir:10s}: {count} 文件")
        return

    if args.demo:
        slides_list = build_hydroclaw_slides()
        title = args.title or "HydroClaw"
        if args.output == "output.pptx":
            args.output = "发布会26.4/output/HydroClaw_Presenton_v3.pptx"
    elif args.input:
        ext = os.path.splitext(args.input)[1].lower()
        if ext == ".md":
            # Markdown 输入 → 自动解析为 JSON
            from markdown_parser import parse_markdown_file
            json_data = parse_markdown_file(args.input)
        elif ext == ".pptx":
            # 现有 PPT → 提取内容结构
            from pptx_to_json import extract_pptx_to_json
            json_data = extract_pptx_to_json(args.input)
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                json_data = json.load(f)
        slides_list = build_slides_from_json(json_data)
        title = args.title or json_data.get("title", "Presentation")
    else:
        if not sys.stdin.isatty():
            json_data = json.load(sys.stdin)
            slides_list = build_slides_from_json(json_data)
            title = args.title or json_data.get("title", "Presentation")
        else:
            parser.print_help()
            sys.exit(1)

    asyncio.run(generate_pptx(args.output, slides_list, title))


if __name__ == "__main__":
    main()
