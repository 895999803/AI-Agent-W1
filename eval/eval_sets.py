evaluation_recommend_set = [
    {
        "case_id": "paper_recommend_01",
        "input": {
            "keyword": "machine learning",
            "paper_number": 5
        },
        "expected": {
            "must_contain": ["title", "authors", "url", "published"],
            "must_not_contain": []
        }
    }
]


evaluation_reading_set = [
    {
        "case_id": "paper_reading_01",
        "input": {
            "paper_url": "https://arxiv.org/pdf/2306.04338v1",
        },
        "expected": {
            "must_contain": ["title", "author", "published", "conclusion"],
            "must_not_contain": ["i don't know"]
        }
    }
]