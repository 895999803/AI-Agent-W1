import yaml
import os
from pathlib import Path


def get_general_system_prompt(prompt_name="prompt"):
    project_root = Path(__file__).parent
    prompt_path = project_root / "prompts" / "system_prompts" / "general_system_prompts.yaml"

    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        general_system_prompt = yaml_data.get(prompt_name)
    return general_system_prompt


def get_system_prompt(prompt_type, prompt_name="prompt", require_tool=True):
    project_root = Path(__file__).parent
    file_name = prompt_type+"_system_prompts.yaml"
    prompt_path = project_root / "prompts" / "system_prompts" / file_name
    system_prompt = ""
    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        system_prompt += yaml_data.get(prompt_name)
    if require_tool:
        prompt_path = project_root / "prompts" / "system_prompts" / "tools_system_prompts.yaml"
        with open(prompt_path, 'r', encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
            system_prompt += yaml_data.get(prompt_name)

    return system_prompt


def get_user_prompt(prompt_type, prompt_name="prompt", compare=False, other_prompt_names=None):
    project_root = Path(__file__).parent
    file_name = prompt_type+"_user_prompts.yaml"
    prompt_path = project_root / "prompts" / "user_prompts" / file_name

    user_prompts = []
    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        user_prompts.append(yaml_data.get(prompt_name))
        if compare:
            for p_name in other_prompt_names:
                user_prompts.append(yaml_data.get(p_name))
    return user_prompts


def get_prompt(prompt_type, user_prompt_name="prompt", compare=False, other_prompt_names=None, require_tool=True):
    general_system_prompt = get_general_system_prompt()
    system_prompt = get_system_prompt(prompt_type, require_tool=require_tool)
    prompts = []
    for user_prompt in get_user_prompt(prompt_type, prompt_name=user_prompt_name,
                                       compare=compare, other_prompt_names=other_prompt_names):
        prompts.append(general_system_prompt+system_prompt+user_prompt)
    return prompts


def get_tools_prompts():
    project_root = Path(__file__).parent
    prompt_path = project_root / "prompts" / "tools_prompts" / "tools_prompts.yaml"

    tools_prompts = ""
    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        for tool in yaml_data:
            tools_prompts += "工具名称：" + yaml_data[tool]["name"] \
                             + "工具描述：" + yaml_data[tool]["description"] \
                             + "工具参数：" + yaml_data[tool]["parameters"] + "\n"
    return tools_prompts


def get_score_prompts(prompt_type, prompt_name="prompt"):

    project_root = Path(__file__).parent
    file_name = prompt_type + "_score_prompts.yaml"
    prompt_path = project_root / "prompts" / "score_prompts" / file_name
    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        score_prompts = yaml_data.get(prompt_name)
    return score_prompts



