import yaml
import os
from pathlib import Path


def get_general_system_prompt():
    project_root = Path(__file__).parent
    prompt_path = project_root / "prompts" / "system_prompts" / "general_system_prompts.yaml"

    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        general_system_prompt = yaml_data.get("prompt")
    return general_system_prompt


def get_system_prompt(prompt_name, require_tool=True):
    project_root = Path(__file__).parent
    file_name = prompt_name+"_system_prompts.yaml"
    prompt_path = project_root / "prompts" / "system_prompts" / file_name
    system_prompt = ""
    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        system_prompt += yaml_data.get("prompt")

    prompt_path = project_root / "prompts" / "system_prompts" / "tools_system_prompts.yaml"
    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        system_prompt += yaml_data.get("prompt")

    return system_prompt


def get_user_prompt(prompt_name, compare=False, other_prompt_names=None):
    project_root = Path(__file__).parent
    file_name = prompt_name+"_user_prompts.yaml"
    prompt_path = project_root / "prompts" / "user_prompts" / file_name

    user_prompts = []
    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        user_prompts.append(yaml_data.get("prompt"))
        if compare:
            for prompt_name in other_prompt_names:
                user_prompts.append(yaml_data.get(prompt_name))
    return user_prompts


def get_prompt(prompt_name, compare=False, other_prompt_names=None):
    general_system_prompt = get_general_system_prompt()
    system_prompt = get_system_prompt(prompt_name)
    prompts = []
    for user_prompt in get_user_prompt(prompt_name, compare, other_prompt_names):
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


