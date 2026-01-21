import model.model as m
import prompt_lab.analysis_prompt as ap
import tools.web_search as ws
import json


def test_tool_calling():

    prompts = ap.get_prompt("summary")[0]
    prompts = prompts.replace("请总结下面的内容", "帮我总结一下这个网页的内容：https://cloud.tencent.com/developer/article/2124888")
    tools_prompts = ap.get_tools_prompts()
    prompts += tools_prompts
    messages = [
        {
            "role": "user",
            "content": [
                {
                        "type": "text",
                        "text": prompts
                }
            ]
        }
    ]

    response = m.model(messages)
    if "I need use tools" in response:
        data = json.loads(response)
        if data["tool"] == "web search":
            content = ws.get_web_content(data["parameters"]["url"])["text"]
            prompts = ap.get_prompt("summary")[0]
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
                            "text": content
                        }
                    ]
                }
            ]
            response = m.model(messages)
            return response
    return response


if __name__ == '__main__':
    r = test_tool_calling()
    print(r)
