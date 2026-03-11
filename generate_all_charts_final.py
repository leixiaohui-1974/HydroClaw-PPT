#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成HydroClaw PPT所需的所有高质量图表
使用matplotlib确保可控性和质量
"""

import sys
import io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
import numpy as np
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

# 配色
C = {
    'purple': '#7B1FA2',
    'orange': '#FF7043',
    'green': '#4CAF50',
    'cyan': '#44A5DC',
    'blue': '#5B9BD5',
    'yellow': '#FFC000',
    'white': '#FFFFFF',
    'gray': '#CCCCCC',
    'dark_gray': '#666666'
}

output_dir = Path("D:/cowork/ppt/nano_diagrams")
output_dir.mkdir(exist_ok=True)

print("=" * 60)
print("HydroClaw PPT 高质量图表生成器")
print("=" * 60)

# 图表1: 四层架构金字塔
print("\n生成图表1: 四层架构金字塔...")
fig, ax = plt.subplots(figsize=(19.2, 10.8))
ax.set_xlim(0, 19.2)
ax.set_ylim(0, 10.8)
ax.axis('off')

layers = [
    ('对象层与元件库\nObject Layer', 2, 14, 1.8, C['cyan']),
    ('计算引擎层\nComputing Engine Layer', 4.3, 11, 1.8, C['green']),
    ('技能编排层\nSkill Orchestration Layer', 6.6, 8, 1.8, C['orange']),
    ('认知决策层\nCognitive Decision Layer', 8.9, 5, 1.8, C['purple'])
]

for name, y, width, height, color in layers:
    x = 9.6 - width / 2
    rect = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='white', linewidth=4, alpha=0.9)
    ax.add_patch(rect)
    ax.text(9.6, y + height/2, name, ha='center', va='center',
           fontsize=20, fontweight='bold', color='white')

# 添加箭头
for i in range(3):
    y_start = 2 + i * 2.3 + 1.8
    ax.arrow(9.6, y_start + 0.1, 0, 0.3, head_width=0.4, head_length=0.15,
            fc=C['dark_gray'], ec=C['dark_gray'], linewidth=2)

ax.text(9.6, 10.2, 'HydroClaw 四层智能决策体系', ha='center', va='center',
       fontsize=28, fontweight='bold', color='#1565C0')

plt.tight_layout()
plt.savefig(output_dir / "architecture_pyramid.png", dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')
plt.close()
print("✓ 已保存: architecture_pyramid.png")

# 图表2: 对比图
print("\n生成图表2: 对比图表...")
fig, ax = plt.subplots(figsize=(19.2, 10.8))

categories = ['设计效率\nDesign Efficiency', '准确性\nAccuracy',
             '可解释性\nExplainability', '学习成本\nLearning Cost']
traditional = [30, 60, 40, 80]
hydroclaw = [90, 95, 85, 30]

x = np.arange(len(categories))
width = 0.35

bars1 = ax.barh(x + width/2, traditional, width, label='传统方法 Traditional',
               color=C['gray'], alpha=0.8)
bars2 = ax.barh(x - width/2, hydroclaw, width, label='HydroClaw',
               color=C['blue'], alpha=0.9)

# 添加数值标签
for i, (v1, v2) in enumerate(zip(traditional, hydroclaw)):
    ax.text(v1 + 2, i + width/2, f'{v1}%', va='center', fontsize=14, fontweight='bold')
    ax.text(v2 + 2, i - width/2, f'{v2}%', va='center', fontsize=14, fontweight='bold')

ax.set_yticks(x)
ax.set_yticklabels(categories, fontsize=16)
ax.set_xlabel('得分 Score (%)', fontsize=16, fontweight='bold')
ax.set_title('传统方法 vs HydroClaw 对比\nTraditional Method vs HydroClaw Comparison',
            fontsize=24, fontweight='bold', pad=20)
ax.legend(fontsize=16, loc='lower right')
ax.set_xlim(0, 105)
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_dir / "comparison_chart.png", dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')
plt.close()
print("✓ 已保存: comparison_chart.png")

# 图表3: 决策流程
print("\n生成图表3: 决策流程图...")
fig, ax = plt.subplots(figsize=(19.2, 10.8))
ax.set_xlim(0, 19.2)
ax.set_ylim(0, 10.8)
ax.axis('off')

steps = [
    ('用户输入\nUser Input', 2, 5.4, C['blue']),
    ('意图理解\nIntent\nUnderstanding', 5, 5.4, C['orange']),
    ('方案生成\nSolution\nGeneration', 8, 5.4, C['blue']),
    ('规则校核\nRule\nVerification', 11, 5.4, C['orange']),
    ('优化调整\nOptimization', 14, 5.4, C['blue']),
    ('结果输出\nResult\nOutput', 17, 5.4, C['orange'])
]

for name, x, y, color in steps:
    circle = Circle((x, y), 0.8, facecolor=color, edgecolor='white',
                   linewidth=3, alpha=0.9)
    ax.add_patch(circle)
    ax.text(x, y, name, ha='center', va='center',
           fontsize=13, fontweight='bold', color='white')

# 添加箭头
for i in range(5):
    x_start = 2 + i * 3 + 0.9
    x_end = 2 + (i + 1) * 3 - 0.9
    ax.arrow(x_start, 5.4, x_end - x_start - 0.1, 0,
            head_width=0.3, head_length=0.2,
            fc=C['dark_gray'], ec=C['dark_gray'], linewidth=2.5)

ax.text(9.6, 8.5, 'HydroClaw 决策流程\nDecision Process',
       ha='center', va='center', fontsize=26, fontweight='bold', color='#1565C0')

plt.tight_layout()
plt.savefig(output_dir / "decision_flow.png", dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')
plt.close()
print("✓ 已保存: decision_flow.png")

# 图表4: KPI效果
print("\n生成图表4: KPI效果展示...")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(19.2, 10.8))

kpis = [
    (ax1, '15%', '能耗降低\nEnergy Reduction', C['blue']),
    (ax2, '3-5x', '效率提升\nEfficiency Improvement', C['green']),
    (ax3, '30%', '漏损降低\nLeakage Reduction', C['orange']),
    (ax4, '70%', '培养周期缩短\nTraining Time Reduction', C['yellow'])
]

for ax, number, label, color in kpis:
    ax.text(0.5, 0.6, number, ha='center', va='center',
           fontsize=80, fontweight='bold', color=color,
           transform=ax.transAxes)
    ax.text(0.5, 0.3, label, ha='center', va='center',
           fontsize=20, color='#333333', transform=ax.transAxes)
    ax.axis('off')
    # 添加边框
    rect = Rectangle((0.05, 0.05), 0.9, 0.9, fill=False,
                     edgecolor='#e0e0e0', linewidth=2,
                     transform=ax.transAxes)
    ax.add_patch(rect)

plt.suptitle('HydroClaw 核心效果指标\nKey Performance Indicators',
            fontsize=28, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(output_dir / "kpi_metrics.png", dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')
plt.close()
print("✓ 已保存: kpi_metrics.png")

print("\n" + "=" * 60)
print("✅ 所有图表生成完成！")
print(f"📁 保存位置: {output_dir}")
print("=" * 60)
