#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HydroClaw 发布会PPT - 高质量图片提示词清单 (Nano Banana Pro)
共35张AI生成图片，用于80页发布会PPT

使用方法:
  1. API可用后运行: python generate_images_nanobanana.py
  2. 图片输出到: 发布会26.4/images/generated/
  3. PPT生成器会自动检测并嵌入
"""

# 所有图片统一输出到 generated/ 子目录
# PPT中图片不存在时显示占位符（深色卡片+文字说明）

PROMPTS = [
    # ═══════════════════════════════════════════
    # 第一组: 封面与总览 (4张)
    # ═══════════════════════════════════════════
    {
        "id": "G01",
        "name": "cover_hero.png",
        "section": "封面",
        "prompt": (
            "A breathtaking futuristic water network intelligent command center, "
            "dark navy blue technology background (#0D1B2A), massive holographic 3D display "
            "showing interconnected water infrastructure — rivers, dams, reservoirs, pumping stations, "
            "canals, and pipelines — all connected by luminous blue data streams and neural network lines, "
            "a translucent AI brain overlaying the network, floating data dashboards with charts and metrics, "
            "clean minimalist design, cinematic volumetric lighting, depth of field, 8K ultra quality, "
            "professional keynote presentation hero image, no text, 16:9 aspect ratio"
        ),
    },
    {
        "id": "G02",
        "name": "three_layer_overview.png",
        "section": "产品架构",
        "prompt": (
            "A stunning 3D isometric technology architecture diagram with three distinct floating layers "
            "connected by glowing data pipelines, on a dark navy background: "
            "Bottom layer (cyan glow): 'HydroOS' — server racks, GPU clusters, database cylinders, Ray computing nodes; "
            "Middle layer (blue glow): 'HydroMAS' — interconnected AI agent icons, brain neural networks, skill cards; "
            "Top layer (white glow): 'HydroTouch' — multiple device screens (laptop, phone, tablet, AR glasses, smartwatch); "
            "glowing particle streams flowing between layers, futuristic holographic style, "
            "professional tech infographic, clean flat design, 16:9, no text"
        ),
    },
    {
        "id": "G03",
        "name": "product_matrix_6editions.png",
        "section": "产品矩阵",
        "prompt": (
            "Six futuristic product cards arranged in a 2x3 grid on dark background, "
            "each card glowing with different accent color and icon: "
            "Personal (blue, person icon), Mobile (green, phone icon), "
            "Education (purple, graduation cap), Research (orange, microscope), "
            "Design (cyan, blueprint), Operations (red, control panel), "
            "holographic card style with glass morphism effect, tech startup product showcase, "
            "clean modern UI design, 16:9, no text labels"
        ),
    },
    {
        "id": "G04",
        "name": "vision_smart_water.png",
        "section": "愿景",
        "prompt": (
            "A panoramic futuristic smart city water management scene, bird's eye view: "
            "crystal clear rivers flowing through a modern city, underground pipe network visible as "
            "glowing blue X-ray overlay, smart sensors on bridges and dams with data holographics, "
            "AI drones monitoring water quality, digital twin overlay showing real-time flow data, "
            "lush green parks with recycled water fountains, sunrise golden hour lighting, "
            "photorealistic rendering, utopian clean technology aesthetic, 16:9, no text"
        ),
    },

    # ═══════════════════════════════════════════
    # 第二组: 五层架构深入 (5张)
    # ═══════════════════════════════════════════
    {
        "id": "G05",
        "name": "five_layer_pyramid.png",
        "section": "五层架构",
        "prompt": (
            "A five-layer luminous pyramid floating in dark space, each layer glowing differently: "
            "L0 bottom (amber): data sensors and perception icons, wave patterns; "
            "L1 (green): distributed computing nodes, Ray cluster hexagons; "
            "L2 (cyan): MCP tool modules, API connectors, 21 small hexagonal tool icons; "
            "L3 (blue): skill workflow cards, 17 interconnected process chains; "
            "L4 top (white/gold): AI brain with 15 agent avatars orbiting; "
            "holographic data streams flowing upward between layers, "
            "futuristic tech infographic style, dark background, 16:9, no text"
        ),
    },
    {
        "id": "G06",
        "name": "l0_core_algorithms.png",
        "section": "L0 核心算法",
        "prompt": (
            "A futuristic laboratory scene showing 14 algorithm modules as glowing holographic cubes "
            "arranged on a curved display: simulation (water tank ODE), control (PID/MPC graphs), "
            "prediction (time series charts), scheduling (Gantt bars), optimization (gradient descent), "
            "identification (ARX model), water balance (flow diagram), evaporation (cooling tower), "
            "leak detection (pipe network with red alert), data cleaning (filter waves), "
            "dark navy background, each cube with different accent color, neon glow effects, "
            "professional scientific visualization, 16:9, no text"
        ),
    },
    {
        "id": "G07",
        "name": "l1_ray_distributed.png",
        "section": "L1 分布式计算",
        "prompt": (
            "A visualization of distributed computing: a central Ray cluster hub radiating connections "
            "to dozens of worker nodes arranged in concentric rings, each node processing different tasks — "
            "simulation (blue), optimization (green), data cleaning (orange), ML training (purple), "
            "GPU acceleration particles streaming between nodes, real-time task dashboard floating above, "
            "dark background with grid lines, futuristic data center aesthetic, "
            "technology illustration, 16:9, no text"
        ),
    },
    {
        "id": "G08",
        "name": "l2_mcp_servers.png",
        "section": "L2 MCP服务",
        "prompt": (
            "21 hexagonal MCP server modules arranged in a honeycomb pattern, each with unique icon and color: "
            "simulation (blue wave), control (green dial), prediction (orange chart), "
            "scheduling (yellow calendar), evaluation (purple gauge), design (cyan ruler), "
            "water balance (aqua scale), evaporation (red steam), leak detection (crimson alert), "
            "reuse (green recycle), hydrology runoff/routing/calibration/precipitation (earth tones), "
            "hydraulic 1D/2D (steel blue), assimilation/ML (violet), "
            "all connected by thin luminous lines, dark background, professional infographic, 16:9, no text"
        ),
    },
    {
        "id": "G09",
        "name": "l4_multi_agent.png",
        "section": "L4 多智能体",
        "prompt": (
            "15 AI agent avatars arranged in three groups orbiting a central orchestrator brain: "
            "Group 1 (blue, 7 agents): domain specialists — planning, analysis, report, safety, LLM, RL dispatch, orchestrator; "
            "Group 2 (green, 4 agents): DevOps — planner, reviewer, tester, orchestrator; "
            "Group 3 (purple, 4 agents): Content — planner, reviewer, publisher, orchestrator; "
            "each agent is a glowing holographic face/icon with connecting message streams, "
            "message bus as a luminous ring connecting all, dark navy background, "
            "futuristic AI team collaboration visualization, 16:9, no text"
        ),
    },

    # ═══════════════════════════════════════════
    # 第三组: 认知智能核心 (5张)
    # ═══════════════════════════════════════════
    {
        "id": "G10",
        "name": "cognitive_decision_flow.png",
        "section": "认知决策",
        "prompt": (
            "A horizontal 5-step cognitive decision pipeline flowing left to right: "
            "Step 1: Intent Understanding (ear icon, speech wave), "
            "Step 2: Skill Matching (puzzle pieces connecting), "
            "Step 3: Rule Loading (5-layer stack, safety lock on bottom), "
            "Step 4: Engine Execution (gears turning, computation), "
            "Step 5: Template Rendering (document with charts forming), "
            "each step is a glowing hexagonal node connected by luminous arrows, "
            "dark background, futuristic tech dashboard style, neon blue/cyan palette, 16:9, no text"
        ),
    },
    {
        "id": "G11",
        "name": "five_layer_rules.png",
        "section": "五层规则",
        "prompt": (
            "A vertical stack of 5 translucent rule layers, top-down inheritance visualization: "
            "L0 (red, locked): Safety baseline — shield with lock icon, cannot be overridden; "
            "L1 (orange): Skill rules — role-tagged rule cards; "
            "L2 (yellow): Product rules — edition-specific configurations; "
            "L3 (green): Scenario rules — context-dependent overrides; "
            "L4 (blue): Case parameters — user-customizable settings; "
            "downward arrows showing inheritance flow, override markers at each level, "
            "dark background, layered glass card design, tech infographic, 16:9, no text"
        ),
    },
    {
        "id": "G12",
        "name": "skill_hierarchy_s0s1s2.png",
        "section": "技能体系",
        "prompt": (
            "A tree/hierarchy visualization showing three tiers of skills: "
            "Bottom (many small cyan dots): S0 Atomic Skills — 35 atomic operations in clusters; "
            "Middle (medium orange nodes): S1 Composite Skills — 15 workflow combinations; "
            "Top (large blue spheres): S2 Workflow Skills — 6 complete processes (四预, SIL, HIL, MBD, Emergency, Education); "
            "connecting lines showing composition relationships, "
            "dark background, particle effects, professional skill taxonomy visualization, 16:9, no text"
        ),
    },
    {
        "id": "G13",
        "name": "intent_router_brain.png",
        "section": "意图路由",
        "prompt": (
            "A large translucent AI brain in the center receiving speech bubbles from the left side "
            "(natural language queries in various forms), processing through visible neural pathways, "
            "and routing to different skill cards on the right side. "
            "Inside the brain: rule matching (60%), LLM understanding (30%), hybrid (10%) zones visible. "
            "Speech bubbles on left, skill cards on right connected by glowing pathways, "
            "dark navy background, neural network visualization, 16:9, no text"
        ),
    },
    {
        "id": "G14",
        "name": "template_24_grid.png",
        "section": "模板体系",
        "prompt": (
            "A grid of 24 response template cards arranged in 4 rows of 6, organized by CHS theory categories: "
            "Row 1 (blue): Status templates — gauges, dashboards, real-time displays; "
            "Row 2 (green): Analysis templates — charts, diagnostics, comparisons; "
            "Row 3 (orange): Decision templates — recommendations, trade-offs, plans; "
            "Row 4 (red): Control templates — commands, schedules, actions; "
            "each card has a tiny preview of its output format, glass morphism style, "
            "dark background, professional UI component library showcase, 16:9, no text"
        ),
    },

    # ═══════════════════════════════════════════
    # 第四组: 多端接入 HydroTouch (4张)
    # ═══════════════════════════════════════════
    {
        "id": "G15",
        "name": "hydrotouch_multidevice.png",
        "section": "多端接入",
        "prompt": (
            "A stunning multi-device showcase: a large desktop monitor showing a water network dashboard, "
            "a laptop with 3D pipeline visualization, a tablet with real-time charts, "
            "a smartphone with alert notifications, a smartwatch with emergency vibration alert, "
            "and AR glasses showing dam inspection overlay — all displaying the same water network data "
            "in device-appropriate formats, devices arranged in a semicircle on a reflective dark surface, "
            "unified blue accent theme, product photography lighting, 16:9, no text"
        ),
    },
    {
        "id": "G16",
        "name": "hydrodesktop_tauri.png",
        "section": "桌面端",
        "prompt": (
            "A sleek desktop application interface screenshot in dark theme: "
            "left sidebar with navigation (scenarios, models, knowledge), "
            "main area showing a water network topology graph with live data overlays, "
            "right panel with AI chat assistant conversation, "
            "bottom panel with computation progress bars, "
            "floating modal showing simulation results with ECharts, "
            "modern Tauri/React design language, glass morphism cards, 16:9"
        ),
    },
    {
        "id": "G17",
        "name": "ar_dam_inspection.png",
        "section": "AR巡检",
        "prompt": (
            "First-person view through AR smart glasses during a dam inspection: "
            "physical concrete dam structure visible with digital overlay — "
            "real-time water level gauge floating next to the dam, "
            "structural stress heatmap overlaid on the dam surface, "
            "AI assistant dialog box suggesting 'structural integrity: 98%, recommend next check in 30 days', "
            "sensor data panels floating in space, "
            "mixed reality aesthetic, photorealistic dam with holographic overlays, 16:9, no text"
        ),
    },
    {
        "id": "G18",
        "name": "feishu_integration.png",
        "section": "飞书集成",
        "prompt": (
            "A split-screen showing enterprise collaboration integration: "
            "left side shows a team chat interface with an AI bot sending water balance alert cards, "
            "center shows a spreadsheet/database with real-time water network KPIs, "
            "right side shows an approval workflow for dispatch decisions, "
            "all connected by flowing data lines to a central HydroMAS brain icon at the top, "
            "modern enterprise SaaS UI design, light theme with blue accents, 16:9, no text"
        ),
    },

    # ═══════════════════════════════════════════
    # 第五组: 核心应用场景 (6张)
    # ═══════════════════════════════════════════
    {
        "id": "G19",
        "name": "four_prediction_loop.png",
        "section": "四预闭环",
        "prompt": (
            "A circular workflow diagram showing the '四预' (Four Predictions) closed loop: "
            "Forecast (预报, blue radar/chart icon) → Warning (预警, orange alarm bell) → "
            "Rehearsal (预演, green simulation sandbox) → Plan (预案, red action checklist), "
            "arrows flowing clockwise, each node is a large glowing hexagon with icon, "
            "center hub shows 'AI Decision Engine', "
            "data streams and feedback loops visible, dark background, neon glow, 16:9, no text"
        ),
    },
    {
        "id": "G20",
        "name": "digital_twin_water_network.png",
        "section": "数字孪生",
        "prompt": (
            "A photorealistic water distribution network rendered as a digital twin: "
            "physical infrastructure (reservoirs, canals, pump stations, pipelines) shown as "
            "transparent holographic 3D models with real-time data overlays — "
            "water flow visualized as glowing blue particles moving through pipes, "
            "floating dashboards showing pressure, flow rate, and water level at each node, "
            "a control room operator silhouette viewing the holographic display, "
            "cinematic dark lighting with blue/cyan accent, 16:9, no text"
        ),
    },
    {
        "id": "G21",
        "name": "leak_detection_gnn.png",
        "section": "泄漏检测",
        "prompt": (
            "A graph neural network visualization overlaid on a pipe network diagram: "
            "network nodes as circles connected by pipe edges, "
            "GAT attention weights shown as varying edge thickness/glow, "
            "one pipe segment highlighted in red with pulsing alert — leak detected, "
            "acoustic sensor data waveforms floating near the leak point, "
            "AI confidence percentage display, "
            "dark background, cyberpunk data visualization aesthetic, 16:9, no text"
        ),
    },
    {
        "id": "G22",
        "name": "alumina_plant_overview.png",
        "section": "氧化铝案例",
        "prompt": (
            "An aerial view of an alumina processing plant with water network overlay: "
            "12+ workshop nodes connected by pipes, cooling towers with visible steam/evaporation, "
            "water intake from river (7,800 m³/d) and flood channel (2,600 m³/d), "
            "digital data overlay showing water balance at each node, "
            "evaporation loss indicators, reuse water flow in green, "
            "industrial engineering meets futuristic digital twin aesthetic, 16:9, no text"
        ),
    },
    {
        "id": "G23",
        "name": "dispatch_center_dashboard.png",
        "section": "调度中心",
        "prompt": (
            "A modern water network dispatch center control room: "
            "massive curved LED wall showing water network topology with 12 node statuses "
            "(green=normal, yellow=warning, red=alert), "
            "water balance dashboard (intake 10,400, evaporation 4,200, reuse 3,100), "
            "AI dispatch recommendations panel, alert list with timestamps, "
            "operator silhouettes at workstations, "
            "dark room with blue ambient glow, cinematic control room aesthetic, 16:9, no text"
        ),
    },
    {
        "id": "G24",
        "name": "mobile_field_inspection.png",
        "section": "现场运维",
        "prompt": (
            "A field maintenance worker holding a smartphone showing a water network inspection app: "
            "checklist with completed/pending items, AI assistant chat bubble suggesting diagnosis, "
            "the worker stands next to a cooling tower in an industrial setting, "
            "AR overlay visible on the phone screen showing equipment data, "
            "professional industrial photography, warm daylight, safety helmet and vest, 16:9, no text"
        ),
    },

    # ═══════════════════════════════════════════
    # 第六组: 技术深度 (4张)
    # ═══════════════════════════════════════════
    {
        "id": "G25",
        "name": "knowledge_graph_chs.png",
        "section": "知识图谱",
        "prompt": (
            "A beautiful 3D knowledge graph visualization: 190+ nodes of different sizes and colors "
            "connected by 354 edges across 19 domains — hydrology (blue), hydraulics (cyan), "
            "water environment (green), cybernetics (orange), methods (purple), applications (red), "
            "central hub node labeled concept, radiating outward in force-directed layout, "
            "nodes glow and pulse, edges show relationship types, "
            "dark background, network science visualization, 16:9, no text"
        ),
    },
    {
        "id": "G26",
        "name": "rag_search_pipeline.png",
        "section": "RAG检索",
        "prompt": (
            "A pipeline visualization showing RAG (Retrieval Augmented Generation) process: "
            "left: user question bubble → center: TF-IDF search engine scanning through book pages "
            "and knowledge base documents → vector matching visualization → "
            "right: AI brain synthesizing retrieved chunks into a coherent answer, "
            "book icons, document cards, vector space dots, neural network, "
            "dark background, information retrieval infographic, 16:9, no text"
        ),
    },
    {
        "id": "G27",
        "name": "security_compliance.png",
        "section": "安全合规",
        "prompt": (
            "A layered security architecture visualization: "
            "outer ring: OIDC/OAuth2.0 authentication gateway with shield icons, "
            "second ring: RBAC with 5 role badges (operator, designer, researcher, admin, teacher), "
            "third ring: SM2/SM3/SM4 national cryptography chain links, "
            "center: protected water network data core, "
            "compliance badges floating: 'Level 3 Security', 'Xinchuang Compatible', "
            "dark background, cybersecurity aesthetic, 16:9, no text"
        ),
    },
    {
        "id": "G28",
        "name": "edge_computing_deploy.png",
        "section": "边缘部署",
        "prompt": (
            "A deployment architecture showing cloud-edge collaboration: "
            "top: university data center with GPU server racks (training, heavy simulation), "
            "center: network connections (campus LAN, VPN, internet), "
            "bottom: edge devices at water stations — small server boxes (Lanmao LC-03), "
            "AI inference modules (Jetson), IoT sensors, "
            "data flowing between cloud and edge with sync arrows, "
            "dark background, cloud infrastructure diagram, professional IT, 16:9, no text"
        ),
    },

    # ═══════════════════════════════════════════
    # 第七组: 用户角色与场景 (4张)
    # ═══════════════════════════════════════════
    {
        "id": "G29",
        "name": "persona_researcher.png",
        "section": "科研人员",
        "prompt": (
            "A researcher/professor in a modern office with multiple screens: "
            "one screen showing simulation results (PID vs MPC comparison charts), "
            "another showing a paper draft being written with AI assistance, "
            "a third showing test results (1851 tests passed), "
            "books and papers on the desk, water engineering diagrams on the wall, "
            "warm lighting, academic atmosphere, professional portrait photography, 16:9, no text"
        ),
    },
    {
        "id": "G30",
        "name": "persona_designer.png",
        "section": "设计人员",
        "prompt": (
            "A design engineer at a workstation with dual monitors: "
            "one screen showing a water network 3D CAD model with pipe routing, "
            "another showing HydroMAS design calculation results and equipment sizing tables, "
            "physical blueprints and technical standards (GB codes) on the desk, "
            "approval workflow visible on tablet, "
            "professional engineering office, focused concentration, 16:9, no text"
        ),
    },
    {
        "id": "G31",
        "name": "persona_operator.png",
        "section": "运维人员",
        "prompt": (
            "A water network operator in a control room monitoring real-time dashboards: "
            "large screen showing water network status with green/yellow/red indicators, "
            "secondary screen with AI chatbot suggesting dispatch adjustments, "
            "phone showing alert notification from Feishu, "
            "professional control room environment, blue ambient lighting, 16:9, no text"
        ),
    },
    {
        "id": "G32",
        "name": "persona_student.png",
        "section": "教学场景",
        "prompt": (
            "A university classroom/lab scene: students at computer workstations running "
            "water network simulations with HydroMAS educational version, "
            "professor's large screen showing a coupled tank control experiment, "
            "one student's screen showing interactive AI tutor helping debug code, "
            "another student's screen showing real-time sensor data from a physical tank model, "
            "modern STEM lab aesthetic, bright academic environment, 16:9, no text"
        ),
    },

    # ═══════════════════════════════════════════
    # 第八组: 路线图与展望 (3张)
    # ═══════════════════════════════════════════
    {
        "id": "G33",
        "name": "roadmap_phases.png",
        "section": "发展路线",
        "prompt": (
            "A horizontal timeline infographic showing 5 development phases: "
            "Phase A (blue, now): MVP Core — icons of MCP servers, agents, web frontend; "
            "Phase B (green, 3-6mo): Desktop + Mobile — Tauri, Flutter, Gateway icons; "
            "Phase C (orange, 6-9mo): Multi-device Sync — CRDTs, HarmonyOS, edge computing; "
            "Phase D (purple, 9-12mo): IoT Frontier — smartwatch, AR glasses, voice terminal; "
            "Phase E (gold, 12-18mo): Scale + Commercialize — SaaS, marketplace, certification; "
            "ascending curve connecting phases, milestone markers, "
            "dark background, modern business roadmap design, 16:9, no text"
        ),
    },
    {
        "id": "G34",
        "name": "self_evolution_flywheel.png",
        "section": "自进化",
        "prompt": (
            "A perpetual flywheel/cycle diagram showing AI self-evolution: "
            "User Interaction (chat icon) → Interaction Logging (database icon) → "
            "Evolution Analysis (magnifying glass on patterns) → "
            "Auto Development (code generation, Claude Code icon) → "
            "Testing Gate (pytest checkmark) → Deployment (rocket) → "
            "back to User Interaction, "
            "flywheel spinning with motion blur, energy accumulating in the center, "
            "dark background, dynamic motion graphics style, 16:9, no text"
        ),
    },
    {
        "id": "G35",
        "name": "closing_vision.png",
        "section": "结语",
        "prompt": (
            "An inspiring panoramic scene: a vast smart water network spanning mountains, "
            "rivers, cities, and farmlands, all connected by a luminous intelligent grid. "
            "Clean rivers, efficient dams, smart sensors everywhere. "
            "In the sky, a constellation of AI nodes forms a guardian network. "
            "Golden sunrise over the horizon, hopeful and visionary. "
            "The future of water management: intelligent, autonomous, sustainable. "
            "Photorealistic landscape with digital overlay, epic cinematic wide shot, 16:9, no text"
        ),
    },
]


def get_prompt_by_id(prompt_id):
    """按ID获取提示词"""
    for p in PROMPTS:
        if p["id"] == prompt_id:
            return p
    return None


def get_prompts_by_section(section):
    """按章节获取提示词"""
    return [p for p in PROMPTS if p["section"] == section]


def print_summary():
    """打印提示词清单摘要"""
    print(f"{'='*70}")
    print(f"HydroClaw PPT 图片提示词清单 — 共 {len(PROMPTS)} 张")
    print(f"{'='*70}")
    sections = {}
    for p in PROMPTS:
        sections.setdefault(p["section"], []).append(p)
    for sec, items in sections.items():
        print(f"\n  [{sec}] ({len(items)}张)")
        for item in items:
            print(f"    {item['id']}: {item['name']}")
    print(f"\n{'='*70}")


if __name__ == "__main__":
    print_summary()
