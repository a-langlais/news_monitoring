import feedparser
from datetime import datetime, timedelta
from typing import List, Dict

def get_recent_articles(rss_urls: List[str], days_back: int = 7) -> List[Dict]:
    """
    Récupère les articles récents à partir d'une liste de flux RSS.

    Args:
        rss_urls (List[str]): Liste d'URLs de flux RSS.
        days_back (int): Nombre de jours en arrière à considérer comme "récent".

    Returns:
        List[Dict]: Liste de dictionnaires contenant les métadonnées des articles.
    """
    cutoff = datetime.now() - timedelta(days=days_back)
    all_articles = []

    for url in rss_urls:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            # Certains flux utilisent 'updated' ou 'published'
            published_parsed = (
                getattr(entry, "published_parsed", None) or
                getattr(entry, "updated_parsed", None)
            )

            if not published_parsed:
                continue

            published_dt = datetime(*published_parsed[:6])
            if published_dt >= cutoff:
                article = {
                    "title": getattr(entry, "title", "Sans titre"),
                    "link": getattr(entry, "link", ""),
                    "published": published_dt,
                    "source": feed.feed.get("title", "Source inconnue"),
                }
                all_articles.append(article)

    return all_articles
