#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HydroClaw 架构图生成器
使用matplotlib生成专业的四层架构金字塔图
"""

import sys
import io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 配色方案
COLORS = {
    'purple': '#7B1FA2',
    'orange': '#FF7043',
    'green': '#4CAF50',
    'cyan': '#44A5DC',
    'white': '#FFFFFF',
    'gray': '#E0E0E0'
}

def create_architecture_pyramid():
    """生成四层架构金字塔图"""
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # 四层架构（从下到上）
    layers = [
        {
            'name': '对象层与元件库',
            'name_en': 'Object Layer & Component Library',
            'y': 1.5,
            'width': 12,
            'height': 1.2,
            'color': COLORS['cyan'],
            'icons': ['管道', '水泵', '节点', '管段', '拓扑']
        },
        {
            'name': '计算引擎层',
            'name_en': 'Computing Engine Layer',
            'y': 3.2,
            'width': 10,
            'height': 1.2,
            'color': COLORS['green'],
            'icons': ['预测', '优化', '仿真', '学习', '验证', '可视化', '报告']
        },
        {
            'name': '技能编排层',
            'name_en': 'Skill Orchestration Layer',
            'y': 4.9,
            'width': 8,
            'height': 1.2,
            'color': COLORS['orange'],
            'icons': ['原子技能', '复合技能', '流程技能']
        },
        {
            'name': '认知决策层',
            'name_en': 'Cognitive Decision Layer',
            'y': 6.6,
            'width': 6,
            'height': 1.2,
            'color': COLORS['purple'],
            'icons': ['大模型', '规则引擎']
        }
    ]

    # 绘制每一层
    for i, layer in enumerate(layers):
        x = 8 - layer['width'] / 2
        y = layer['y']

        # 绘制层的矩形
        rect = FancyBboxPatch(
            (x, y), layer['width'], layer['height'],
            boxstyle="round,pad=0.05",
            facecolor=layer['color'],
            edgecolor='white',
            linewidth=3,
            alpha=0.9
        )
        ax.add_patch(rect)

        # 添加层名称（中文）
        ax.text(8, y + layer['height'] - 0.25, layer['name'],
                ha='center', va='center',
                fontsize=18, fontweight='bold', color='white')

        # 添加层名称（英文）
        ax.text(8, y + 0.25, layer['name_en'],
                ha='center', va='center',
                fontsize=12, color='white', alpha=0.9)

        # 添加图标/标签
        icon_spacing = layer['width'] / (len(layer['icons']) + 1)
        for j, icon in enumerate(layer['icons']):
            icon_x = x + icon_spacing * (j + 1)
            icon_y = y + layer['height'] / 2

            # 绘制小圆点作为图标
            circle = Circle((icon_x, icon_y), 0.15,
                          facecolor='white', edgecolor=layer['color'],
                          linewidth=2, alpha=0.8)
            ax.add_patch(circle)

            # 图标文字
            ax.text(icon_x, icon_y - 0.5, icon,
                   ha='center', va='top',
                   fontsize=9, color=layer['color'], fontweight='bold')

        # 绘制层间箭头（除了最上层）
        if i < len(layers) - 1:
            arrow = FancyArrowPatch(
                (8, y + layer['height'] + 0.1),
                (8, y + layer['height'] + 0.8),
                arrowstyle='->,head_width=0.4,head_length=0.3',
                color='#666666',
                linewidth=2,
                alpha=0.6
            )
            ax.add_patch(arrow)

    # 添加标题
    ax.text(8, 8.3, 'HydroClaw 四层智能决策体系',
           ha='center', va='center',
           fontsize=24, fontweight='bold', color='#1565C0')

    # 添加副标题
    ax.text(8, 0.5, '从底层对象到顶层认知的完整架构',
           ha='center', va='center',
           fontsize=14, color='#666666', style='italic')

    plt.tight_layout()
    return fig

if __name__ == "__main__":
    print("生成HydroClaw四层架构图...")
    fig = create_architecture_pyramid()
    output_path = "D:/cowork/ppt/nano_diagrams/architecture_pyramid_v2.png"
    fig.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"✓ 已保存: {output_path}")
    plt.close()
