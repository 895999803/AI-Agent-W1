import json
import time
import eval_score as sc
import assertion.assert_reading as assert_reading
import assertion.assert_recommend as assert_recommend
import agent.agent_reading as ar
import agent.agent_recommend as arc
import eval_sets as es


def run_evaluation(agent_class, eval_case, assert_contains, assert_not_contains):
    start = time.time()
    agent = agent_class(eval_case["input"])
    agent.run()
    result = agent.get_result()
    summary = result["summary"]
    expected = eval_case["expected"]

    assertions = {
        "must_contain": assert_contains(summary, expected["must_contain"]),
        "must_not_contain": assert_not_contains(summary, expected["must_not_contain"])
    }
    score = sc.eval_score(result)
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


def eval_all(agent, cases, assert_contains, assert_not_contains):
    results = []
    for case in cases:
        result = run_evaluation(agent, case, assert_contains, assert_not_contains)
        results.append(result)
    return results


def eval_recommend():
    r = run_evaluation(arc.AgentRecommend,
                       es.evaluation_recommend_set[0],
                       assert_recommend.assert_contains_for_recommend,
                       assert_recommend.assert_not_contains_for_recommend)
    for key in r:
        print(key, ": ", r[key])


def eval_reading():
    r = run_evaluation(ar.AgentReading,
                       es.evaluation_reading_set[0],
                       assert_reading.assert_contains_for_reading,
                       assert_reading.assert_not_contains_for_reading)
    for key in r:
        print(key, ": ", r[key])


if __name__ == '__main__':

    eval_recommend()
    eval_reading()



