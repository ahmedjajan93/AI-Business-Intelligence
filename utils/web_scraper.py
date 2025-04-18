# 📁 File: utils/web_scraper.py
import requests
from bs4 import BeautifulSoup
from langchain.schema import Document


def scrape_website(url: str) -> list[Document]:
    """
    Scrape textual content from a webpage and split into Document chunks.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.find_all(["p", "li", "span", "h1", "h2", "h3"])
    visible_text = ' '.join(tag.get_text(separator=" ", strip=True) for tag in tags if tag.get_text())

    chunks = [visible_text[i:i+1000] for i in range(0, len(visible_text), 1000)]
    return [Document(page_content=chunk, metadata={"source": url}) for chunk in chunks]
