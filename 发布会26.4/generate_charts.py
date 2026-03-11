#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HydroClaw 发布会PPT 专业图表生成器
生成8张高质量matplotlib图表，用于50页PPT
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from pathlib import Path
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import warnings
warnings.filterwarnings('ignore')

# 中文字体配置
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT = Path("D:/cowork/ppt/发布会26.4/images")
OUT.mkdir(exist_ok=True)

# 配色方案
COLORS = {
    'blue': '#5B9BD5', 'dark_blue': '#1F4E78', 'light_blue': '#D6E4F0',
    'orange': '#ED7D31', 'green': '#70AD47', 'yellow': '#FFC000',
    'purple': '#8E7CC3', 'cyan': '#4472C4', 'red': '#C00000',
    'gray': '#7F7F7F', 'light_gray': '#F2F2F2', 'white': '#FFFFFF',
    'bg': '#0D1B2A', 'bg2': '#1B2838',
}

DPI = 200
FIG_W, FIG_H = 16, 9  # 16:9宽屏


def save(fig, name):
    fig.savefig(OUT / name, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ {name} ({(OUT/name).stat().st_size//1024}KB)")


def chart_01_architecture_pyramid():
    """四层架构金字塔图"""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # 标题
    ax.text(8, 8.5, 'HydroClaw 四层智能决策体系', fontsize=28, fontweight='bold',
            color='white', ha='center', va='center')

    layers = [
        (1.5, 0.5, 13, 1.5, COLORS['yellow'], '④ 对象层', '三族元件库（物理/水文/模型）+ 水网组装',
         '算什么 — 具体的元件实例和工程系统', 0.85),
        (2.5, 2.2, 11, 1.5, COLORS['green'], '③ 计算引擎层', '七大通用引擎 + 工具箱',
         '怎么算 — 与领域无关的纯算法', 0.85),
        (3.5, 3.9, 9, 1.5, COLORS['orange'], '② 技能编排层', 'Skill体系（原子→组合→流程）',
         '做什么 — 知道按什么顺序调引擎', 0.85),
        (4.5, 5.6, 7, 1.5, COLORS['blue'], '① 认知决策层', '大模型 + 规则引擎 + 模板渲染',
         '理解意图、选择Skill、约束行为', 0.9),
    ]

    for x, y, w, h, color, title, desc, sub, alpha in layers:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                              facecolor=color, alpha=alpha, edgecolor='white', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.65, title, fontsize=20, fontweight='bold',
                color='white', ha='center', va='center')
        ax.text(x + w/2, y + h*0.35, desc, fontsize=12,
                color='white', ha='center', va='center', alpha=0.9)
        ax.text(x + w/2, y + h*0.12, sub, fontsize=10,
                color='white', ha='center', va='center', alpha=0.7, style='italic')

    # 箭头：单向调用
    for i in range(3):
        y_start = layers[i+1][1]
        y_end = layers[i][1] + layers[i][3]
        ax.annotate('', xy=(8, y_end + 0.05), xytext=(8, y_start - 0.05),
                    arrowprops=dict(arrowstyle='->', color='white', lw=2, alpha=0.6))

    ax.text(15.5, 4.5, '单\n向\n调\n用', fontsize=12, color='white', alpha=0.5,
            ha='center', va='center', fontweight='bold')

    save(fig, 'chart_architecture_pyramid.png')


def chart_02_seven_engines():
    """七大引擎环形图"""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(-5, 5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(0, 3.2, '七大通用计算引擎', fontsize=28, fontweight='bold',
            color='white', ha='center')

    engines = [
        ('仿真引擎', 'Saint-Venant\nMOC/ODE', COLORS['blue']),
        ('辨识引擎', 'UKF/EnKF\n遗传算法', COLORS['cyan']),
        ('调度引擎', 'LP/MILP\nDP/SDDP', COLORS['green']),
        ('控制引擎', 'PID/MPC\nDMPC', COLORS['orange']),
        ('优化引擎', 'SQP/GA\nDE/PSO', COLORS['yellow']),
        ('预测引擎', 'LSTM/GNN\nTransformer', COLORS['purple']),
        ('学习引擎', 'RL/模仿\n在线学习', COLORS['red']),
    ]

    n = len(engines)
    R = 2.2
    for i, (name, desc, color) in enumerate(engines):
        angle = np.pi/2 + 2*np.pi*i/n
        x = R * np.cos(angle)
        y = R * np.sin(angle) - 0.3

        circle = plt.Circle((x, y), 0.75, facecolor=color, alpha=0.85,
                            edgecolor='white', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y + 0.15, name, fontsize=13, fontweight='bold',
                color='white', ha='center', va='center')
        ax.text(x, y - 0.25, desc, fontsize=8, color='white',
                ha='center', va='center', alpha=0.8)

    # 中心
    center = plt.Circle((0, -0.3), 0.9, facecolor=COLORS['dark_blue'], alpha=0.9,
                         edgecolor='white', linewidth=2)
    ax.add_patch(center)
    ax.text(0, -0.15, '统一接口', fontsize=14, fontweight='bold',
            color='white', ha='center')
    ax.text(0, -0.55, 'engine.xxx()', fontsize=10, color=COLORS['yellow'],
            ha='center', family='monospace')

    # 连接线
    for i in range(n):
        angle = np.pi/2 + 2*np.pi*i/n
        x1 = 0.9 * np.cos(angle)
        y1 = 0.9 * np.sin(angle) - 0.3
        x2 = (R - 0.75) * np.cos(angle)
        y2 = (R - 0.75) * np.sin(angle) - 0.3
        ax.plot([x1, x2], [y1, y2], color='white', alpha=0.3, linewidth=1.5, linestyle='--')

    save(fig, 'chart_seven_engines.png')


def chart_03_skill_hierarchy():
    """Skill三层继承树状图"""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(8, 8.5, 'Skill 三层继承体系', fontsize=28, fontweight='bold',
            color='white', ha='center')

    def draw_box(x, y, w, h, text, color, fontsize=11):
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.1",
                              facecolor=color, alpha=0.85, edgecolor='white', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, text, fontsize=fontsize, fontweight='bold',
                color='white', ha='center', va='center')

    # S2 流程Skill
    s2_items = [('四预闭环', 2.5), ('SIL验证', 5.5), ('MBD全流程', 8.5),
                ('应急响应', 11.5), ('教学实验', 14)]
    for name, x in s2_items:
        draw_box(x, 7, 2.2, 0.7, name, COLORS['blue'])

    ax.text(0.3, 7, 'S2\n流程', fontsize=11, color=COLORS['blue'], fontweight='bold', ha='center', va='center')

    # S1 组合Skill
    s1_items = [('预报', 1.5), ('预警', 3.5), ('预演', 5.5), ('预案', 7.5),
                ('SIL测试', 9.5), ('泄漏诊断', 11.5), ('控制设计', 13.5)]
    for name, x in s1_items:
        draw_box(x, 5, 1.8, 0.7, name, COLORS['orange'])

    ax.text(0.3, 5, 'S1\n组合', fontsize=11, color=COLORS['orange'], fontweight='bold', ha='center', va='center')

    # S0 原子Skill
    s0_items = [('仿真', 1), ('辨识', 2.5), ('调度', 4), ('控制', 5.5),
                ('检测', 7), ('预测', 8.5), ('学习', 10), ('清洗', 11.5),
                ('拟合', 13), ('报告', 14.5)]
    for name, x in s0_items:
        draw_box(x, 3, 1.3, 0.7, name, COLORS['green'])

    ax.text(0.3, 3, 'S0\n原子', fontsize=11, color=COLORS['green'], fontweight='bold', ha='center', va='center')

    # 引擎层
    draw_box(8, 1, 14, 0.7, '七大通用引擎 + 工具箱（Toolkit）', COLORS['gray'], fontsize=13)

    # 连接线
    for name, x in s2_items:
        for n2, x2 in s1_items:
            if abs(x - x2) < 4:
                ax.plot([x, x2], [7 - 0.35, 5 + 0.35], color='white', alpha=0.1, linewidth=0.8)

    for name, x in s1_items:
        for n2, x2 in s0_items:
            if abs(x - x2) < 3:
                ax.plot([x, x2], [5 - 0.35, 3 + 0.35], color='white', alpha=0.1, linewidth=0.8)

    # 数量标注
    ax.text(15.5, 7, '~6个', fontsize=10, color=COLORS['blue'], ha='center', alpha=0.7)
    ax.text(15.5, 5, '~15个', fontsize=10, color=COLORS['orange'], ha='center', alpha=0.7)
    ax.text(15.5, 3, '~40个', fontsize=10, color=COLORS['green'], ha='center', alpha=0.7)

    save(fig, 'chart_skill_hierarchy.png')


def chart_04_cognitive_flow():
    """五步认知决策流程图"""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H * 0.7))
    fig.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(8, 5.5, '认知决策五步流程', fontsize=26, fontweight='bold',
            color='white', ha='center')

    steps = [
        ('Step 1', '意图理解', '大模型解析\n用户想做什么', COLORS['blue']),
        ('Step 2', 'Skill匹配', '规则+大模型\n确定调哪个Skill', COLORS['cyan']),
        ('Step 3', '规则加载', '自动加载\nL1-L4规则集', COLORS['orange']),
        ('Step 4', 'Skill执行', '调用技能\n编排层', COLORS['green']),
        ('Step 5', '模板渲染', '格式化结果\n角色修饰', COLORS['purple']),
    ]

    x_positions = np.linspace(1.5, 14.5, 5)
    y = 3

    for i, (step, title, desc, color) in enumerate(steps):
        x = x_positions[i]
        # 六边形效果用圆角矩形
        rect = FancyBboxPatch((x - 1.1, y - 0.9), 2.2, 1.8, boxstyle="round,pad=0.15",
                              facecolor=color, alpha=0.85, edgecolor='white', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y + 0.5, step, fontsize=9, color='white', ha='center', alpha=0.7)
        ax.text(x, y + 0.15, title, fontsize=14, fontweight='bold', color='white', ha='center')
        ax.text(x, y - 0.45, desc, fontsize=9, color='white', ha='center', alpha=0.85)

        # 箭头
        if i < 4:
            x_next = x_positions[i+1]
            ax.annotate('', xy=(x_next - 1.1, y), xytext=(x + 1.1, y),
                        arrowprops=dict(arrowstyle='->', color='white', lw=2.5, alpha=0.6))

    # 输入输出标注
    ax.text(0.3, y, '用户\n输入', fontsize=12, color=COLORS['yellow'], ha='center',
            va='center', fontweight='bold')
    ax.annotate('', xy=(x_positions[0] - 1.1, y), xytext=(0.8, y),
                arrowprops=dict(arrowstyle='->', color=COLORS['yellow'], lw=2))

    ax.text(15.7, y, '格式化\n输出', fontsize=12, color=COLORS['yellow'], ha='center',
            va='center', fontweight='bold')
    ax.annotate('', xy=(15.2, y), xytext=(x_positions[4] + 1.1, y),
                arrowprops=dict(arrowstyle='->', color=COLORS['yellow'], lw=2))

    # 底部注释
    ax.text(8, 1, '规则处理 ~60% 交互  |  大模型处理 ~30% 交互  |  大模型+规则兜底 ~10%',
            fontsize=11, color='white', ha='center', alpha=0.6)

    save(fig, 'chart_cognitive_flow.png')


def chart_05_comparison():
    """传统方法 vs HydroClaw 对比雷达图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(FIG_W, FIG_H),
                                    subplot_kw=dict(projection='polar'))
    fig.set_facecolor(COLORS['bg'])

    categories = ['响应速度', '专业深度', '多场景覆盖', '可扩展性', '用户友好', '安全可靠']
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    traditional = [3, 5, 2, 2, 4, 6]
    hydroclaw = [9, 8, 9, 9, 8, 9]
    traditional += traditional[:1]
    hydroclaw += hydroclaw[:1]

    for ax, values, title, color in [
        (ax1, traditional, '传统方法', COLORS['gray']),
        (ax2, hydroclaw, 'HydroClaw', COLORS['blue'])
    ]:
        ax.set_facecolor(COLORS['bg'])
        ax.fill(angles, values, color=color, alpha=0.3)
        ax.plot(angles, values, color=color, linewidth=2)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=11, color='white')
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8, color='white', alpha=0.5)
        ax.grid(color='white', alpha=0.2)
        ax.set_title(title, fontsize=18, fontweight='bold', color='white', pad=20)
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
            spine.set_alpha(0.3)

    fig.suptitle('传统方法 vs HydroClaw 能力对比', fontsize=26, fontweight='bold',
                 color='white', y=0.98)

    save(fig, 'chart_comparison_radar.png')


def chart_06_kpi_dashboard():
    """KPI效果仪表盘"""
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    fig.set_facecolor(COLORS['bg'])

    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(8, 8.3, 'HydroClaw 核心效果指标', fontsize=28, fontweight='bold',
            color='white', ha='center')

    kpis = [
        ('10×', '效率提升', '设计全流程\n自动化', COLORS['blue']),
        ('60%', '规则自动处理', '确定性交互\n无需大模型', COLORS['orange']),
        ('50+', '原子技能', '覆盖水网\n全业务场景', COLORS['green']),
        ('100+', '工具函数', '10大工具包\n日常计算', COLORS['purple']),
    ]

    for i, (num, title, desc, color) in enumerate(kpis):
        x = 2 + i * 3.5
        y = 5
        rect = FancyBboxPatch((x - 1.3, y - 1.8), 2.6, 3.6, boxstyle="round,pad=0.2",
                              facecolor=color, alpha=0.15, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y + 0.8, num, fontsize=48, fontweight='bold', color=color,
                ha='center', va='center')
        ax.text(x, y - 0.2, title, fontsize=14, fontweight='bold', color='white',
                ha='center', va='center')
        ax.text(x, y - 0.9, desc, fontsize=10, color='white', ha='center',
                va='center', alpha=0.7)

    # 底部进度条
    categories_bar = ['城市供水', '城市排水', '引调水', '河道防洪', '水库调度', '地下水']
    values_bar = [95, 85, 90, 80, 75, 50]
    y_base = 1.5
    for i, (cat, val) in enumerate(zip(categories_bar, values_bar)):
        x_start = 1.5
        bar_width = 11 * val / 100
        ax.barh(y_base - i*0.35, bar_width, height=0.25, left=x_start,
                color=COLORS['blue'], alpha=0.6)
        ax.text(x_start - 0.1, y_base - i*0.35, cat, fontsize=9, color='white',
                ha='right', va='center')
        ax.text(x_start + bar_width + 0.2, y_base - i*0.35, f'{val}%', fontsize=9,
                color='white', va='center')

    save(fig, 'chart_kpi_dashboard.png')


def chart_07_component_tree():
    """三族元件库树状图"""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(8, 8.5, '三族元件库 — 统一基类，混合组装', fontsize=26, fontweight='bold',
            color='white', ha='center')

    # 根节点
    root = FancyBboxPatch((6, 6.8), 4, 0.8, boxstyle="round,pad=0.1",
                          facecolor=COLORS['dark_blue'], edgecolor='white', linewidth=2)
    ax.add_patch(root)
    ax.text(8, 7.2, 'Component 基类', fontsize=14, fontweight='bold',
            color='white', ha='center', va='center')

    families = [
        ('第一族：物理元件', COLORS['blue'], 2.5, [
            '执行器(T1): 闸门/水泵/阀门/水轮机',
            '蓄水体(T2): 水库/湖泊/水池/调蓄池',
            '输水体(T3): 明渠/管道/河道/隧洞',
            '耦合器: 水机电/闸渠/泵管接口',
        ]),
        ('第二族：水文元件', COLORS['green'], 8, [
            '产流(H1): 流域/透水面/土壤层',
            '汇流(H2): 单位线/马斯京根/运动波',
            '气象(H3): 降雨场/蒸发场/温度场',
            '耦合器: 流域-河道/地表-地下水',
        ]),
        ('第三族：模型元件', COLORS['purple'], 13.5, [
            '替代模型(M1): IDZ/POD/PINN',
            '时序预测(M2): LSTM/Transformer/GNN',
            '策略模型(M3): RL/模仿学习',
            '水文模型(M4): 新安江/HBV/GR4J',
        ]),
    ]

    for title, color, cx, items in families:
        # 族标题
        rect = FancyBboxPatch((cx - 2, 5), 4, 0.7, boxstyle="round,pad=0.1",
                              facecolor=color, alpha=0.85, edgecolor='white', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(cx, 5.35, title, fontsize=12, fontweight='bold',
                color='white', ha='center', va='center')

        # 连接到根
        ax.plot([cx, 8], [5.7, 6.8], color='white', alpha=0.3, linewidth=1.5)

        # 子项
        for j, item in enumerate(items):
            y = 4 - j * 0.85
            rect = FancyBboxPatch((cx - 2.1, y - 0.25), 4.2, 0.5, boxstyle="round,pad=0.05",
                                  facecolor=color, alpha=0.2, edgecolor=color, linewidth=1)
            ax.add_patch(rect)
            ax.text(cx, y, item, fontsize=9, color='white', ha='center', va='center')
            ax.plot([cx, cx], [y + 0.25, 5], color=color, alpha=0.15, linewidth=0.8)

    save(fig, 'chart_component_tree.png')


def chart_08_timeline():
    """设计院三阶段渗透时间线"""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H * 0.65))
    fig.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    ax.text(8, 5, '设计院三阶段渗透策略', fontsize=26, fontweight='bold',
            color='white', ha='center')

    # 时间轴
    ax.plot([1, 15], [2.5, 2.5], color='white', linewidth=3, alpha=0.4)

    phases = [
        (3, '阶段1', '单点工具替代', ['泵站选型', '管网计算', '断面优化', '替代Excel'],
         COLORS['blue'], '3-6个月'),
        (8, '阶段2', 'MBD验证赋能', ['数字孪生', '全系统验证', '发现缺陷', '降低返工'],
         COLORS['orange'], '6-12个月'),
        (13, '阶段3', '全流程革命', ['方案自动生成', '施工图自动化', '效率提升10×', '设计革命'],
         COLORS['green'], '12-24个月'),
    ]

    for x, phase, title, items, color, duration in phases:
        # 大圆
        circle = plt.Circle((x, 2.5), 0.4, facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, 2.5, phase[-1], fontsize=14, fontweight='bold', color='white',
                ha='center', va='center')

        # 标题
        ax.text(x, 3.3, title, fontsize=15, fontweight='bold', color=color, ha='center')
        ax.text(x, 3.0, duration, fontsize=10, color='white', alpha=0.6, ha='center')

        # 子项
        for j, item in enumerate(items):
            y = 1.8 - j * 0.35
            ax.text(x, y, f'• {item}', fontsize=10, color='white', ha='center', alpha=0.8)

        # 连接线到下一阶段
        if x < 13:
            ax.annotate('', xy=(x + 2.5, 2.5), xytext=(x + 0.4, 2.5),
                        arrowprops=dict(arrowstyle='->', color='white', lw=2, alpha=0.4))

    save(fig, 'chart_timeline.png')


def chart_09_rule_layers():
    """五层规则继承"""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(8, 8.5, '五层规则继承体系', fontsize=26, fontweight='bold',
            color='white', ha='center')

    layers = [
        ('L0', '安全底线', '物理守恒 / 安全约束只紧不松 / 不编造数据', COLORS['red'], '始终加载', '不可覆盖'),
        ('L1', 'Skill角色规则', '选Skill自动加载对应角色规则', COLORS['orange'], '按Skill加载', '自动切换'),
        ('L2', '产品规则', 'SIL隔离 / MBD流程 / 操作二次确认', COLORS['yellow'], '按产品加载', ''),
        ('L3', '场景规则', '实时控制 / 设计优化 / 应急响应 / 教学', COLORS['green'], '按场景加载', ''),
        ('L4', '案例参数', '中线冰期Fr≤0.06 / 胶东泵站启停序', COLORS['blue'], '按工程加载', '最具体'),
    ]

    for i, (level, title, desc, color, load, note) in enumerate(layers):
        y = 7 - i * 1.3
        # 条带
        rect = FancyBboxPatch((1, y - 0.4), 14, 0.8, boxstyle="round,pad=0.1",
                              facecolor=color, alpha=0.25, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect)

        # 级别标签
        label_rect = FancyBboxPatch((1.2, y - 0.3), 1.2, 0.6, boxstyle="round,pad=0.05",
                                    facecolor=color, alpha=0.85, edgecolor='white', linewidth=1)
        ax.add_patch(label_rect)
        ax.text(1.8, y, level, fontsize=14, fontweight='bold', color='white', ha='center', va='center')

        ax.text(3, y + 0.1, title, fontsize=13, fontweight='bold', color='white', va='center')
        ax.text(3, y - 0.2, desc, fontsize=9, color='white', va='center', alpha=0.8)
        ax.text(13.5, y, load, fontsize=10, color=color, ha='center', va='center')

        # 向下箭头
        if i < 4:
            ax.annotate('', xy=(1.8, y - 0.4 - 0.2), xytext=(1.8, y - 0.4),
                        arrowprops=dict(arrowstyle='->', color='white', lw=1.5, alpha=0.4))

    save(fig, 'chart_rule_layers.png')


def chart_10_persona_matrix():
    """四大角色场景矩阵"""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(8, 8.5, '个人水网智能体 — 选Skill即获角色', fontsize=26, fontweight='bold',
            color='white', ha='center')

    personas = [
        ('设计工程师', '个人超级工具', ['泵站选型', '断面优化', '管网计算', 'MBD验证'],
         COLORS['blue'], '🔧'),
        ('运维人员', '智能运维助手', ['ODD预警', '故障诊断', '调度优化', '应急响应'],
         COLORS['orange'], '🔍'),
        ('科研人员', '科研实验平台', ['仿真对比', '参数辨识', '方案评估', 'RL策略'],
         COLORS['green'], '🔬'),
        ('学生教师', '智能教学助手', ['实验教学', '概念演示', '分层引导', '自动评估'],
         COLORS['purple'], '📚'),
    ]

    for i, (role, subtitle, skills, color, icon) in enumerate(personas):
        x = 2 + i * 3.5
        # 卡片背景
        rect = FancyBboxPatch((x - 1.5, 1.5), 3, 5.5, boxstyle="round,pad=0.15",
                              facecolor=color, alpha=0.12, edgecolor=color, linewidth=2)
        ax.add_patch(rect)

        # 头像圆
        circle = plt.Circle((x, 6.2), 0.5, facecolor=color, alpha=0.85, edgecolor='white', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, 6.2, icon, fontsize=20, ha='center', va='center')

        ax.text(x, 5.3, role, fontsize=15, fontweight='bold', color='white', ha='center')
        ax.text(x, 4.9, subtitle, fontsize=10, color=color, ha='center')

        # 技能列表
        for j, skill in enumerate(skills):
            y = 4.2 - j * 0.65
            skill_rect = FancyBboxPatch((x - 1.2, y - 0.2), 2.4, 0.4, boxstyle="round,pad=0.05",
                                        facecolor=color, alpha=0.3, edgecolor='none')
            ax.add_patch(skill_rect)
            ax.text(x, y, skill, fontsize=10, color='white', ha='center', va='center')

    save(fig, 'chart_persona_matrix.png')


if __name__ == "__main__":
    print("=" * 50)
    print("HydroClaw 专业图表生成器")
    print("=" * 50)

    chart_01_architecture_pyramid()
    chart_02_seven_engines()
    chart_03_skill_hierarchy()
    chart_04_cognitive_flow()
    chart_05_comparison()
    chart_06_kpi_dashboard()
    chart_07_component_tree()
    chart_08_timeline()
    chart_09_rule_layers()
    chart_10_persona_matrix()

    print(f"\n✅ 全部10张图表已生成到 {OUT}")
