import yaml


def get_general_system_prompt():
    prompt_path = "./prompts/system_prompts/general_system_prompts.yaml"
    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        general_system_prompt = yaml_data.get("prompt")
    return general_system_prompt


def get_system_prompt(prompt_name):
    prompt_path = "./prompts/system_prompts/"+prompt_name+"_system_prompts.yaml"
    with open(prompt_path, 'r', encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        system_prompt = yaml_data.get("prompt")
    return system_prompt


def get_user_prompt(prompt_name, compare=False, other_prompt_names=None):

    prompt_path = "./prompts/user_prompts/"+prompt_name+"_user_prompts.yaml"
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

