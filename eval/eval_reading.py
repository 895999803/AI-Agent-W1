import time
import agent.agent_reading as ar
import eval_sets as es


def assert_contains_for_reading(paper, keywords):
    if not paper:
        return False
    text = paper.lower()
    for keyword in keywords:
        if keyword not in text:
            return False
    return True


def assert_not_contains_for_reading(paper, keywords):
    if not paper:
        return False
    text = paper.lower()
    for keyword in keywords:
        if keyword in text:
            return False
    return True


def score_for_reading(summary):

    if not summary:
        return 0
    score = 1
    return score


def run_evaluation(agent_class, eval_case):
    start = time.time()
    agent = agent_class(eval_case["input"])
    agent.run()
    result = agent.get_result()
    summary = result["summary"]
    expected = eval_case["expected"]

    assertions = {
        "must_contain": assert_contains_for_reading(summary, expected["must_contain"]),
        "must_not_contain": assert_not_contains_for_reading(summary, expected["must_not_contain"])
    }

    score = score_for_reading(summary)

    status = "PASS" if all(assertions.values()) else "FAIL"

    return {
        "case_id": eval_case["case_id"],
        "status": status,
        "assertions": assertions,
        "score": score,
        "latency_ms": int((time.time() - start) * 1000),
        "retry": result["retry"],
        "output": summary
    }


def eval_all(cases):
    results = []
    for case in cases:
        result = run_evaluation(ar.Agent_Reading, case)
        results.append(result)
    return results


if __name__ == '__main__':

    r = run_evaluation(ar.Agent_Reading, es.evaluation_reading_set[0])
    for item in r:
        print(item, ": ", r[item])





