import sys

import requests
import arxiv
from arxiv import Search
from bs4 import BeautifulSoup


def get_web_content(url):

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.text if soup.title else "No title"
    text = soup.get_text(separator=" ",strip=True)

    return {
        "title": title,
        "text": text
    }


def get_arxiv_content(keyword, paper_number=5, tostring=True):

    search = Search(
        query=keyword,
        max_results=paper_number,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = search.results()

    if tostring:
        papers = ""
        for paper in results:
            papers += "Title: " + str(paper.title) + "\n" +\
                           "Summary: " + str(paper.summary) + "\n" +\
                           "Published: " + str(paper.published) + "\n" +\
                           "Authors: " + str(paper.authors) + "\n" +\
                           "Url: " + paper.pdf_url + "\n"
        return papers
    else:
        papers = []
        for paper in results:
            papers.append({"title": paper.title,
                           "summary": paper.summary,
                           "published": paper.published,
                           "authors": paper.authors,
                           "url": paper.pdf_url})
        return papers


if __name__ == "__main__":
    get_arxiv_content("machine learning")
