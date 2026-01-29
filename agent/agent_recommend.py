
import logging
import os
import sys
import json
import model.model as m
import prompt_lab.analysis_prompt as ap
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import tools.tools as t

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename='agent_recommend.log',
    filemode='a',
    encoding='utf-8'
)


class State:
    INIT = "INIT"
    SEARCH = "SEARCH"
    FETCH = "FETCH"
    SUMMARIZE = "SUMMARIZE"
    DONE = "DONE"
    FAILED = "FAILED"


class AgentRecommend:
    def __init__(self, parameters):
        self.state = State.INIT
        self.context = {
            "keyword": parameters["keyword"],
            "paper_number": parameters["paper_number"],
            "papers": None,
            "query": None,
            "prompt": None,
            "model_response": None,
            "tool_calling": False,
            "retry": 0
        }
        self.max_retry = 3

    def get_result(self):
        return {
            "state": self.state,
            "summary": self.context.get("model_response"),
            "retry": self.context.get("retry"),
            "prompt": self.context.get("prompt")
        }

    def log(self, msg):
        logging.info(f"[{self.state}] {msg}")

    def run(self):
        while self.state not in (State.DONE, State.FAILED):
            try:
                if self.state == State.INIT:
                    self.step_init()
                elif self.state == State.SEARCH:
                    self.step_search()
                elif self.state == State.FETCH:
                    self.step_fetch()
                elif self.state == State.SUMMARIZE:
                    self.step_summarize()
            except Exception as e:
                self.handle_failure(e)

        self.log("Agent finished")

    # -------- 每个状态一步 --------

    def step_init(self):
        self.log("Initializing")
        self.state = State.SEARCH
        self.context["query"] = "请帮我推荐" + str(self.context["paper_number"]) + \
                                "篇与" + self.context["keyword"] + "相关的论文。"
        self.log(f"Query: {self.context['query']}")

    def step_search(self):
        self.log(f"Searching papers for {self.context['keyword']}")
        prompts = ap.get_prompt("summary")[0]
        prompts = prompts.replace("请总结下面的内容", self.context["query"])
        tools_prompts = ap.get_tools_prompts()
        prompts += tools_prompts
        self.log(f"Prompts: {prompts}")
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
        self.log(f"Model response: {response}")
        if "I need use tools" in response:
            self.context["model_response"] = json.loads(response)
            self.context["tool_calling"] = True
            self.state = State.FETCH
        else:
            self.context["model_response"] = response
            self.context["tool_calling"] = False
            self.state = State.DONE

    def step_fetch(self):
        self.log("Fetching paper content")
        if self.context["tool_calling"]:
            if self.context["model_response"]["tool"] == "arxiv search":
                self.log(f"Tool calling:{self.context["model_response"]["tool"]}")
                self.log(f"Tool Parameters:{self.context["keyword"], self.context["paper_number"]}")
                self.context["papers"] = t.get_arxiv_content(self.context["keyword"],
                                                             self.context["paper_number"],
                                                             tostring=True)
                self.context["prompt"] = ap.get_prompt("summary",
                                                       user_prompt_name="prompt_arxiv",
                                                       require_tool=False)[0]
                self.log(f"Content:{self.context["papers"]}")
            else:
                self.log(f"未知的方法调用:{self.context["model_response"]["tool"]}")
                raise Exception("未知的方法调用:" + self.context["model_response"]["tool"])
            self.state = State.SUMMARIZE

    def step_summarize(self):
        self.log("Summarizing paper")
        self.log(f"Prompt: {self.context['prompt']}")
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self.context["prompt"]
                    },
                    {
                        "type": "text",
                        "text": self.context["papers"]
                    }
                ]
            }
        ]
        response = m.model(messages)
        # data = json.loads(response)
        self.log(f"Model response: {response}")
        '''
        for i in range(len(data)):
            authors = ""
            for author in data[i]['authors']:
                authors += author + "\n"
            data[i]['authors'] = authors
        '''
        self.context["model_response"] = response
        self.state = State.DONE

    # -------- 失败恢复 --------

    def handle_failure(self, error):
        self.context["retry"] += 1
        self.log(f"Error: {error}, retry={self.context['retry']}")

        if self.context["retry"] >= self.max_retry:
            self.state = State.FAILED
            self.log("Max retry reached, giving up")
        else:
            self.log("Retrying current state")


if __name__ == '__main__':

    agent = Agent_Recommend({"keyword": "machine learning", "paper_number": 5})
    agent.run()

