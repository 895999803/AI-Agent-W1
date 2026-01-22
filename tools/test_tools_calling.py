import model.model as m
import prompt_lab.analysis_prompt as ap
import tools as t
import json


def web_search_calling(web_url):
    content = t.get_arxiv_content(web_url)["text"]
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


def arxiv_search_calling(keyword, paper_number):
    content = t.get_arxiv_content(keyword, paper_number)
    prompts = ap.get_prompt("summary", user_prompt_name="prompt_arxiv", require_tool=False)[0]
    # print(content)
    # print(prompts)
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
    # print(response)
    return response


def test_tool_calling():

    prompts = ap.get_prompt("summary")[0]
    # prompts = prompts.replace("请总结下面的内容", "帮我总结一下这个网页的内容：https://cloud.tencent.com/developer/article/2124888")
    prompts = prompts.replace("请总结下面的内容", "帮我推荐几篇和机器学习相关的论文")
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
        if "yes" in data["I need use tools"]:
            if data["tool"] == "web search":
                return web_search_calling(data["parameters"]["url"])
            if data["tool"] == "arxiv search":
                return arxiv_search_calling(data["parameters"]["keyword"], data["parameters"]["number"])
    return response


if __name__ == '__main__':
    r = test_tool_calling()
    print(r)
