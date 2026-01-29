import prompt_lab.analysis_prompt as ap
import model.score_model as sm


def eval_score(model_response):

    prompts = ((ap.get_general_system_prompt() +
               ap.get_system_prompt(prompt_type="score", require_tool=False)) +
               ap.get_score_prompts("recommend"))
    context = "用户问题：" + model_response["prompt"] + "模型输出：" + model_response["summary"]
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompts
                },
                {
                    "type": "text",
                    "text": context
                }
            ]
        }
    ]
    response = sm.model(messages)
    return response
