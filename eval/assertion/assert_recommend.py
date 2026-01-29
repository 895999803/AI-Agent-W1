import json


def assert_contains_for_recommend(summery, keywords):
    if not summery:
        return False

    papers = json.loads(summery)
    for paper in papers:
        for keyword in keywords:
            if keyword not in paper:
                return False
    return True


def assert_not_contains_for_recommend(summery, keywords):
    if not summery:
        return False

    papers = json.loads(summery)
    for paper in papers:
        for keyword in keywords:
            if keyword in paper:
                return False
    return True







