summarize_user_prompts = {

    "task": "请总结下面的内容：",
    "content": {},
    "constraints": {
        1: "用简单的话说明整体在讲什么。",
        2: "提炼 3～5 条最重要的信息。",
        3: "不加入原文没有的内容。"
    },
    "output": "使用条目形式输出。"
}

extraction_user_prompts = {

    "task": "请从下面的内容中抽取信息：",
    "content": {},
    "constraints": {
        1: "时间，",
        2: "涉及对象（人 / 产品 / 系统），",
        3: "明确提出的需求，",
        4: "已提到的问题或风险，",
    },
    "output": "请使用列表形式输出。"
}

comparison_user_prompts = {

    "task": "请对比以下内容：",
    "content": {"1": {}, "2": {}},
    "constraints": {
        1: "各自的优点，",
        2: "各自的不足，",
        3: "各自适合的场景，",
        4: "在什么情况下选择 1 或 2，",
    },
    "output": "请用表格或分点方式输出。"
}

plan_user_prompts = {

    "task": "请生成一个执行计划：",
    "content": {"plan": {}},
    "constraints": {
        1: "将目标拆分为多个步骤，",
        2: "每一步说明要做什么，",
        3: "写清楚每一步完成后的结果，",
        4: "步骤顺序要合理，",
    },
    "output": "请用编号列表输出。"
}

examine_user_prompts = {

    "task": "请检查下面的内容：",
    "content": {},
    "constraints": {
        1: "是否存在明显错误或不合理之处，",
        2: "是否有容易引发问题的地方，",
        3: "是否有改进建议，",
        4: "整体质量的简要评价，",
    },
    "output": "请使用通俗语言说明。"
}
