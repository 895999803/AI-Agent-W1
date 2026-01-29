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





