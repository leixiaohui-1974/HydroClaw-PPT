# HydroClaw 认知智能体系完整方案

# Cognitive AI Architecture for Autonomous Water Network Operations

---

## 一、设计哲学

三句话概括整个方案：

1. **确定性的事用规则，不确定性的事用大模型，大模型的输出用规则兜底**
2. **用户选了什么Skill就具备什么角色，行为即身份**
3. **引擎通用不分领域，差异全在元件和参数**
4. **物理元件、水文元件、模型元件统一基类，混合组装任意水网**

---

## 二、总体架构：四层

```
┌─────────────────────────────────────────────────────────────┐
│  ①  认知决策层                                               │
│      大模型 + 规则引擎 + 模板渲染                             │
│      "理解意图、选择Skill、约束行为、格式化输出"               │
├─────────────────────────────────────────────────────────────┤
│  ②  技能编排层                                               │
│      Skill体系（原子→组合→流程）                              │
│      "知道做什么、按什么顺序、怎么解读结果"                    │
├─────────────────────────────────────────────────────────────┤
│  ③  计算引擎层                                               │
│      七大通用引擎（仿真/辨识/调度/控制/优化/预测/学习）          │
│      + 工具箱（数据处理/曲线拟合/统计/诊断/水力计算/...）       │
│      "怎么算——与领域无关的纯算法和公共工具"                    │
├─────────────────────────────────────────────────────────────┤
│  ④  对象层                                                    │
│      三族元件库（物理/水文/模型）+ 水网组装 + 外部工具接入       │
│      "算什么——具体的元件实例和工程系统"                        │
└─────────────────────────────────────────────────────────────┘
```

四层之间的调用关系是单向的：①调②，②调③，③驱动④。每层只依赖下一层的统一接口，不感知内部实现。

---

## 三、第①层：认知决策

### 3.1 大模型与规则的分工

```
规则引擎处理（~60%交互）      大模型处理（~30%交互）        大模型主导+规则兜底（~10%）
确定性场景                    需要理解和推理               开放性问题
━━━━━━━━━━━━━━━━              ━━━━━━━━━━━━━━━━             ━━━━━━━━━━━━━━━━━
查询闸门当前水位              分析工况并推荐方案            未预见的异常工况
执行标准巡检流程              设计方案比选                  科研探索性讨论
ODD阈值判别                   跨域关联分析                  应急情况类比推理
预警等级确定                  可解释性生成                  创新性方案构想
```

### 3.2 规则体系：五层继承

规则不是从"角色声明"触发，而是从"Skill选择"自动加载：

```
L0  安全底线（不可覆盖）
    物理守恒 / 安全约束只紧不松 / 不编造数据 / 不确定性必须声明
    ↓ 始终加载
L1  Skill携带的角色规则（自动加载）
    用户选"断面优化"Skill → 自动加载设计规则（规范遵从、安全系数、变更追溯）
    用户选"ODD预警"Skill  → 自动加载运维规则（指令遵从、异常上报、预演验证）
    用户选"仿真对比"Skill → 自动加载科研规则（方法透明、对比分析、可复现）
    用户选"教学实验"Skill → 自动加载教学规则（苏格拉底引导、试错鼓励）
    ↓ 按Skill标签加载
L2  产品规则
    SIL平台：测试环境与生产隔离 / 通过不等于现场可行
    MBD设计器：V模型流程不可跳过 / 设计文档完整性
    HydroClaw交互：涉及操作二次确认 / 群聊信息脱敏
    ↓ 按当前产品加载
L3  场景规则
    实时控制：决策延迟不超过控制周期 / 物理预演校验
    设计优化：必须与基准方案对比 / 权衡分析
    应急响应：优先级自动切换 / 保守策略 / 同步通知领导
    教学实验：安全环境 / 允许试错 / 自动评估
    ↓ 按业务场景加载
L4  案例参数
    中线工程：冰期Fr≤0.06 / 水位变化率≤0.3m/h
    胶东调水：泵站群启动先下游后上游
    双容水箱：溢流口高度 / 映射知识点
    ↓ 按工程案例加载
```

**核心简化**：用户不需要声明角色，不需要切换模式。选Skill就自动获得对应的规则约束、回复深度和术语风格。一个用户上午用"仿真对比"（科研模式），下午用"ODD预警"（运维模式），系统自动切换，无缝衔接。

### 3.3 回复模板：24个模板覆盖全场景

基于CHS六要素（Plant-Actuator-Sensor-Disturbance-Constraint-Objective），通过继承组合避免模板爆炸：

```
T0（六要素基类）
├── T0-S 状态查询    T0-A 分析诊断    T0-D 决策建议     ← 3个原子模板
│
├── T1 执行器类（闸泵阀水轮机）                         ← 3个子模板
│   T1.status / T1.diagnosis / T1.control
├── T2 蓄水体类（库湖池）                               ← 2个子模板
│   T2.status / T2.prediction
├── T3 输水体类（河沟渠）                               ← 2个子模板
│   T3.status / T3.simulation
│
├── B1预报 B2预警 B3预演 B4预案 B5-SIL B6-HIL           ← 6个业务模板
│   （组合引用T1/T2/T3的子模板）
│
└── W1四预闭环 W2-SIL验证 W3-HIL验证                    ← 6个工作流模板
    W4-MBD全流程 W5应急响应 W6教学实验
    （编排B模板的有序序列）

模板总数 = 4 + 7 + 6 + 6 = 23个
角色适配：不增加模板，用修饰器调整同一模板的输出深度和术语
案例适配：不增加模板，用L4参数填充具体数值
```

**同一个B2预警模板，不同Skill上下文自动调整输出**：

运维Skill触发 → 简洁步骤式："⚠️渠池2水位42.35m超限，立即上报L1"

科研Skill触发 → 深度分析："Saint-Venant分析显示上游闸门调整后波前传播时间约45min，当前状态为积分饱和特征，参见Malaterre(2004)..."

### 3.4 认知决策的五步流程

每次用户交互，认知层执行固定的五步：

```
用户输入
  ↓
Step 1: 意图理解 — 大模型解析用户想做什么
  ↓
Step 2: Skill匹配 — 规则引擎+大模型确定调哪个Skill
  ↓
Step 3: 规则加载 — 根据Skill标签自动加载L1-L4规则集
  ↓
Step 4: Skill执行 — 调用技能编排层（见第④层）
  ↓
Step 5: 模板渲染 — 用对应模板格式化结果，用角色修饰器调整深度
  ↓
输出
```

---

## 四、第②层：技能编排

### 4.1 Skill三层继承

```
S0 原子Skill（~25个）
│  一个Skill封装一个MCP工具调用
│  包含：前置检查 → 参数组装 → 调用 → 结果解读 → ODD关联
│
├── S1 组合Skill（~10个）
│   编排多个S0完成一个业务功能
│   编排逻辑是硬编码的领域知识，不由大模型即兴决定
│
└── S2 流程Skill（~6个）
    编排多个S1完成完整业务流程
    包含人机交互点和最终报告生成
```

### 4.2 原子Skill清单（按引擎分类）

```yaml
仿真类:
  S0-SIM-01: 明渠仿真          S0-SIM-02: 管网仿真
  S0-SIM-03: 水库仿真          S0-SIM-04: 集中参数仿真(水箱)
  S0-SIM-05: 水锤仿真          S0-SIM-06: 冰期仿真

辨识类:
  S0-ID-01: 糙率辨识           S0-ID-02: 泵曲线辨识
  S0-ID-03: 闸系数辨识         S0-ID-04: UKF状态估计
  S0-ID-05: 模型校准

调度类:
  S0-SCH-01: 全局调度优化      S0-SCH-02: 泵站经济运行
  S0-SCH-03: 闸门序列优化      S0-SCH-04: 水平衡核算
  S0-SCH-05: 水库优化调度

控制类:
  S0-CTL-01: PID计算           S0-CTL-02: MPC计算
  S0-CTL-03: DMPC计算          S0-CTL-04: 控制器评估

检测评估类:
  S0-DET-01: ODD检查           S0-DET-02: 泄漏检测
  S0-DET-03: 异常检测          S0-DET-04: WNAL评估
  S0-DET-05: 蒸发计算

预测类:
  S0-PRD-01: 水文预报(概念模型)  S0-PRD-02: 时序预测(LSTM/Transformer)
  S0-PRD-03: 降阶模型预测(IDZ/POD) S0-PRD-04: 图网络预测(GNN)
  S0-PRD-05: 混合预测(物理+数据)

学习类:
  S0-LRN-01: RL策略训练         S0-LRN-02: RL策略部署(在线推断)
  S0-LRN-03: 模仿学习(从专家数据) S0-LRN-04: 在线学习(参数自适应)
  S0-LRN-05: 模型训练管理(训练/验证/版本)

工具类（水网领域常用工具箱——不归属任何引擎，但每天都会用到）:
  # ---- 数据处理 ----
  S0-UTL-01: 数据清洗          # 缺失/跳变/冻结/漂移检测与修复
  S0-UTL-02: 时序重采样        # 不等间距→等间距，多源时间对齐
  S0-UTL-03: 数据质量评估      # 完整率/一致性/可信度评分
  # ---- 统计与拟合 ----
  S0-UTL-04: 曲线拟合          # 泵特性曲线/库容曲线/阻力曲线/率定曲线
  S0-UTL-05: 频率分析          # 洪水频率/暴雨频率/P-III/GEV分布拟合
  S0-UTL-06: 相关性分析        # 变量相关/互信息/格兰杰因果/滞后相关
  S0-UTL-07: 趋势检测          # Mann-Kendall/突变检验/周期分析
  # ---- 诊断与归因 ----
  S0-UTL-08: 运行诊断          # "为什么水位偏高"——多因素归因分析
  S0-UTL-09: 模型诊断          # 仿真vs实测偏差分析，定位模型失准原因
  S0-UTL-10: 设备健康评估      # 泵/闸/阀运行状态趋势，剩余寿命估计
  # ---- 可视化与报告 ----
  S0-UTL-11: 过程线绘图        # 水位/流量/压力等时程曲线自动绘图
  S0-UTL-12: 断面/管网绘图     # 纵剖面图/平面拓扑图/压力等值线
  S0-UTL-13: 报告生成          # 日报/周报/月报/调度总结自动生成
  # ---- 格式转换 ----
  S0-UTL-14: 模型格式转换      # INP↔JSON / HDF5↔CSV / 不同工具格式互转
  S0-UTL-15: 单位换算          # SI↔英制/各种水利工程常用单位
  # ---- 知识查询 ----
  S0-UTL-16: 规范查询          # 检索设计规范条文（RAG）
  S0-UTL-17: 案例检索          # 从历史案例库中检索相似工况/相似设计
  S0-UTL-18: 公式计算器        # 曼宁公式/水头损失/泵相似律/堰流等常用公式
```

### 4.3 组合Skill清单

```yaml
S1-FCST:  预报    = UKF状态估计 → 模型仿真或数据预测 → 不确定性量化
S1-WARN:  预警    = ODD检查 → 趋势预测 → 预警等级判定
S1-RHSL:  预演    = 方案解析 → 闭环仿真 → 约束校核 → 方案排序
S1-PLAN:  预案    = 案例库检索 → 预演验证 → 预案优化
S1-SIL:   SIL测试 = 工况加载 → 闭环仿真×N → 性能评估 → 准入判定
S1-HIL:   HIL测试 = 继承SIL + 硬件连接检查 + SIL-HIL对比
S1-LEAK:  泄漏诊断 = 水平衡 → 异常检测 → 泄漏定位 → 诊断报告
S1-SYSID: 系统辨识 = 数据采集 → 参数辨识 → 模型校准 → 校准验证
S1-CTLD:  控制设计 = 系统建模 → 控制器设计 → SIL验证 → 调参优化
S1-WNAL:  自主等级评估 = ODD覆盖度 → 控制能力 → 综合评估
S1-HYDRO: 水文预报 = 降雨预报→产流计算→汇流演算→入流预测（概念/数据/混合可选）
S1-TRAIN: 模型训练 = 数据准备→模型训练→验证评估→版本管理→部署上线
S1-RLOPT: RL策略优化 = 环境配置→策略训练→SIL评估→与传统方法对比→部署
S1-DIAG:  运行诊断 = 数据清洗→异常检测→多因素归因→模型诊断→诊断报告
S1-DCLN:  数据治理 = 质量评估→清洗修复→重采样对齐→质量看板→归档
S1-REPT:  自动报告 = 数据采集→统计分析→过程线绘图→模板渲染→报告输出
```

### 4.4 流程Skill清单

```yaml
S2-4P:   四预闭环    = S1-FCST → S1-WARN → S1-RHSL → S1-PLAN
S2-SIL:  SIL策略验证  = S1-SIL × 正常区 → S1-SIL × 降级区 → 汇总
S2-HIL:  HIL硬件验证  = S1-HIL × 关键工况 → SIL-HIL对比 → 准入判定
S2-MBD:  MBD全流程   = ODD定义 → S1-CTLD → S1-RHSL → S2-SIL → S2-HIL
S2-EMG:  应急响应    = S1-WARN → S1-PLAN → S1-RHSL → 执行/人工确认
S2-EDU:  教学实验    = 场景配置 → S1-SIL(教学模式) → 自动评估
```

### 4.5 Skill承载角色：四维度×多层级

不只是运维分三级——**每个维度都有层级**，差异在于能看什么、能改什么、需不需要上级确认：

```
运维                教学                  设计              科研
━━━━━━━━━━         ━━━━━━━━━━           ━━━━━━━━          ━━━━━━━━
L2 调度中心         课程负责人/教授       总工/技术总监      PI/博导
   全局决策            课程体系设计          方案审定           方向把控
   制定方案            教学大纲审定          技术决策           课题设计
   审批指令            考核标准制定          规范审查           论文终审

L1 管理段           主讲教师/副教授       专业负责人/主任工   博士生/副研
   段内协调            课堂教学              专业设计            独立研究
   方案执行            实验设计              计算校核            撰写论文
   上报异常            指导毕设              图纸审核            数据分析

L0 现地             助教/实验员           设计员/绘图员       硕士生
   执行指令            辅导答疑              参数计算            辅助计算
   数据采集            设备维护              出图                文献调研
   异常上报            批改作业              资料整理            数据整理
```

**学生作为独立维度，也分层级**——从大专生到研究生，知识基础、培养目标、Skill开放程度差异巨大：

```
学生层级            知识基础                培养目标              Skill开放度
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

S3 研究生           控制论+水力学+编程      独立科研能力          S0全部+S1大部分
   硕士/博士         可做算法开发            方法创新              可自定义工况和参数
                                           论文写作              与researcher_L0/L1重叠

S2 本科生           高数+水力学基础         理解控制原理          S0受限子集+S1教学版
   大三大四          初步编程能力            能做基本仿真实验      不能修改模型参数
                                                                不能自定义极端工况

S1 大专/高职生      水利工程基础            掌握操作技能          操作类S0子集
   水利类专业        基本操作能力            理解安全规程          只能操作预配置场景
                                           持证上岗能力          不能修改任何参数

S0 低年级/科普      基础物理+数学           建立系统概念          演示类Skill（只看）
   通识选修          无专业基础              激发兴趣              不实际操作
```

**同一个"水位控制实验"Skill，四级学生的行为完全不同**：

```yaml
S2-EDU-水位控制实验:

  student_S3:  # 研究生
    scene: "双容水箱 + MPC控制器"
    freedom: "自行设计控制器结构、修改预测步长、对比多种算法"
    guidance: "开放探索，仅在物理约束被违反时提醒"
    evaluation: "算法创新性 + 性能分析深度 + 论文写作质量"
    output: "学术实验报告格式，含数学推导"

  student_S2:  # 本科生
    scene: "双容水箱 + PID控制器"
    freedom: "可调Kp/Ki/Kd参数，观察响应变化"
    guidance: |
      苏格拉底引导：
      "你把Ki调大了，水位开始振荡——
       想想看，积分项在做什么？翻阅教材4.3节'积分饱和'。"
    evaluation: "知识点理解 + 参数整定合理性 + 实验报告规范性"
    output: "标准实验报告格式，关联知识点清单"

  student_S1:  # 大专生
    scene: "双容水箱 + 已配置好的PID（参数固定）"
    freedom: "只能操作启停和设定值切换，不能改控制器参数"
    guidance: |
      步骤式引导：
      "第1步：将1号水箱目标水位设为30cm，点击'启动'
       第2步：观察水位变化曲线，记录调节时间
       第3步：将目标水位改为20cm，观察响应
       问题：水位从30降到20时，经过了几次振荡？"
    evaluation: "操作正确性 + 观察记录完整性 + 基本现象解释"
    output: "操作记录表 + 观察问题回答，不要求数学推导"

  student_S0:  # 低年级/科普
    scene: "双容水箱动画演示（不实际操作）"
    freedom: "只能观看和提问"
    guidance: |
      类比式解释：
      "看这个水箱——想象你在调节淋浴的水温。
       你转热水龙头（这是控制），水温变化（这是响应），
       你感觉到温度（这是反馈）。水箱控制的原理完全一样！"
    output: "概念图 + 生活类比 + 趣味问答"
```

**教师维度也相应三级细化**：

```yaml
teacher_L2（课程负责人/教授）:
  - "设计整门课程的实验体系和知识图谱"
  - "定义各学生层级(S0-S3)的考核标准和Skill可见范围"
  - "审定主讲教师设计的实验方案"
  - "查看全部学生的学习数据分析报告"

teacher_L1（主讲教师/副教授）:
  - "设计单次实验场景参数，预设错误陷阱"
  - "设定单次实验评分标准，查看本班学生数据"
  - "调整实验难度（在课程负责人授权范围内）"

teacher_L0（助教/实验员）:
  - "执行教师配置好的实验方案，辅导学生操作"
  - "批改实验报告（辅助评分），记录设备异常"
  - "不能修改场景参数和评分标准"
```

每个Skill自带`(role, level)`二元标签，同一个Skill对不同层级开放不同操作深度：

```yaml
skill_role_tags:

  # ---- 运维类（三级不变）----
  S0-DET-01: ["operator_L0", "operator_L1", "operator_L2"]
  S1-WARN:   ["operator_L1", "operator_L2"]
  S2-4P:     ["operator_L2"]
  S2-EMG:    ["operator_L1", "operator_L2"]

  # ---- 设计类（三级分层）----
  S0-SIM-*:  ["designer_L0", "designer_L1", "designer_L2"]
  S0-ID-*:   ["designer_L0", "designer_L1", "designer_L2"]
  S1-CTLD:   ["designer_L1", "designer_L2"]     # 设计员不能自行设计控制器
  S2-MBD:    ["designer_L1", "designer_L2"]     # 设计员不能启动全流程
  S2-SIL:    ["designer_L1", "designer_L2"]
  S2-HIL:    ["designer_L2"]                     # 只有总工能批准HIL

  # ---- 教学类（教师三级 + 学生四级）----
  S2-EDU:    ["teacher_L0", "teacher_L1", "teacher_L2",
              "student_S0", "student_S1", "student_S2", "student_S3"]
  # 教师看到的Skill菜单多出"配置场景""设定评分"
  # student_S0只看到"观看演示"，student_S1看到"操作实验"
  # student_S2看到"参数调整实验"，student_S3看到"自主设计实验"

  # 教师专属Skill（学生不可见）
  # "场景配置":   ["teacher_L1", "teacher_L2"]
  # "评分标准":   ["teacher_L1", "teacher_L2"]
  # "课程设计":   ["teacher_L2"]
  # "学生数据":   ["teacher_L0", "teacher_L1", "teacher_L2"]

  # ---- 科研类（三级分层）----
  S0-SIM-*:  ["researcher_L0", "researcher_L1", "researcher_L2"]
  S1-SYSID:  ["researcher_L1", "researcher_L2"]  # 硕士生不能独立做系统辨识
  S1-WNAL:   ["researcher_L2"]                    # 只有PI做自主等级评估

  # ---- 跨维度Skill → 根据上下文消歧 ----
  S0-CTL-02: ["researcher_L1", "designer_L1"]
  # 在设计项目里调用 → 设计规则
  # 独立探索性调用 → 科研规则

  # ---- 工具箱Skill → 所有角色都能用，层级决定深度 ----
  S0-UTL-*:  ["所有角色"]   # 数据清洗、曲线拟合、单位换算——人人需要
  S1-DIAG:   ["operator_L1", "operator_L2", "researcher_L1", "designer_L1"]
  S1-DCLN:   ["所有角色"]   # 数据治理人人需要
  S1-REPT:   ["operator_L1", "operator_L2", "designer_L1", "teacher_L1"]
  # 工具箱的层级差异体现在：
  #   L0用户看到简化版（一键清洗、一键报告）
  #   L1用户看到参数可调版（选清洗策略、选报告模板）
  #   L2用户看到全配置版（自定义规则、自定义模板）
```

**层级决定的不是"能不能用这个Skill"，而是"用这个Skill时能做到什么程度"**：

```yaml
# 以"泵站选型"为例，同一个Skill三个层级的行为差异：
S0-OPT-设备选型:
  designer_L0:  # 设计员
    can_do:   ["按给定参数查泵型手册", "出选型计算书"]
    cannot:   ["修改设计流量", "决定用离心还是轴流"]
    approval: "计算书需L1校核"
    output:   "详细计算过程 + 候选泵型参数表"

  designer_L1:  # 专业负责人
    can_do:   ["泵型比选(离心/轴流/混流)", "变频/工频决策",
               "全工况性能校核", "修改设计参数"]
    cannot:   ["变更设计标准", "跨专业修改管径"]
    approval: "重大选型变更需L2审批"
    output:   "选型报告 + 全工况性能曲线 + 与基准方案对比"

  designer_L2:  # 总工
    can_do:   ["审定选型方案", "跨专业协调(管径↔泵型联动)",
               "决定设计标准", "批准非标方案"]
    approval: "直接批准"
    output:   "决策摘要：关键指标+结论+批示"
```

**用户层级怎么确定**——用户能看到哪些Skill就说明他是什么层级，Skill菜单本身就是权限边界：

```python
def get_visible_skills(user: User) -> List[Skill]:
    """用户看到的Skill列表 = 其权限的直接体现"""
    user_tags = user.role_tags  # 如 ["designer_L1"]
    return [s for s in all_skills
            if any(tag in s.role_tags for tag in user_tags)]

    # designer_L0 看到：仿真、校核、计算书生成
    # designer_L1 看到：上述 + 选型比选、控制设计、SIL测试
    # designer_L2 看到：上述 + HIL测试、MBD全流程、方案审批
    # 层级越高，可见Skill越多
```

---

## 五、第③层：计算引擎

七大引擎是通用的纯算法，不知道自己在算什么水网、服务什么角色。前五个面向物理机理，后两个面向数据和学习——但对Skill层来说调用接口完全统一。另有一套工具箱覆盖日常通用需求：

```yaml
# ---- 物理机理引擎 ----
SimulationEngine:     "解方程 — Saint-Venant/MOC/节点连续性/ODE/产汇流"
IdentificationEngine: "估参数 — 最小二乘/UKF/EnKF/遗传算法/PINN"
SchedulingEngine:     "求最优分配 — LP/MILP/DP/SDDP/多目标"
ControlEngine:        "闭环反馈 — PID/MPC/DMPC/自适应/鲁棒"
OptimizationEngine:   "搜索最优解 — SQP/GA/DE/PSO/贝叶斯/敏感性分析"

# ---- 数据与学习引擎 ----
PredictionEngine:     "预测未来 — LSTM/Transformer/GNN/降阶模型/混合模型"
LearningEngine:       "学习策略 — RL(DQN/PPO/SAC)/模仿学习/在线学习"

# ---- 日常工具箱 ----
UtilityToolkit:       "数据清洗/曲线拟合/频率分析/诊断归因/可视化/报告/单位换算/公式计算"
```

**为什么需要独立的预测引擎和学习引擎，而不是塞进仿真引擎？**

仿真引擎的核心逻辑是"给定方程和初边条件，向前推进时间步"——它需要完整的物理方程。但很多实际场景中：
- 水文预报的输入是降雨场、蒸发、土壤墒情——没有封闭的解析方程，必须用数据驱动或概念性水文模型
- 实时控制中需要在毫秒级给出预测——全物理模型太慢，需要降阶替代模型（IDZ、POD、神经网络代理）
- 调度策略在高维约束空间中搜索——传统优化求解器可能陷入局部最优，RL可以学习全局策略
- 运行工况识别需要从时序数据中提取模式——不是物理推演而是模式识别

这些能力和物理仿真的计算逻辑根本不同，但对Skill层来说只是"另一种后端"。

```python
# 统一接口——Skill不关心调的是物理模型还是数据模型
engine.simulate(network, bc, duration, dt)          → SimulationResult     # 物理仿真
engine.predict(input_features, horizon, model_type)  → PredictionResult    # 数据预测
engine.learn(environment, reward_fn, episodes)       → PolicyResult        # 策略学习

# 同一个预报Skill，可以选不同后端：
S1-FCST（预报）:
  方式A: SimulationEngine + Saint-Venant   → 物理推演（精确但慢）
  方式B: PredictionEngine + LSTM           → 数据预测（快但需训练数据）
  方式C: PredictionEngine + 降阶模型(IDZ)  → 物理降阶（快且保留物理约束）
  方式D: PredictionEngine + 混合模型       → 物理+数据融合（精确且快）
```

### 5.0 预测引擎详述

```yaml
PredictionEngine:
  description: "从历史数据和当前状态预测未来——不依赖完整物理方程"

  model_families:

    # ---- 水文概念模型 ----
    conceptual_hydrology:
      models: ["新安江模型", "Sacramento", "HBV", "GR4J", "TOPMODEL"]
      input:  "降雨、蒸发、温度、土壤参数"
      output: "径流过程线"
      applicable: "流域来水预报、洪水预报"
      特征: "参数少(5-20个)，可辨识，有一定物理含义"

    # ---- 深度学习时序预测 ----
    deep_sequence:
      models: ["LSTM", "GRU", "Transformer", "TFT(Temporal Fusion Transformer)",
               "Informer", "PatchTST"]
      input:  "历史时序 + 协变量（气象/调度/日历）"
      output: "未来N步预测 + 不确定性区间"
      applicable: "需水预测、水位预测、水质预测、负荷预测"
      特征: "需要训练数据，长序列效果好，可量化不确定性"

    # ---- 图神经网络 ----
    graph_network:
      models: ["GCN", "GAT", "GraphSAGE", "STGCN(时空图卷积)"]
      input:  "管网/河网拓扑 + 节点/边特征时序"
      output: "全网状态预测"
      applicable: "管网压力预测、水质扩散预测、泄漏传播分析"
      特征: "天然适合网络结构数据，空间依赖关系建模能力强"

    # ---- 降阶替代模型 ----
    surrogate:
      models: ["IDZ(Integrator-Delay-Zero)", "POD(本征正交分解)",
               "DMD(动态模态分解)", "神经网络代理模型", "PINN"]
      input:  "物理模型的输入输出数据（离线生成）"
      output: "近似物理模型的快速预测"
      applicable: "MPC在线优化中需要快速前向预测的场景"
      特征: |
        保留物理约束（特别是PINN和IDZ）
        比全物理模型快2-3个数量级
        用于替代仿真引擎中的重型求解器做实时控制

    # ---- 物理-数据混合 ----
    hybrid:
      models: ["物理约束神经网络", "残差学习(物理基+数据修正)",
               "嵌入物理的Transformer"]
      input:  "物理模型粗预测 + 实测数据"
      output: "修正后的高精度预测"
      applicable: "物理模型有系统偏差时的在线修正"
      特征: "兼顾物理可解释性和数据适应性——CHS的核心主张"

  unified_interface:
    input:  "{input_features, horizon, model_type, model_id, uncertainty}"
    output: "{predictions, confidence_intervals, model_diagnostics}"
```

### 5.0b 学习引擎详述

```yaml
LearningEngine:
  description: "从交互中学习最优策略——不需要显式目标函数的解析形式"

  method_families:

    # ---- 强化学习 ----
    reinforcement_learning:
      algorithms: ["DQN", "PPO", "SAC", "TD3", "A3C"]
      frameworks: ["Stable-Baselines3", "RLlib", "CleanRL"]
      input:  "状态空间(水网状态) + 动作空间(闸泵控制) + 奖励函数"
      output: "策略π(state→action)"
      applicable: |
        泵站群启停组合优化（离散动作空间）
        闸门群协调调度（连续动作空间）
        应急响应策略学习
        水库长期调度策略
      特征: |
        可以处理传统优化求解器难以处理的大规模离散-连续混合问题
        需要仿真引擎提供训练环境（SIL即RL的训练场）
        策略一旦训练完成，在线执行极快（毫秒级）

    # ---- 模仿学习 ----
    imitation_learning:
      algorithms: ["行为克隆(BC)", "DAgger", "GAIL"]
      input:  "专家调度员的历史操作数据"
      output: "模仿专家行为的策略"
      applicable: "将资深调度员的经验转化为可复用的自动策略"
      特征: "不需要定义奖励函数，直接从人类行为中学习"

    # ---- 在线学习 ----
    online_learning:
      algorithms: ["Contextual Bandit", "在线凸优化", "贝叶斯优化"]
      input:  "实时运行数据流"
      output: "持续更新的参数/策略"
      applicable: "控制器参数在线自适应、需水模式在线追踪"
      特征: "无需离线训练，边运行边学习，适应缓变系统"

  unified_interface:
    input:  "{environment, reward_fn/expert_data, algorithm, config}"
    output: "{policy, training_metrics, evaluation_results}"

  与仿真引擎的关系: |
    学习引擎不替代仿真引擎，而是"寄生"在仿真引擎上训练：
    RL训练循环 = 仿真引擎提供environment.step()
                + 学习引擎更新策略
    SIL平台天然就是RL的训练场
    训练好的策略可以作为控制引擎的一个"控制器类型"使用：
    ControlEngine.control(state, ..., type="rl_policy") → action
```

每个引擎提供统一接口，Skill层不关心内部用哪个求解器：

```python
engine.simulate(network, boundary_conditions, duration, dt)   → SimulationResult
engine.identify(model, observed_data, params_to_identify)     → IdentificationResult
engine.predict(input_features, horizon, model_type)           → PredictionResult
engine.learn(environment, reward_fn, episodes)                → PolicyResult
engine.schedule(objectives, constraints, decision_variables)  → SchedulingResult
engine.control(state, setpoint, model, constraints, type)     → ControlResult
engine.optimize(objective_fn, constraints, variables, bounds)  → OptimizationResult
engine.toolkit.calc_manning(Q, n, slope, ...)                 → CalcResult
```

### 5.1 引擎内部可切换后端

同一个引擎接口，内部可以走自研求解器或外部工具：

```
engine.simulate(city_network)
  │
  ├── 自研HydroOS求解器（默认，自主可控）
  │
  ├── EPANET/WNTR后端（大规模管网，某单位已有标定模型）
  │
  ├── HEC-RAS后端（某流域机构的河道模型）
  │
  ├── PSS/E后端（某电力院的水电模型）
  │
  └── 某课题组的专用模型后端
```

**自研体系是核心**——什么水网都能从零建模计算，不依赖任何外部工具。**外部工具是生态**——各单位、团队手里已有的成熟标定模型，通过标准接口接入，与自研体系并列提供计算能力。科研场景下可以同时调两个后端对比验证。

### 5.2 外部工具生态现状（2026年3月）

水网领域的主流工具正在快速向AI可调用方向演进。以下是可直接集成到HydroClaw体系的工具全景：

**第一梯队：Python原生API，可直接封装为MCP工具（pip install即可）**

```yaml
WNTR:
  领域: "城市供水管网"
  安装: "pip install wntr"
  开发者: "US EPA + Sandia国家实验室"
  能力: |
    纯Python实现的EPANET兼容引擎
    读写EPANET INP文件，支持压力驱动需水(PDD)
    泄漏模拟、韧性分析、灾害场景仿真
    3行代码完成一次管网水力仿真：
      wn = wntr.network.WaterNetworkModel('Net3')
      sim = wntr.sim.EpanetSimulator(wn)
      results = sim.run_sim()
  AI就绪度: "高——纯Python，无外部依赖，可直接在MCP Server中调用"
  集成优先级: "★★★★★ 最高——城市供水场景的核心后端"

PySWMM:
  领域: "城市排水/雨洪管理"
  安装: "pip install pyswmm"
  开发者: "OpenWaterAnalytics / US EPA"
  能力: |
    EPA SWMM的Python运行时接口
    可在仿真过程中逐步长读写参数、注入控制
    已被用于实时控制(RTC)和MPC控制策略开发
    支持CSO管理、洪水模拟、水质追踪
  AI就绪度: "高——运行时控制能力天然适合AI Agent调用"
  集成优先级: "★★★★★ 最高——排水场景的核心后端"

swmm_api:
  领域: "城市排水（模型编辑侧）"
  安装: "pip install swmm-api"
  能力: |
    SWMM模型的完整读写（不只是运行时控制）
    支持模型创建、GIS集成、批量仿真、校准、敏感性分析
    与PySWMM互补：swmm_api管模型编辑，PySWMM管运行时控制
  集成优先级: "★★★★ 高——与PySWMM配合覆盖排水全流程"

ras-commander:
  领域: "河道/防洪/溃坝"
  安装: "pip install ras-commander"
  开发者: "gpt-cmdr（开源社区）"
  能力: |
    HEC-RAS 6.2+的Python自动化API
    HDF5数据直接读取（无需COM接口）
    支持1D/2D仿真、溃坝分析、地形处理
    分布式计算（PsExec/Docker/SSH workers）
  AI就绪度: |
    ★极高——2025年12月更新明确宣布支持"完全agentic工程体验"
    内置agents、skills、rules和认知记忆系统
    采用分层知识结构+渐进式信息披露+人在回路
    设计理念与HydroClaw高度一致，可直接参考其agent架构
  集成优先级: "★★★★★ 最高——河道防洪场景首选，且agent设计经验可借鉴"

FloPy:
  领域: "地下水"
  安装: "pip install flopy"
  开发者: "USGS"
  能力: "MODFLOW地下水模型的Python接口，模型构建/运行/后处理"
  集成优先级: "★★★ 中——地下水场景需求时接入"

Pyomo:
  领域: "通用优化求解"
  安装: "pip install pyomo"
  状态: "已在HydroOS中集成"
  能力: "LP/MILP/NLP建模框架，对接GLPK/Gurobi/CPLEX"
  集成优先级: "已完成"
```

**第二梯队：有Python接口，需安装宿主软件**

```yaml
HEC-HMS_pyhms:
  领域: "流域水文预报"
  接口: "Python包装HEC-HMS命令行"
  用途: "降雨径流预报，流域来水边界条件生成"
  集成方式: "MCP工具封装，需服务器安装HEC-HMS"

MIKE_SDK:
  领域: "二维/三维水动力"
  接口: "DHI MIKE SDK (Python/C#)"
  用途: "复杂河口、海岸、湖泊水动力仿真"
  集成方式: "商业授权+MCP封装"
  注意: "需商业许可证"

OpenFOAM:
  领域: "CFD三维流场"
  接口: "Python驱动（PyFoam）"
  用途: "水工建筑物局部流场精细仿真"
  集成方式: "Docker容器化+MCP封装"
```

**第三梯队：专用领域，需特殊桥接**

```yaml
PSS_E:
  领域: "电力系统暂态稳定"
  接口: "psspy (Python, Windows COM)"
  用途: "水电梯级的电网侧仿真"
  集成方式: "Windows服务器+COM桥接+MCP封装"

RTDS:
  领域: "实时电力仿真（HIL）"
  接口: "专用API"
  用途: "水电机组HIL测试"
  集成方式: "需专用硬件，通过网络API桥接"

BPA_PSASP:
  领域: "中国电力系统仿真"
  接口: "文件接口/COM"
  用途: "国内水电工程的电网接入分析"
  集成方式: "文件I/O桥接+MCP封装"
```

**第四梯队：数据驱动/ML/RL基础设施（学习族引擎的底座）**

```yaml
PyTorch:
  角色: "学习族引擎的底层框架"
  安装: "pip install torch"
  驱动: "LSTM/Transformer/GNN/PINN/RL策略网络的训练和推理"
  集成方式: "PredictionEngine和LearningEngine内部使用，不直接暴露为MCP"

Stable_Baselines3:
  角色: "PolicyEngine的RL算法库"
  安装: "pip install stable-baselines3"
  驱动: "PPO/SAC/DQN/TD3/A2C"
  集成方式: "PolicyEngine内部调用，策略训练好后序列化为模型元件(M3)"

scikit-learn:
  角色: "传统ML方法"
  安装: "pip install scikit-learn"
  驱动: "随机森林/XGBoost/SVR/聚类/异常检测"
  集成方式: "PredictionEngine和DetectionEngine内部使用"

Hugging_Face_Transformers:
  角色: "预训练Transformer模型"
  安装: "pip install transformers"
  驱动: "TFT/PatchTST等时序Transformer，以及LLM微调"
  集成方式: "PredictionEngine内部使用"

DeepXDE_neuraloperator:
  角色: "物理约束深度学习"
  安装: "pip install deepxde / pip install neuraloperator"
  驱动: "PINN/DeepONet/FNO——构建保物理约束的代理模型"
  集成方式: "SurrogateEngine内部使用，产出的模型作为模型元件(M1)"

Gymnasium:
  角色: "RL训练环境标准接口"
  安装: "pip install gymnasium"
  驱动: "将SIL仿真包装为Gymnasium环境供RL训练"
  集成方式: |
    SIL平台实现env.step()/env.reset()接口
    PolicyEngine通过此接口训练RL策略
    训练好的策略作为模型元件(M3)挂入ControlEngine
```

**这些ML工具不直接暴露为MCP**——它们是引擎的内部依赖。对Skill层来说只看到`engine.predict()`和`engine.train_policy()`，不需要知道底层用的是PyTorch还是TensorFlow。

### 5.3 MCP封装示例

第一梯队工具的MCP封装极薄——Python原生API上面套一层标准接口即可：

```python
# WNTR → MCP封装示例（约30行核心代码）
@mcp_tool
def simulate_pipe_network(inp_file: str, duration: float = 86400,
                          timestep: float = 300) -> dict:
    """管网水力仿真"""
    import wntr
    wn = wntr.network.WaterNetworkModel(inp_file)
    wn.options.time.duration = duration
    wn.options.time.hydraulic_timestep = timestep
    sim = wntr.sim.WNTRSimulator(wn)
    results = sim.run_sim()
    return {
        "pressures": results.node['pressure'].to_dict(),
        "flows": results.link['flowrate'].to_dict(),
        "status": "success"
    }

# PySWMM → MCP封装示例
@mcp_tool
def simulate_drainage(inp_file: str, control_rules: dict = None) -> dict:
    """排水管网仿真（支持运行时控制注入）"""
    from pyswmm import Simulation, Nodes, Links
    results = {"node_depths": {}, "link_flows": {}}
    with Simulation(inp_file) as sim:
        for step in sim:
            if control_rules:
                _apply_controls(sim, control_rules)  # 运行时注入控制
            # 记录关键结果...
    return results

# RAS Commander → MCP封装示例
@mcp_tool
def simulate_river_reach(project_path: str, plan_id: str = "01") -> dict:
    """河道水力仿真"""
    from ras_commander import init_ras_project, RasCmdr, ras
    init_ras_project(project_path, "6.5")
    success = RasCmdr.compute_plan(plan_id)
    # 从HDF5直接读取结果
    return {
        "water_surface": ras.get_results("water_surface"),
        "velocity": ras.get_results("velocity"),
        "success": success
    }
```

### 5.4 集成路线图

```
阶段       接入工具                    覆盖场景               工作量
━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━       ━━━━━━━━━━━━━━━━     ━━━━━━━
已完成     HydroOS自研 + Pyomo        引调水/通用仿真/优化    —

Phase 1   WNTR + PySWMM              城市供排水              每个2-3天
(近期)     ras-commander              河道防洪               2-3天
          共3个MCP工具封装             覆盖五大水网中的三大类

Phase 2   FloPy                      地下水                 2-3天
(中期)     HEC-HMS(pyhms)             流域水文预报            3-5天
          swmm_api                   排水模型编辑            2-3天

Phase 3   PSS/E桥接                  水电梯级电气侧          1-2周
(按需)     MIKE SDK                   复杂水动力             1-2周
          各单位自有模型               项目定制               按项目

每个工具封装 = 1个MCP函数 + 1个S0 Skill包装
上层S1/S2/规则/模板完全不变
```

### 5.5 工具箱层（Toolkit）：领域小工具集

七大引擎是"干大事的"，但日常工作中80%的时间在用各种"小工具"——数据清洗、曲线拟合、单位换算、格式转换、统计分析……这些不是引擎，是**跨引擎的公共基础设施**，任何引擎、任何Skill、任何元件都可能调用。

```
架构位置：工具箱不是第八个引擎，而是与七大引擎并列的公共服务层

┌─────────────── ②Skill层 ───────────────┐
│  S0/S1/S2 都可以调用引擎和工具箱         │
├──────────┬──────────────────────────────┤
│  七大引擎 │         工具箱（Toolkit）     │
│  仿真     │  数据处理 / 统计分析 / 诊断   │
│  辨识     │  曲线拟合 / 格式转换 / GIS    │
│  调度     │  可视化 / 报告 / 能耗分析      │
│  控制     │  水质 / 经济 / 频率分析        │
│  优化     │  单位换算 / 坐标变换           │
│  预测     │  ......                       │
│  学习     │  任何引擎和Skill都可以调       │
├──────────┴──────────────────────────────┤
│             ④ 三族元件库                  │
└─────────────────────────────────────────┘
```

工具箱按功能域分为10个工具包，每个工具包含若干工具函数：

```yaml
# ============================================================
# TK1: 数据处理工具包（最常用，几乎每次交互都会用到）
# ============================================================
TK1_DataProcessing:
  tools:
    clean_timeseries:       "缺失填补(线性/样条/前向)、异常值检测剔除、冻结值识别"
    resample:               "时序重采样(升采样/降采样/对齐多源数据)"
    filter:                 "滤波(滑动平均/中值/Butterworth/小波去噪)"
    normalize:              "标准化/归一化(MinMax/Z-Score/物理量纲归一)"
    align_multi_source:     "多源数据时间对齐(SCADA/气象/水文站/IoT)"
    detect_outlier:         "异常值检测(3σ/IQR/孤立森林/DBSCAN)"
    detect_changepoint:     "变点检测(CUSUM/Pettitt/贝叶斯变点)"
    fill_gap:               "缺测段智能填补(按数据特征自选方法)"
    validate_physics:       "物理一致性校验(水量平衡/能量守恒/单调性)"

# ============================================================
# TK2: 曲线拟合与函数逼近
# ============================================================
TK2_CurveFitting:
  tools:
    fit_polynomial:         "多项式拟合(最小二乘，自动选阶)"
    fit_rating_curve:       "水位-流量关系曲线(幂函数/分段/复合)"
    fit_pump_curve:         "泵特性曲线拟合(H-Q/η-Q/P-Q)"
    fit_storage_curve:      "库容曲线拟合(Z-V/Z-A)"
    fit_loss_curve:         "水头损失曲线拟合(Darcy/Hazen-Williams系数反推)"
    fit_gate_discharge:     "闸门出流系数拟合(开度-流量系数)"
    fit_evaporation:        "蒸发公式拟合(Penman/Hargreaves参数率定)"
    fit_infiltration:       "入渗曲线拟合(Horton/Green-Ampt/Philip)"
    fit_custom:             "自定义函数形式的最小二乘/极大似然拟合"
    interpolate_2d:         "二维插值(综合特性曲线/效率曲面)"

# ============================================================
# TK3: 统计分析
# ============================================================
TK3_Statistics:
  tools:
    frequency_analysis:     "频率分析(P-III/LogNormal/GEV/Gumbel，设计洪水/暴雨)"
    trend_test:             "趋势检验(Mann-Kendall/Sen斜率/线性回归)"
    correlation:            "相关分析(Pearson/Spearman/互相关/滞后相关)"
    spectral:               "频谱分析(FFT/功率谱/小波分析——识别周期性)"
    return_period:          "重现期计算(给定量级→重现期，或给定重现期→量级)"
    confidence_interval:    "置信区间估计(Bootstrap/Delta法/贝叶斯)"
    distribution_fit:       "概率分布拟合与检验(K-S/A-D/Chi-Square)"
    extreme_value:          "极值统计(年最大值/超阈值POT)"
    regression:             "回归分析(线性/多元/分段/非线性/正则化)"

# ============================================================
# TK4: 诊断与健康评估
# ============================================================
TK4_Diagnostics:
  tools:
    diagnose_sensor:        "传感器健康诊断(漂移/冻结/噪声增大/量程偏移)"
    diagnose_pump:          "水泵性能衰退诊断(效率下降/振动异常/气蚀征兆)"
    diagnose_gate:          "闸门健康诊断(卡阻/泄漏/开度偏差)"
    diagnose_pipe:          "管道健康评估(壁厚/粗糙度变化/漏损率趋势)"
    diagnose_model:         "模型诊断(残差分析/偏差趋势/是否需要重校准)"
    diagnose_controller:    "控制器性能诊断(振荡/超调增大/跟踪精度下降)"
    root_cause_analysis:    "根因分析(鱼骨图/故障树/关联规则挖掘)"
    remaining_life:         "剩余寿命估计(退化模型/Weibull分析)"

# ============================================================
# TK5: 单位与坐标
# ============================================================
TK5_UnitsAndCoords:
  tools:
    convert_units:          "任意物理量单位换算(流量/水头/压力/功率/...)"
    convert_datum:          "高程基准转换(黄海85/吴淞/当地基准)"
    convert_coordinates:    "坐标系转换(WGS84/CGCS2000/UTM/高斯投影)"
    calc_distance:          "两点距离/河道长度计算"
    delineate_catchment:    "流域/子流域边界提取(DEM→分水线)"

# ============================================================
# TK6: 格式转换与数据I/O
# ============================================================
TK6_FormatIO:
  tools:
    read_scada:             "SCADA数据导入(OPC-UA/Modbus/MQTT/CSV)"
    read_inp:               "EPANET INP文件读写"
    read_hdf5:              "HEC-RAS HDF5结果读取"
    read_dss:               "HEC-DSS数据读写"
    read_netcdf:            "气象/水文NetCDF数据读取"
    read_shp:               "GIS Shapefile读取(管网/流域/DEM)"
    export_report:          "导出标准格式报告(Word/PDF/HTML)"
    export_chart:           "导出图表(PNG/SVG/交互式HTML)"
    convert_model_format:   "模型格式互转(INP↔JSON↔YAML↔HydroOS)"

# ============================================================
# TK7: 水力水文计算小工具
# ============================================================
TK7_HydroCalc:
  tools:
    calc_manning:           "明渠均匀流Manning公式(正算/反算任一变量)"
    calc_weir:              "堰流公式(宽顶堰/薄壁堰/实用堰)"
    calc_orifice:           "孔口出流(自由/淹没)"
    calc_pipe_headloss:     "管道水头损失(Darcy-Weisbach/Hazen-Williams/万宁)"
    calc_water_hammer:      "简化水锤估算(Joukowsky公式)"
    calc_critical_depth:    "临界水深计算"
    calc_normal_depth:      "正常水深计算(迭代求解)"
    calc_backwater:         "壅水曲线计算(逐段推求)"
    calc_flood_routing:     "洪水演算(马斯京根/连续法)"
    calc_rational_method:   "推理公式(暴雨径流设计流量)"
    calc_scs_cn:            "SCS-CN法径流量计算"
    calc_idf:               "暴雨强度公式(IDF曲线)计算"
    calc_concentration_time: "流域汇流时间估算(多种经验公式)"
    calc_evaporation:       "蒸发量计算(Penman/Penman-Monteith/Hargreaves)"
    calc_water_balance:     "水量平衡核算(入-出-蓄-损)"

# ============================================================
# TK8: 水质计算
# ============================================================
TK8_WaterQuality:
  tools:
    calc_bod_decay:         "BOD衰减计算(Streeter-Phelps)"
    calc_chlorine_decay:    "余氯衰减计算(一阶反应)"
    calc_mixing:            "混合计算(完全混合/不完全混合)"
    calc_wqi:               "水质指数计算(综合WQI/单因子)"
    calc_dilution:          "稀释倍数计算(排污口/支流汇入)"
    calc_sediment:          "泥沙输运基本计算(悬移质/推移质)"
    calc_water_age:         "管网水龄估算"

# ============================================================
# TK9: 经济与能耗分析
# ============================================================
TK9_Economics:
  tools:
    calc_pump_energy:       "泵站能耗计算(电量/电费/单方水能耗)"
    calc_turbine_energy:    "水轮机发电量计算"
    calc_lifecycle_cost:    "全生命周期成本分析(建设+运行+维护+更新)"
    calc_benefit_cost:      "效益费用比计算"
    calc_tariff_optimization: "峰谷电价下的泵站运行时段优化"
    calc_carbon_footprint:  "碳排放估算(泵站/水处理/管网)"
    calc_water_price:       "水价测算(成本+利润+税费)"

# ============================================================
# TK10: 可视化
# ============================================================
TK10_Visualization:
  tools:
    plot_timeseries:        "时序曲线图(单/多变量/双轴/包络)"
    plot_profile:           "沿程剖面图(水面线/压力线/能量线)"
    plot_network:           "管网/渠系拓扑图(着色=压力/流量/水质)"
    plot_scatter:           "散点图(相关性/率定前后对比)"
    plot_exceedance:        "超越概率曲线(频率分析结果)"
    plot_hydrograph:        "流量过程线(洪水/日变化)"
    plot_pump_curve:        "泵特性曲线+工作点标注"
    plot_heatmap:           "时空热力图(管网/渠系)"
    plot_comparison:        "多方案对比图(柱状/雷达/平行坐标)"
    animate_simulation:     "仿真动画(水面线演进/洪水淹没)"
```

**工具箱如何与Skill层衔接**：

工具箱里的每个函数不单独暴露为S0 Skill——它们太细碎了，直接列在Skill菜单里会淹没用户。正确的做法是：

```
方式1：被S0/S1 Skill内部调用（用户不感知）
  S0-SIM仿真Skill内部自动调TK1数据清洗来预处理输入
  S0-ID辨识Skill内部自动调TK2曲线拟合来拟合泵曲线
  S1-FCST预报Skill内部自动调TK3频率分析来量化不确定性

方式2：被认知AI直接调用（用户问小问题时）
  用户问"把这个水位数据清洗一下" → 认知AI直接调TK1.clean_timeseries
  用户问"渠道正常水深多少" → 认知AI直接调TK7.calc_normal_depth
  用户问"泵站月电费多少" → 认知AI直接调TK9.calc_pump_energy

方式3：被模板渲染器调用（生成输出时）
  B3预演报告需要图 → 模板渲染器调TK10.plot_comparison
  B5 SIL报告需要统计 → 模板渲染器调TK3.confidence_interval
```

**工具箱函数的Skill权限继承其调用者**——TK7.calc_manning()被designer_L0的Skill调用时，输出格式按设计员规则出计算书；被student_S1的Skill调用时，输出格式按大专生规则出步骤式操作说明。工具箱本身不区分角色。

**工具箱的数量**：10个工具包 × 平均10个函数 = ~100个工具函数。听起来多，但每个都很小（几十行代码），且大部分是对scipy/numpy/pandas/matplotlib的薄封装加上水利专业的默认参数和物理校验。

---

## 六、第④层：对象（三族元件库）

### 6.1 元件库

元件是引擎驱动的最小计算单元。之前只覆盖了水力元件（闸泵阀、库湖池、河沟渠），现在扩展为三大族：物理元件、水文元件、模型元件——统一继承同一个基类，统一被引擎驱动。

```
元件库（三族）
│
├── 第一族：物理元件（被仿真引擎驱动）
│   ├── 执行器类（T1）
│   │   闸门（平板/弧形/人字）  水泵（离心/轴流/混流）
│   │   阀门（蝶阀/球阀/PRV/FCV）  水轮机（混流/轴流转桨/冲击/贯流）
│   │   船闸闸门  升船机
│   ├── 蓄水体类（T2）
│   │   水库  湖泊  水池/水箱  调蓄池  蓄滞洪区
│   ├── 输水体类（T3）
│   │   明渠（梯形/矩形/U形）  管道（球墨铸铁/PCCP/钢管/PE）
│   │   河道  隧洞  渡槽  倒虹吸
│   └── 耦合器类
│       水机电接口  闸-渠接口  泵-管接口  船闸充泄水  梯级耦合
│
├── 第二族：水文元件（被仿真引擎+预测引擎驱动）
│   ├── 产流类（H1）
│   │   流域/子流域  透水面  不透水面  土壤层  地下含水层
│   ├── 汇流类（H2）
│   │   单位线  马斯京根河段  运动波渠段  地下水汇流
│   ├── 气象驱动类（H3）
│   │   降雨场  蒸发场  温度场  风场  雪/冰模型
│   └── 水文耦合器
│       流域-河道接口  地表-地下水交换  降雨-径流-汇流串联
│
└── 第三族：模型元件（被预测引擎+学习引擎驱动）
    ├── 替代模型类（M1）
    │   IDZ降阶模型  POD降阶模型  DMD降阶模型
    │   神经网络代理模型  PINN物理约束网络
    ├── 时序预测模型类（M2）
    │   LSTM  Transformer  TFT  GNN(图网络)
    │   集成模型(物理+数据混合)
    ├── 策略模型类（M3）
    │   RL策略(PPO/SAC/DQN)  模仿学习策略  规则策略
    │   在线学习模型(Bandit/贝叶斯优化)
    └── 概念水文模型类（M4）
        新安江  Sacramento  HBV  GR4J  TOPMODEL  SCS-CN
```

**三族的统一性**：所有元件继承同一个基类，都有compute()方法、参数集、端口和约束——只是内部计算逻辑不同：

```python
class Component(ABC):
    """所有元件的统一基类——物理元件、水文元件、模型元件共用"""

    @abstractmethod
    def compute(self, state, inputs, dt) -> dict:
        """推进一步——物理元件解方程，水文元件算产汇流，模型元件做推断"""

    @abstractmethod
    def get_params(self) -> ParamSet:         # 参数集
    def get_ports(self) -> List[Port]:         # 连接端口
    def get_constraints(self) -> ConstraintSet # 约束
    def get_designable_params(self) -> List    # 可设计参数


# 物理元件：compute()内部解Saint-Venant方程
class OpenChannelComponent(Component):
    def compute(self, state, inputs, dt):
        return saint_venant_step(state, inputs, self.params, dt)

# 水文元件：compute()内部算产流
class SubBasinComponent(Component):
    def compute(self, state, inputs, dt):
        rainfall = inputs["precipitation"]
        return runoff_generation(state, rainfall, self.soil_params, dt)

# 模型元件：compute()内部做神经网络推断
class LSTMPredictorComponent(Component):
    def compute(self, state, inputs, dt):
        return self.model.forward(inputs["features"])

# 策略元件：compute()内部做RL策略推断
class RLPolicyComponent(Component):
    def compute(self, state, inputs, dt):
        return self.policy.predict(state["observation"])
```

### 6.1b 水文元件详述

水文元件和物理元件的关键差异在于：物理元件描述的是**管控对象**（有执行器可以干预），水文元件描述的是**外部驱动**（降雨你控制不了，只能预测和应对）。但在CHS六要素框架下，水文过程正是**Disturbance（扰动）**的来源——水文预报的本质就是预测扰动的未来演化。

```yaml
SubBasinComponent:  # 子流域产流元件
  category: "H1"
  params:
    area:              {unit: "km²",  attr: FIXED}
    cn_number:         {unit: "-",    attr: IDENTIFIABLE}   # SCS曲线号
    soil_type:         {choices: ["砂土","壤土","黏土"], attr: FIXED}
    initial_loss:      {unit: "mm",   attr: IDENTIFIABLE}
    recession_constant: {unit: "-",   attr: IDENTIFIABLE}
  ports:
    input:  "降雨序列(mm/h)"
    output: "径流过程线(m³/s)"
  compute_methods:     # 同一个元件可以有多种计算方法
    - "SCS-CN法"       # 仿真引擎调用
    - "新安江三水源"    # 仿真引擎调用
    - "LSTM数据驱动"   # 预测引擎调用
    - "GR4J概念模型"   # 仿真引擎调用

UnitHydrographComponent:  # 单位线汇流元件
  category: "H2"
  params:
    lag_time:     {unit: "h",  attr: IDENTIFIABLE}
    peak_factor:  {unit: "-",  attr: IDENTIFIABLE}
    shape:        {choices: ["SCS无因次", "Snyder", "Clark"], attr: DESIGNABLE}
  ports:
    input:  "净雨序列(mm/h)"
    output: "出口流量过程线(m³/s)"

RainfallFieldComponent:  # 降雨场元件
  category: "H3"
  params:
    stations:        {desc: "雨量站列表和坐标"}
    interpolation:   {choices: ["泰森多边形","IDW","克里金"], attr: DESIGNABLE}
    forecast_source: {choices: ["气象局API","WRF降尺度","统计降水生成器"]}
  ports:
    output: "时空降雨场(mm/h per grid)"
```

### 6.1c 模型元件详述

模型元件是物理元件的**加速替身或智能扩展**。一个模型元件挂在一个物理元件上，提供"快速近似计算"或"学习得到的策略"：

```yaml
IDZSurrogateComponent:  # IDZ降阶模型
  category: "M1"
  description: "渠池的Integrator-Delay-Zero传递函数降阶模型"
  parent_component: "OpenChannelComponent"  # 它是明渠元件的替身
  params:
    integrator_gain: {unit: "-", attr: IDENTIFIABLE}  # 从仿真数据辨识
    delay_time:      {unit: "s", attr: IDENTIFIABLE}
    zero_time:       {unit: "s", attr: IDENTIFIABLE}
  accuracy: "设计点附近误差<5%，偏离设计点>20%时需回退物理模型"
  use_case: "MPC在线优化中替代Saint-Venant做快速前向预测"

LSTMPredictorComponent:  # LSTM预测模型
  category: "M2"
  description: "基于历史时序的多步预测"
  params:
    input_features:  {desc: "输入特征列表", attr: DESIGNABLE}
    hidden_size:     {unit: "-", attr: DESIGNABLE, range: [32, 512]}
    num_layers:      {unit: "-", attr: DESIGNABLE, range: [1, 4]}
    lookback:        {unit: "步", attr: DESIGNABLE}
    horizon:         {unit: "步", attr: DESIGNABLE}
    trained_weights: {desc: "训练好的权重文件路径", attr: FIXED}
  training:
    engine: "PredictionEngine"
    data: "历史运行数据"
    validation: "留出法或交叉验证"

RLPolicyComponent:  # 强化学习策略
  category: "M3"
  description: "通过与仿真环境交互学习到的调度/控制策略"
  params:
    state_space:     {desc: "状态空间定义（哪些观测量）"}
    action_space:    {desc: "动作空间定义（哪些控制变量）"}
    reward_function: {desc: "奖励函数定义", attr: DESIGNABLE}
    algorithm:       {choices: ["PPO","SAC","DQN","TD3"], attr: DESIGNABLE}
    trained_policy:  {desc: "训练好的策略文件路径", attr: FIXED}
  training:
    engine: "LearningEngine"
    environment: "SimulationEngine提供的SIL环境"
    episodes: "训练轮次"
  deployment: |
    训练好的策略作为ControlEngine的一个控制器类型使用：
    ControlEngine.control(state, type="rl_policy", policy=self.trained_policy)
    在线执行只需毫秒级推断，不需要重新训练

XinAnJiangComponent:  # 新安江水文模型
  category: "M4"
  description: "三水源新安江模型——中国最广泛使用的概念性水文模型"
  params:
    WM:    {desc: "流域平均蓄水容量", unit: "mm", attr: IDENTIFIABLE}
    WUM:   {desc: "上层蓄水容量",    unit: "mm", attr: IDENTIFIABLE}
    WLM:   {desc: "下层蓄水容量",    unit: "mm", attr: IDENTIFIABLE}
    KC:    {desc: "蒸发折算系数",    unit: "-",  attr: IDENTIFIABLE}
    B:     {desc: "蓄水容量曲线指数", unit: "-",  attr: IDENTIFIABLE}
    SM:    {desc: "自由水蓄水容量",   unit: "mm", attr: IDENTIFIABLE}
    KG:    {desc: "地下水出流系数",   unit: "-",  attr: IDENTIFIABLE}
    KI:    {desc: "壤中流出流系数",   unit: "-",  attr: IDENTIFIABLE}
    # 共约15个参数，全部可辨识
  ports:
    input: "降雨(mm) + 蒸发(mm)"
    output: "地表径流 + 壤中流 + 地下径流(m³/s)"
```

### 6.1d 元件之间的关系

```
物理元件（第一族）        水文元件（第二族）        模型元件（第三族）
━━━━━━━━━━━━━━━         ━━━━━━━━━━━━━━━         ━━━━━━━━━━━━━━━
描述管控对象              描述外部驱动              描述加速替身/学习策略

闸门.compute()           子流域.compute()          IDZ.compute()
  → 解闸孔出流公式          → 算降雨径流               → 传递函数快速推演

水库.compute()           降雨场.compute()          LSTM.compute()
  → 解水量平衡方程          → 插值时空降雨场           → 神经网络推断

管道.compute()           马斯京根.compute()        RL策略.compute()
  → 解MOC特征线方程         → 算河道洪水演进           → 策略网络推断

          │                      │                      │
          └──────────┬───────────┘──────────┬───────────┘
                     │                      │
              都继承Component基类     都被引擎统一驱动
              都有compute/params/ports  都可以组装成水网
```

**组装示例**：一个完整的流域防洪系统 = 水文元件 + 物理元件 + 模型元件混合组装：

```python
flood_system = WaterNetwork()
# 水文元件：降雨→产流→汇流
flood_system.add(RainfallFieldComponent("rain_field"))
flood_system.add(SubBasinComponent("sub_1", method="新安江"))
flood_system.add(SubBasinComponent("sub_2", method="LSTM"))  # 数据驱动
flood_system.add(UnitHydrographComponent("uh_1"))
# 物理元件：水库+河道+闸门
flood_system.add(ReservoirComponent("reservoir_1"))
flood_system.add(GateComponent("spillway_gate"))
flood_system.add(OpenChannelComponent("downstream_reach"))
# 模型元件：RL调度策略
flood_system.add(RLPolicyComponent("dispatch_policy", algorithm="PPO"))
# 连接
flood_system.connect("rain_field→sub_1→uh_1→reservoir_1")
flood_system.connect("rain_field→sub_2→reservoir_1")  # 第二个子流域用LSTM
flood_system.connect("reservoir_1→spillway_gate→downstream_reach")
flood_system.connect("dispatch_policy→spillway_gate")  # RL策略控制闸门
```

### 6.2 元件参数的四种属性

每个参数标注其属性，决定它被哪个引擎操作：

```
FIXED        — 物理常数或已定设计值    → 不可变
IDENTIFIABLE — 可从运行数据中估计      → 辨识引擎操作
DESIGNABLE   — 可在设计阶段优化        → 优化引擎操作
TRAINABLE    — 可从数据/交互中学习      → 预测引擎或学习引擎操作
```

```yaml
# 物理元件参数（和之前一样）
PumpComponent:
  pump_type:     DESIGNABLE      # 选型
  curve_H:       IDENTIFIABLE    # 从实测拟合
  NPSH_required: FIXED           # 出厂确定

# 水文元件参数
SubBasinComponent:
  area:          FIXED           # 地理确定
  cn_number:     IDENTIFIABLE    # 从历史洪水数据反推
  soil_type:     FIXED           # 勘察确定

# 模型元件参数
LSTMPredictorComponent:
  hidden_size:   DESIGNABLE      # 网络结构设计
  lookback:      DESIGNABLE      # 输入窗口设计
  weights:       TRAINABLE       # 从训练数据中学习

RLPolicyComponent:
  reward_fn:     DESIGNABLE      # 奖励函数设计
  algorithm:     DESIGNABLE      # PPO/SAC选择
  policy_weights: TRAINABLE      # 从环境交互中学习
```

**TRAINABLE参数的生命周期**：离线训练→验证→部署→在线微调→定期重训练。与IDENTIFIABLE的区别是：IDENTIFIABLE用少量物理约束数据估计几个参数，TRAINABLE用大量数据学习成百上千的权重。

示例：

```yaml
PumpComponent:
  pump_type:     DESIGNABLE   # 离心/轴流/混流 → 优化引擎选型
  rated_flow:    DESIGNABLE   # 额定流量 → 优化引擎确定
  rated_head:    DESIGNABLE   # 额定扬程 → 优化引擎确定
  quantity:      DESIGNABLE   # 台数（含备用） → 优化引擎确定
  curve_H:       IDENTIFIABLE # H-Q特性曲线 → 辨识引擎从实测拟合
  curve_eta:     IDENTIFIABLE # 效率曲线 → 辨识引擎从实测拟合
  NPSH_required: FIXED        # 必需汽蚀余量 → 出厂确定

OpenChannelComponent:
  bottom_width:  DESIGNABLE   # 底宽 → 优化引擎（经济断面）
  side_slope:    DESIGNABLE   # 边坡 → 优化引擎
  bed_slope:     DESIGNABLE   # 底坡 → 优化引擎
  roughness:     IDENTIFIABLE # 糙率 → 辨识引擎（从实测水面线反推）
  lining:        DESIGNABLE   # 衬砌方式 → 优化引擎
```

### 6.3 水网组装

任意水网 = 从三族元件库选元件 + 定义拓扑连接 + 设置边界条件。物理元件、水文元件、模型元件可以混合组装：

```python
# 南水北调中线 = 物理元件为主
#   64闸 + 渠池 + 倒虹吸 + 渡槽 + IDZ降阶模型(MPC用)

# 流域防洪 = 三族混合
#   子流域(水文) + 新安江模型(水文) + 水库(物理) + 河道(物理) + RL调度策略(模型)

# 城市供水 = 物理元件 + 预测模型
#   管段+泵站+阀门(物理) + LSTM需水预测(模型) + GNN泄漏检测(模型)

# 水电梯级 = 物理元件 + RL策略
#   水库+水轮机+引水隧洞(物理) + PPO联合调度策略(模型)

# 双容水箱 = 纯物理
#   2个水箱 + 1个泵 + 2个阀门
```

新增一种水网不需要改任何上层代码——从三族元件库混合组装即可自动获得全部Skill能力。水文元件提供扰动预报，模型元件提供快速预测和学习策略，物理元件提供精确仿真和安全校验——三族协作。

---

## 七、设计的全部环节

"设计"远不止控制器设计。优化引擎可以作用于元件的任何DESIGNABLE参数：

```yaml
工程设计环节:
  拓扑布局:   路线选择、节点布置、管段/渠段分段
  断面设计:   底宽、边坡、管径、壁厚、衬砌方式（经济断面优化）
  设备选型:   泵型(离心/轴流/混流)、台数、变频/工频、阀门型式、口径
  结构设计:   水池尺寸、水库特征水位、闸室长宽、消力池深度
  工艺计算:   设计流量、调蓄容积、水头损失、NPSH校核

水文设计环节:
  流域分析:   子流域划分、汇水面积、CN值确定
  设计暴雨:   暴雨频率分析、设计雨型选择、面深关系
  产汇流模型: 水文模型类型选择(新安江/HBV/SCS-CN)、参数率定
  设计洪水:   频率洪水推求、PMF计算、调洪演算

数据模型设计环节:
  预测模型:   模型架构选择(LSTM/Transformer/GNN)、超参数优化、训练数据切分
  降阶模型:   降阶方法选择(IDZ/POD/PINN)、精度-速度权衡、适用范围标定
  RL策略:     状态空间/动作空间定义、奖励函数设计、安全约束编码
  混合模型:   物理-数据融合策略设计、物理约束权重、在线修正机制

控制系统设计环节:
  控制架构:   HDC层级划分、MAS分区、通信架构
  控制器设计: 算法选择(PID/MPC/DMPC/RL策略)、参数整定、采样周期
  ODD定义:    正常/降级/限制三区边界、降级策略

验证设计环节:
  测试设计:   SIM/SIL/HIL测试工况集、通过标准
  场景库:     ODD全工况覆盖、极端工况定义

运行策略设计:
  调度规则:   规则参数、优先级
  启停序列:   泵站群最优启动顺序
  工况切换:   切换阈值、过渡策略
```

每个环节都是已有S0 Skill的组合应用——仿真校核+辨识建模+优化求解+控制验证——指向元件不同的DESIGNABLE参数，不需要新增Skill。

### 7.1 MBD与传统设计院流程的矛盾

传统设计院按专业划分，流水线协作，反馈代价极高：

```
传统设计院流水线：
规划专业 → 水文专业 → 水工专业 → 机电专业 → 自动化专业 → 概预算
  来水分析   设计洪水    渠道断面    泵站选型    控制系统    工程造价
             径流系列    闸室尺寸    阀门选型    SCADA配置
                        管径计算    水轮机选型

人工反馈（很少发生，代价巨大）：
  机电专业发现：选出的轴流泵在低流量工况扬程不够
  → 退回水工专业：改管径降低阻力，或改渠道坡降
  → 水工改了管径 → 概预算重算 → 审查会重开
  → 所以大多数时候选择"凑合用"或"加翻板闸憋水头"
```

**传统设计的反馈代价太高，所以大家尽量避免反馈。** 每个专业交出的成果一旦修改，下游全部返工。设计院文化是"尽量一次做对"而不是"快速迭代"。

MBD则是完全不同的逻辑：

```
MBD闭环（统一模型内）：
  水工改了管径 → 水力仿真自动重算 → 泵的工作点自动更新
  → 控制器性能自动重新评估 → 造价自动更新
  → 不满足就再改，每次迭代几分钟而不是几个月
```

### 7.2 设计院切入策略：三阶段渗透

不能一上来就要求设计院变革流程。正确的路径是从不颠覆现有流程开始，逐步渗透：

```
阶段      目标用户                产品形态          价值主张
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

近期      机电/自动化骨干工程师    个人超级工具      "全工况校核，3分钟出结果"
（1人用）  designer_L1             S0原子Skill      不改流程，帮个人做得更好
          不需要跨专业协作         选型+仿真+校核    发现问题后有数据去沟通

中期      项目总工                方案审查平台       "方案审定前做全系统验证"
（带团队） designer_L2             S1组合Skill      减少返工，避免运行阶段翻车
          协调各专业               方案比选+SIL      多专业模型集成审查

远期      设计院整体              MBD设计平台        "设计即运行能力定义"
（流程变革）全层级协作              S2流程Skill      从流水线到闭环迭代
          新成立的团队先试          MBD全流程        V模型贯通
```

**三个阶段对应的Skill层级和设计角色**：

```yaml
近期_个人工具:
  用户: "designer_L1"（机电专业骨干）
  典型场景:
    - 拿到水工给的管径和流量 → 用S0-SIM做全工况泵选型校验
    - 发现10个流量工况下轴流泵扬程不够 → 有仿真数据去跟水工沟通
    - 比较离心泵vs轴流泵vs混流泵在全工况范围的效率包络
  Skill使用: S0-SIM（仿真）+ S0-OPT（选型优化）+ S0-ID（曲线辨识）
  价值: 不改变设计院任何流程，一个人就能用起来

中期_方案审查:
  用户: "designer_L2"（项目总工）
  典型场景:
    - 方案审查前 → 用S1-RHSL做全系统联合仿真
    - "这个方案在10个流量工况下能不能正常启动？"
    - 发现问题 → 在模型里直接调参数看改进效果
    - 多方案比选 → 统一指标体系量化对比
  Skill使用: S1-RHSL（预演）+ S1-SIL（全工况测试）+ S0-OPT（参数优化）
  价值: 总工第一次能在审查阶段验证"设计出来的系统到底能不能运行"

远期_MBD变革:
  用户: 全层级设计团队
  典型场景:
    - 水工、机电、自动化围绕统一模型并行工作
    - 改一个参数 → 全系统自动重算 → 实时反馈
    - V模型完整走通：需求→ODD→设计→SIM→SIL→HIL
  Skill使用: S2-MBD（全流程）
  价值: 从"流水线串行交接"到"统一模型并行协作"
```

### 7.3 设计院的销售故事

串联泵站案例是最好的切入点：

```
故事线：
  某引调水工程，设计流量20m³/s，各泵站选用轴流泵，扬程2m。
  设计阶段：按设计工况点选型，计算书没问题，审查通过。
  运行阶段：经常只有10个流量，轴流泵扬程不够，启动失败。
  打补丁：甩站（低扬程泵站不开）+ 出口加翻板闸憋水头。
  代价：能耗增加30%+，运行灵活性丧失，安全隐患。

如果用了HydroClaw：
  设计阶段，机电工程师用"全工况选型校核"（S0-SIM + S0-OPT）：
  → 3分钟发现10个流量工况下轴流泵扬程不够
  → 自动比选：改用混流泵，或增加变频驱动
  → SIL全工况测试（S1-SIL）：5-20个流量全覆盖验证
  → 在设计阶段就解决问题，不用到运行阶段打补丁

  一句话：
  "如果当初用了我们的工具，翻板闸就不用加了，
   每年省下的电费就够买十套HydroClaw。"
```

---

## 八、运行时示例

### 示例1：用户选"断面优化"Skill

```
用户："帮我优化这段渠道的断面，设计流量50m³/s"

系统自动执行：
├── 角色推断：Skill标签=[designer] → 加载设计规则
│   规则：必须引用设计规范、包含安全系数、对比基准方案
│
├── Skill执行（S0组合）：
│   Step 1: S0-SIM → 当前断面水力校核
│   Step 2: S0-OPT → 以经济断面为目标，优化bottom_width/side_slope
│           目标函数：min(造价+运行费)
│           约束：流速≤允许值、弗劳德数、超高≥规范要求
│   Step 3: S0-SIM → 优化后断面水力复核
│
├── 模板渲染：T3.simulation + 设计规则修饰
│   输出包含：规范依据、安全系数、与原方案对比
│
└── 输出（设计角色风格）：
    "依据《灌溉与排水工程设计标准》GB 50288，
     优化后梯形断面：底宽4.2m，边坡1:1.5，设计水深2.8m。
     较原方案（底宽5.0m）减少开挖方量18%，
     年运行费降低12%。弗劳德数0.35，满足≤0.86的规范要求。
     安全超高0.5m，满足≥0.4m的规范要求。"
```

### 示例2：用户选"ODD预警"Skill

```
用户："系统现在安全吗？"

系统自动执行：
├── 角色推断：Skill标签=[operator_L1, operator_L2]
│   根据用户权限确定L1还是L2
│   加载对应运维规则
│
├── Skill执行（S1-WARN）：
│   Step 1: S0-DET-01 → ODD检查（全系统扫描）
│   Step 2: S1-FCST → 对偏离正常区的指标做趋势预测
│
├── 模板渲染：B2预警模板
│
└── 输出（L1运维角色风格）：
    "🟢 全段整体正常。
     🟡 渠池17水位42.28m，距降级区上界0.02m，
        过去1h上升0.08m/h。建议关注。
     如需启动预演分析，请选择'四预闭环'Skill。"
```

### 示例3：设计院机电工程师选"泵站选型校核"Skill

```
用户（designer_L1）："帮我校核一下这组轴流泵，设计流量20m³/s，
                      但实际经常运行在10个流量，看看有没有问题"

系统自动执行：
├── 角色推断：Skill标签=[designer_L1] → 加载设计规则
│   规则：引用设计规范、全工况校核、给出比选方案
│
├── Skill执行（S0组合）：
│   Step 1: S0-SIM → 全工况仿真（5/10/15/20 m³/s四个工况）
│   Step 2: S0-ID  → 泵特性曲线与系统阻力曲线交叉分析
│   Step 3: S0-OPT → 候选泵型全工况效率包络对比
│           候选：轴流泵 vs 混流泵 vs 离心泵+变频
│   Step 4: S0-SIM → 最优方案的启停工况验证
│
├── 模板渲染：T1.diagnosis + 设计规则修饰
│
└── 输出（设计L1角色风格）：
    "⚠️ 校核发现关键问题：
     设计工况（20m³/s）：轴流泵扬程2.1m＞系统阻力1.8m，正常 ✅
     运行工况（10m³/s）：轴流泵扬程1.2m＜系统阻力1.4m，无法启动 ❌
     原因：轴流泵H-Q曲线陡降特性，偏离设计点后扬程下降快于阻力。

     替代方案比选（全工况5~20m³/s效率包络）：
     方案A 混流泵：        全工况效率62~78%，10m³/s可启动 ✅
     方案B 离心泵+变频：   全工况效率58~82%，10m³/s可启动 ✅
     方案C 轴流泵+翻板闸： 全工况效率41~75%，10m³/s依靠憋水头 ⚠️

     依据《泵站设计规范》GB/T 50265，推荐方案B（变频离心泵），
     年运行费较方案C节省约28%。
     详细选型计算书已生成，需提交专业负责人（L2）审核。"
```

### 示例4：项目总工选"MBD全系统验证"Skill

```
用户（designer_L2）："这个泵站改造方案，整体上能不能用？
                      做一个全系统验证"

系统自动执行：
├── 角色推断：Skill标签=[designer_L2] → 加载总工级设计规则
│   规则：全局视角、跨专业协调、给出审定意见
│
├── Skill执行（S2-MBD简化版）：
│   Step 1: 水网模型组装（管道+泵站+闸门+渠道全要素）
│   Step 2: S1-SIL → 全工况自动测试
│           · 5/10/15/20 m³/s稳态运行
│           · 10→20升流过渡
│           · 20→10降流过渡
│           · 单泵跳闸应急
│           · 冰期低流量运行
│   Step 3: 性能汇总 + 约束违反检查
│
└── 输出（总工L2角色风格）：
    "全系统验证结果摘要：
     测试工况12个，通过10个，未通过2个。
     ❌ 10m³/s冷启动：3号泵站扬程不足（详见校核报告§4.2）
     ❌ 单泵跳闸后重启：水锤压力峰值超管道承压（§5.1）
     建议：3号泵站改为混流泵+变频方案后，重新过SIL。
     批准状态：【待修改后重新验证】"
```

### 示例5：学生选"教学实验"Skill

```
本科生（student_S2）："我想试试把PID的Ki调大看看会怎样"

系统自动执行：
├── 角色推断：Skill标签=[student_S2] → 加载本科生教学规则
│   规则：苏格拉底引导、可调参数但不改模型、安全护栏
│
├── Skill执行（S2-EDU → S1-SIL教学模式）：
│   在隔离的教学SIL环境中执行Ki增大后的仿真
│   检测到即将振荡 → 暂停
│
└── 输出（本科生S2风格）：
    "有意思！水位开始振荡了。
     思考一下：Ki增大意味着积分作用更强，
     当偏差持续存在时积分项会怎样累积？
     这种现象在控制理论里叫什么？
     提示：翻阅教材第4章4.3节'积分饱和'。
     关联知识点：✅积分作用 ✅振荡分析 ☐抗饱和设计"
```

```
大专生（student_S1）同样的实验场景：

系统自动执行：
├── 角色推断：Skill标签=[student_S1] → 加载大专生教学规则
│   规则：步骤式引导、参数固定不可调、操作记录
│
└── 输出（大专生S1风格）：
    "实验任务：观察水位控制过程
     第1步：确认目标水位已设为30cm ✓
     第2步：点击'启动'按钮，等待系统稳定
     第3步：在记录表中填写调节时间：___秒
     第4步：观察曲线——水位有没有超过目标值？超过了多少？
     第5步：在实验报告中画出你观察到的曲线形状

     注意：本实验不需要修改控制器参数，
     重点是学会观察和记录系统响应。"
```

---

## 九、组件数量统计

```
层级              组件类型          数量     说明
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
① 认知决策层
  规则              L0-L4分层规则     ~40条   五层继承，Skill自动加载
  模板              T/B/W三级模板     23个    继承组合，角色修饰
  角色层级           5维度×多层级      19个    运维/教学/设计/科研各3级+学生4级

② 技能编排层
  S0原子Skill       封装引擎调用      ~53个   物理+预测+学习+工具箱
  S1组合Skill       编排多个S0        17个    原10+水文+训练+RL+诊断+数据治理+报告+泄漏
  S2流程Skill       编排多个S1         6个    含人机交互点

③ 计算引擎层
  通用引擎           领域无关算法       7个    仿真/辨识/调度/控制/优化/预测/学习
  工具箱             跨引擎公共服务     10包    数据处理/曲线拟合/统计/诊断/单位/
                    ~100个工具函数             格式IO/水力计算/水质/经济/可视化
  工具箱             日常工具集         1套    数据处理/统计/诊断/可视化/转换/知识查询

④ 物理对象层
  物理元件(第一族)    三大类+耦合器     ~20类   闸泵阀水轮机/库湖池/河沟渠
  水文元件(第二族)    产流+汇流+气象    ~10类   子流域/单位线/降雨场等
  模型元件(第三族)    替代+预测+策略    ~10类   IDZ/LSTM/RL策略/新安江等
  外部工具后端       已验证可集成       10+类   WNTR/PySWMM/ras-commander等
  ML/RL基础设施     引擎内部依赖       6+类    PyTorch/SB3/sklearn/HF/DeepXDE/Gymnasium
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总计                                  ~290个组件（含~100个工具函数）
```

---

## 十、扩展路径

所有扩展都是增量的，不改已有组件：

```
新增场景        新增方式                                    改动量
━━━━━━━━━━     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━          ━━━━━━━
新物理元件      继承Component实现compute()                   +1文件
新水文元件      继承Component，指定产流/汇流方法              +1文件
新预测模型      继承Component，封装训练好的模型               +1文件
新RL策略        继承Component，封装训练好的策略               +1文件
新概念水文模型  继承Component，实现模型方程                   +1文件
新工具函数      在对应TK工具包中添加函数                      +几行代码
新工具包        新建TK11等（如噪声分析/通航计算）              +1文件
新外部工具      作为引擎的可选后端(pip install+MCP封装)       +1文件，2-3天
新工程案例      新增L4案例参数文件                           +1 yaml
新设计环节      组合已有S0 Skill指向新的designable/trainable参数 +0文件
新水网类型      从三族元件库混合组装                          +0文件
新业务场景      组合已有S1为新S2                              +1文件
新角色层级      在Skill的role_tag中增加层级标签                改tag
```

---

## 十一、与已有系统的关系

```
CHS理论框架                HydroClaw认知智能实现
━━━━━━━━━━━                ━━━━━━━━━━━━━━━━━━━━━
六要素(PASDCO)         ←→  元件库的统一描述结构 + 模板基类
                           水文元件是Disturbance的来源建模
三大类物理对象          ←→  T1执行器 / T2蓄水体 / T3输水体
水文过程               ←→  H1产流 / H2汇流 / H3气象驱动 / M4概念水文模型
降阶与替代模型          ←→  M1替代模型（IDZ/POD/PINN/神经网络代理）
数据驱动预测           ←→  M2时序预测（LSTM/Transformer/GNN/混合）
强化学习策略           ←→  M3策略模型（RL/模仿学习/在线学习）
Physical AI            ←→  仿真引擎+辨识引擎+控制引擎+优化引擎+调度引擎+元件库
Cognitive AI           ←→  认知决策层（规则+大模型+模板）+预测引擎+学习引擎
HDC分层分布式控制       ←→  L0/L1/L2的MAS智能体，每个内嵌Skill
MBD基于模型的定义       ←→  S2-MBD流程Skill + 设计全环节
ODD运行设计域          ←→  S0-DET-01 ODD检查 + 三区规则
SIL/HIL在环验证        ←→  S2-SIL / S2-HIL流程Skill
                           SIL同时是RL策略的训练场
WNAL自主运行分级       ←→  S1-WNAL评估Skill

HydroOS产品            ←→  第③④层（7引擎+工具箱+三族元件库+水网实例）
                           自研核心：七大引擎+元件库（自主可控）
                           外部生态：WNTR/PySWMM/ras-commander/FloPy等
HydroMAS产品           ←→  第①②层（认知决策+技能编排）
HydroClaw产品          ←→  用户交互入口（飞书/企微 → Skill选择 → 结果展示）
```

---

## 十二、面向不同用户群体的产品-市场匹配

```
用户群体           切入角色          首选Skill层级    价值主张
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
设计院·工程师      designer_L1       S0原子          全工况校核3分钟出结果
设计院·总工        designer_L2       S1组合          方案审定前全系统验证
运管单位·值班员    operator_L0       S0原子          异常上报有数据支撑
运管单位·段长      operator_L1       S1组合          段内协调有仿真预演
运管单位·调度中心  operator_L2       S2流程          四预闭环+应急响应
高校·课程负责人    teacher_L2        S2流程(教学)    课程体系+考核标准设计
高校·主讲教师      teacher_L1        S1+S2(教学)     一键配置实验场景
高校·助教          teacher_L0        S0+S1(教学)     辅导答疑+批改辅助
高校·研究生        student_S3        S0全部+S1       独立科研全工具链
高校·本科生        student_S2        S0受限+S1教学版  苏格拉底引导式学习
高职·大专生        student_S1        操作类S0子集     步骤式操作技能训练
通识/科普          student_S0        演示类           可视化演示+兴趣激发
科研·PI            researcher_L2     S1+S2           方向把控+成果评估
科研·博士生        researcher_L1     S0+S1           独立研究全工具链
科研·硕士生        researcher_L0     S0(受限)        辅助计算+学习工具

设计院近期切入策略：
  不改流程 → 给机电骨干一个"泵选型校核"工具
  → 他用出效果 → 带动总工用"方案审查"
  → 总工体验到价值 → 推动团队级MBD变革

教学切入策略：
  先给主讲教师(L1)"一键配置实验"的便利
  → 学生体验好，教学效果提升
  → 课程负责人(L2)推动课程体系级采用
  → 大专/本科/研究生分层级全覆盖
```

