import requests
from xml.etree import ElementTree
import re
from datetime import datetime

CURRENT_YEAR = datetime.utcnow().year


def extract_year(article):
    """
    Robust and SAFE publication year extraction.
    Prevents future-year artifacts (e.g., 2026).
    """

    # 1️⃣ Journal Issue Year (MOST RELIABLE)
    year = article.findtext(".//Journal/JournalIssue/PubDate/Year")
    if year and year.isdigit():
        y = int(year)
        if y <= CURRENT_YEAR:
            return y

    # 2️⃣ MedlineDate (e.g. "2018 Jan-Feb")
    medline = article.findtext(".//Journal/JournalIssue/PubDate/MedlineDate")
    if medline:
        match = re.search(r"(19|20)\d{2}", medline)
        if match:
            y = int(match.group())
            if y <= CURRENT_YEAR:
                return y

    # 3️⃣ ArticleDate (ONLINE-FIRST → LAST RESORT)
    year = article.findtext(".//ArticleDate/Year")
    if year and year.isdigit():
        y = int(year)
        if y <= CURRENT_YEAR:
            return y

    return None


def fetch_pubmed_articles(query, max_results=20):
    """
    Fetch PubMed articles with safe publication years
    """

    search_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=pubmed&term={query}&retmax={max_results}&retmode=json"
    )

    r = requests.get(search_url, timeout=10)
    r.raise_for_status()

    ids = r.json().get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []

    fetch_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        f"?db=pubmed&id={','.join(ids)}&retmode=xml"
    )

    r = requests.get(fetch_url, timeout=10)
    r.raise_for_status()

    root = ElementTree.fromstring(r.content)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="").strip()

        abstract_parts = [
            a.text.strip()
            for a in article.findall(".//AbstractText")
            if a.text
        ]
        abstract = " ".join(abstract_parts)

        pmid = article.findtext(".//PMID", default="")
        year = extract_year(article)

        if not abstract or not year:
            continue

        articles.append({
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
            "year": year
        })

    return articles
