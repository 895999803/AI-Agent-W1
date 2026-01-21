import requests
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

