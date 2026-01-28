
import logging
import os
import sys
import model.model as m
import prompt_lab.analysis_prompt as ap

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import tools.tools as t

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename='agent_reading.log',
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


class Agent_Reading:
    def __init__(self, parameters):
        self.state = State.INIT
        self.context = {
            "paper_url": parameters["paper_url"],
            "prompt": None,
            "paper_content": None,
            "model_response": None,
            "retry": 0
        }
        self.max_retry = 3

    def get_result(self):
        return {
            "state": self.state,
            "summary": self.context.get("model_response"),
            "retry": self.context.get("retry")
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
        self.log(f"Query: {self.context['paper_url']}")

    def step_search(self):
        self.log(f"Searching papers for {self.context['paper_url']}")
        self.context["prompt"] = ap.get_prompt("summary",
                                               user_prompt_name="prompt_arxiv_paper",
                                               require_tool=False)[0]
        self.log(f"Prompts: {self.context["prompt"]}")
        self.state = State.FETCH

    def step_fetch(self):
        self.log("Fetching paper content")
        self.context["paper_content"] = t.get_arxiv_paper(self.context['paper_url'])
        self.log(f"Content:{self.context["paper_content"]}")
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
                        "text": self.context['prompt']
                    },
                    {
                        "type": "text",
                        "text": self.context["paper_content"]
                    }
                ]
            }
        ]
        self.context["model_response"] = m.model(messages)
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

    agent = Agent_Reading({"paper_url": "https://arxiv.org/pdf/2306.04338v1"})
    agent.run()


