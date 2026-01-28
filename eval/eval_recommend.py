import time
import agent.agent_recommend as are
import eval_sets as es


def assert_contains_for_recommend(papers, keywords):
    if not papers:
        return False
    for paper in papers:
        for keyword in keywords:
            if keyword not in paper:
                return False
    return True


def assert_not_contains_for_recommend(papers, keywords):
    if not papers:
        return False
    for paper in papers:
        for keyword in keywords:
            if keyword in paper:
                return False
    return True


def score_for_recommend(summary):

    if not summary:
        return 0
    score = 1
    for item in summary:
        if len(item["title"].split(" ")) < 20:
            score += 1
        else:
            score -= 1
    return score


def run_evaluation(agent_class, eval_case):
    start = time.time()
    agent = agent_class(eval_case["input"])
    agent.run()
    result = agent.get_result()
    summary = result["summary"]
    expected = eval_case["expected"]

    assertions = {
        "must_contain": assert_contains_for_recommend(summary, expected["must_contain"]),
        "must_not_contain": assert_not_contains_for_recommend(summary, expected["must_not_contain"])
    }

    score = score_for_recommend(summary)

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
        result = run_evaluation(are.Agent_Recommend, case)
        results.append(result)
    return results


if __name__ == '__main__':

    r = run_evaluation(are.Agent_Recommend, es.evaluation_recommend_set[0])
    for item in r:
        print(item, ": ", r[item])





