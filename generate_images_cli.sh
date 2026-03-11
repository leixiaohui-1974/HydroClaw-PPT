#!/bin/bash
# 使用gemini CLI生成HydroClaw PPT图表

cd /d/cowork/ppt/nano_diagrams

echo "=========================================="
echo "HydroClaw PPT 图表生成器 (Gemini CLI)"
echo "=========================================="

# 图表1: 四层架构金字塔
echo ""
echo "生成图表1: 四层架构金字塔..."
gemini -m "gemini-3-pro-image" -p "Create a professional 4-layer architecture pyramid diagram for HydroClaw intelligent water network system. Isometric pyramid view with 4 horizontal layers stacked from bottom to top. Layer 4 (bottom, cyan gradient): Object Layer with component icons (pipe, pump, node, link, topology). Layer 3 (green gradient): Computing Engine Layer with 7 small engine icons (prediction, optimization, simulation, learning, verification, visualization, reporting). Layer 2 (orange gradient): Skill Orchestration Layer with workflow icons (atomic skill, composite skill, process skill with inheritance arrows). Layer 1 (top, purple gradient): Cognitive Decision Layer with AI brain icon and rule engine icon. Modern flat design, white background, professional business presentation style, clear visual hierarchy, minimalist, 16:9 aspect ratio, high quality. Save as architecture_pyramid.png"

# 图表2: 对比图
echo ""
echo "生成图表2: 对比图表..."
gemini -m "gemini-3-pro-image" -p "Create a professional comparison bar chart showing 'Traditional Method vs HydroClaw'. Horizontal grouped bar chart with 4 metrics on Y-axis: Design Efficiency, Accuracy, Explainability, Learning Cost. Traditional Method (gray bars #CCCCCC): 30%, 60%, 40%, 80%. HydroClaw (blue bars #5B9BD5): 90%, 95%, 85%, 30%. Clean modern business chart, white background, grid lines, clear labels in Chinese and English, professional color scheme, data labels on bars, legend in top right. 16:9 aspect ratio. Save as comparison_chart.png"

# 图表3: 决策流程
echo ""
echo "生成图表3: 决策流程图..."
gemini -m "gemini-3-pro-image" -p "Create a professional horizontal workflow diagram showing HydroClaw decision process. 6 circular nodes connected by arrows from left to right: 'User Input' (blue circle), 'Intent Understanding' (orange circle), 'Solution Generation' (blue circle), 'Rule Verification' (orange circle), 'Optimization' (blue circle), 'Result Output' (orange circle). Gray curved arrows with arrowheads connecting each node. Modern flat design, white background, clean typography, professional business presentation quality, minimalist. 16:9 aspect ratio. Save as decision_flow.png"

# 图表4: KPI效果
echo ""
echo "生成图表4: KPI效果展示..."
gemini -m "gemini-3-pro-image" -p "Create a professional 2x2 grid dashboard showing 4 key performance indicators. Card 1 (top-left): Large number '15%' in blue (#5B9BD5), label below 'Energy Reduction'. Card 2 (top-right): Large number '3-5x' in green (#4CAF50), label below 'Efficiency Improvement'. Card 3 (bottom-left): Large number '30%' in orange (#FF7043), label below 'Leakage Reduction'. Card 4 (bottom-right): Large number '70%' in yellow (#FFC000), label below 'Training Time Reduction'. Clean modern dashboard, white background, subtle card shadows, large bold numbers, bilingual labels (Chinese and English), professional business presentation quality. 16:9 aspect ratio. Save as kpi_metrics.png"

echo ""
echo "=========================================="
echo "图表生成完成！"
echo "请检查 nano_diagrams 目录"
echo "=========================================="
