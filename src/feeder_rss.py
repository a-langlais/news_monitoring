import feedparser
from datetime import datetime, timedelta
import csv

def parse_rss(url, start_date, end_date):
    """
    Récupère et filtre les articles d'un flux RSS entre deux dates, puis les enregistre dans un fichier CSV.

    :param url: Lien du flux RSS
    :param start_date: Date de début (format YYYY-MM-DD)
    :param end_date: Date de fin (format YYYY-MM-DD)
    :return: Liste des articles filtrés
    """
    try:
        feed = feedparser.parse(url)
        articles = []

        # Conversion des dates
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        for entry in feed.entries:
            # Vérifier l'existence de published_parsed
            if hasattr(entry, 'published_parsed'):
                # Convertir la date de publication en format datetime
                pub_date = datetime(*entry.published_parsed[:6])

                if start_dt <= pub_date <= end_dt:
                    articles.append({
                        "title": entry.title if hasattr(entry, 'title') else "No title",
                        "link": entry.link if hasattr(entry, 'link') else "",
                        "summary": entry.summary if hasattr(entry, 'summary') else "",
                        "published": pub_date.strftime("%Y-%m-%d")
                    })

        return articles

    except Exception as e:
        print(f"Erreur lors de la récupération des articles : {e}")
        return []
