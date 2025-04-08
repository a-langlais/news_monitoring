import requests
from bs4 import BeautifulSoup
from typing import Optional


def scrape_article_content(url: str, min_length: int = 500) -> Optional[str]:
    """
    Scrape le contenu principal (texte) d’un article à partir de son URL.

    Args:
        url (str): URL de l’article.
        min_length (int): Longueur minimale de texte pour valider le résultat.

    Returns:
        Optional[str]: Texte brut de l’article, ou None si échec.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # On collecte tous les paragraphes visibles
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs)
        cleaned_text = text.strip()

        if len(cleaned_text) < min_length:
            return None

        return cleaned_text

    except Exception as e:
        print(f"[Erreur scraping] {url} — {e}")
        return None
