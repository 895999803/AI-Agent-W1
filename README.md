# 多Agent软件开发自动化流水线 - 协作关系图谱

```mermaid
graph TD
    %% 定义节点样式
    classDef agent fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef review fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef dev fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef test fill:#fce4ec,stroke:#880e4f,stroke-width:2px,color:#000
    classDef orche fill:#f3e5f5,stroke:#4a148c,stroke-width:3px,color:#000

    %% Orchestrator (总控)
    O[Orchestrator<br/>编排器<br/>default: true]::orche

    %% 需求阶段
    R1[需求Agent<br/>req_gen]::agent
    R2[需求审核Agent<br/>req_review]::review
    ReqDoc[需求文档<br/>requirements.md]

    %% 计划阶段
    P1[开发计划Agent<br/>plan_gen]::agent
    P2[计划审核Agent<br/>plan_review]::review
    PlanDoc[开发计划<br/>development-plan.md]

    %% 进度阶段
    S1[开发监督Agent<br/>prog_super]::agent
    S2[进度评估Agent<br/>prog_eval]::review
    ProgDoc[开发进度<br/>progress-plan.md]

    %% 开发阶段
    D[开发Agent<br/>developer]::dev
    Code[源代码 + 说明<br/>src/ + README.md]

    %% 代码审核
    CR[代码审核Agent<br/>code_review]::review
    CodeReview[代码审查报告<br/>code-review.md]

    %% 测试阶段
    UT[单元测试工程师<br/>unit_tester]::test
    UIT[UI测试工程师<br/>ui_tester]::test
    TestReport[测试报告<br/>test-report.md]

    %% 临时文档
    Temp1[需求审核反馈<br/>req-review-feedback.md]
    Temp2[计划审核反馈<br/>plan-review-feedback.md]
    Temp3[进度审核反馈<br/>prog-review-feedback.md]
    Temp4[代码审核反馈<br/>code-review-feedback.md]
    Temp5[测试报告<br/>test-result.md]
    ModRecord[修改记录<br/>changes-record.md]

    %% 流程连线

    %% 需求生成与审核循环
    O -->|1. 发起需求| R1
    R1 -->|2. 产出| ReqDoc
    ReqDoc -->|3. 送审| R2
    R2 -->|4. 审核意见| Temp1
    Temp1 -->|5. 反馈修改| R1
    R1 -->|审核通过?| R2
    R2 -.->|否,继续循环| Temp1
    R2 -->|是,批准| ReqDoc

    %% 计划制定与审核循环
    ReqDoc -->|6. 开始计划| P1
    P1 -->|7. 产出| PlanDoc
    PlanDoc -->|8. 送审| P2
    P2 -->|9. 审核意见| Temp2
    Temp2 -->|10. 反馈修改| P1
    P1 -->|审核通过?| P2
    P2 -.->|否,继续循环| Temp2
    P2 -->|是,批准| PlanDoc

    %% 进度计划与评估循环
    PlanDoc -->|11. 生成进度| S1
    S1 -->|12. 产出| ProgDoc
    ProgDoc -->|13. 送审| S2
    S2 -->|14. 评估意见| Temp3
    Temp3 -->|15. 反馈修改| S1
    S1 -->|审核通过?| S2
    S2 -.->|否,继续循环| Temp3
    S2 -->|是,批准| ProgDoc

    %% 开发执行阶段 (按进度分阶段)
    ProgDoc -->|16. 开始开发| D
    D -->|17. 生成代码包| Code
    Code -->|18. 送审| CR
    CR -->|19. 审核意见| Temp4
    Temp4 -->|20. 修改代码| D
    D -->|修改完成,记录| ModRecord
    D -->|审核通过?| CR
    CR -.->|否,继续循环| Temp4
    CR -->|是,通过| Code

    %% 测试阶段 (根据项目类型分支)
    Code -->|21. 选择测试类型| UT
    Code -->|21. 选择测试类型| UIT

    %% UI项目路径
    D -->|isUIProject| UIT
    UIT -->|22. 执行UI测试| TestReport
    TestReport -->|23. 测试反馈| Temp5
    Temp5 -->|24. 修复问题| D
    D -->|修复记录| ModRecord
    UIT -->|测试通过?| D
    D -.->|否,继续循环| Temp5
    UIT -->|是,完成| Code

    %% 非UI项目路径
    D -->|!isUIProject| UT
    UT -->|22. 执行单元测试| TestReport
    TestReport -->|23. 测试反馈| Temp5
    Temp5 -->|24. 修复问题| D
    D -->|修复记录| ModRecord
    UT -->|测试通过?| D
    D -.->|否,继续循环| Temp5
    UT -->|是,完成| Code

    %% 阶段推进
    TestReport -->|25. 本阶段完成,推进下一阶段| D
    D -->|26. 继续下一进度阶段| S1

    %% 虚线框表示整体流程循环
    subgraph 完整开发流水线
        R1
        R2
        P1
        P2
        S1
        S2
        D
        CR
        UT
        UIT
    end

    %% 标注
    style O fill:#9c27b0,color:#fff
    style R1 fill:#2196f3,color:#fff
    style R2 fill:#ff9800,color:#fff
    style P1 fill:#2196f3,color:#fff
    style P2 fill:#ff9800,color:#fff
    style S1 fill:#2196f3,color:#fff
    style S2 fill:#ff9800,color:#fff
    style D fill:#4caf50,color:#fff
    style CR fill:#ff9800,color:#fff
    style UT fill:#e91e63,color:#fff
    style UIT fill:#e91e63,color:#fff
```

## 图谱说明

### 核心流程阶段
1. **需求阶段** (蓝色 + 橙色审核) - 循环直到需求审核通过
2. **计划阶段** (蓝色 + 橙色审核) - 循环直到计划审核通过
3. **进度阶段** (蓝色 + 橙色审核) - 循环直到进度审核通过
4. **开发阶段** (绿色) - 按进度分模块开发
5. **审核阶段** (橙色) - 代码工程规范审核
6. **测试阶段** (粉色) - 根据UI/非UI选择测试路径

### 关键特性
- **完全自动化**: 所有Agent通过`orchestrator`编排,无需人工干预
- **迭代循环**: 每个审核阶段都是"产出→审核→反馈→修改"循环
- **分支判断**: 测试阶段根据项目类型自动选择单元测试或UI测试
- **修改记录**: 每次修改都生成`changes-record.md`追踪变更
- **文档流转**: 通过共享工作区文件传递,而非社交软件

### 文件传递路径
```
Orchestrator
  ↓ 指令
req_gen → ReqDoc → req_review → Temp1 → req_gen (循环)
  ↓ 批准
plan_gen → PlanDoc → plan_review → Temp2 → plan_gen (循环)
  ↓ 批准
prog_super → ProgDoc → prog_eval → Temp3 → prog_super (循环)
  ↓ 批准
developer (阶段1) → Code → code_review → Temp4 → developer (循环)
  ↓ 通过
(type判断) → UT/UIT → TestReport → Temp5 → developer (循环)
  ↓ 通过
developer → 推进下一阶段 → S1
```

### 配置要点
- `orchestrator`设为`default: true`,是唯一用户直接交互的Agent
- 其他9个Agent设为`default: false`,仅后台运行
- 开启`tools.agentToAgent.enabled: true`并允许所有10个Agent
- 所有共享文件放在`C:\Users\Forever\.openclaw\workspace\shared/`目录
- 状态追踪文件: `collaboration-state.json`记录当前阶段、文档版本、Agent状态
