import sys

import requests
import arxiv
from arxiv import Search
from bs4 import BeautifulSoup
import requests
import fitz  # PyMuPDF
import io


def get_web_content(url):

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.text if soup.title else "No title"
    text = soup.get_text(separator=" ",strip=True)
    return {
        "title": title,
        "text": text
    }


def get_arxiv_paper(url):
    paper_url = url + ".pdf"
    response = requests.get(paper_url)
    response.raise_for_status()

    pdf_stream = io.BytesIO(response.content)
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


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
            papers += "title: " + str(paper.title) + "\n" + \
                      "authors: " + str(paper.authors) + "\n" + \
                      "published: " + str(paper.published) + "\n" +\
                      "url: " + paper.pdf_url + "\n" + \
                      "category:" + paper.primary_category + "\n" # + \
                      # "abstract: " + str(paper.summary) + "\n"
        return papers
    else:
        papers = []
        for paper in results:
            papers.append({"title": paper.title,
                           "summary": paper.summary,
                           "published": paper.published,
                           "authors": paper.authors,
                           "url": paper.pdf_url,
                           "category": paper.primary_category,
                           "abstract": paper.summary})
        return papers


if __name__ == "__main__":
    # get_arxiv_content("machine learning")
    print(get_arxiv_paper("https://arxiv.org/pdf/2306.04338v1"))
