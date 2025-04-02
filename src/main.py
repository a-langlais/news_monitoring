import feedparser
import csv
from datetime import datetime, timedelta
import os

from feeder_rss import *

end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days = 7)).strftime("%Y-%m-%d")

rss_urls = ["https://hf.co/blog/feed.xml",          # Hugging-Face Blog
            "https://jamesg.blog/hf-papers.xml",    # Hugging-Face Papers
            "theverge.com/rss/index.xml",           # The Verge
            "http://www.kdnuggets.com/feed"         # KDnuggets
            "https://techcrunch.com/feed/",         # TechCrunch
            "https://www.databricks.com/fr/feed",   # Databricks
            ]

articles = []
for flux in rss_urls:
    news = parse_rss(flux, start_date, end_date)
    articles.extend(news) # extend au lieu de append pour éviter les listes imbriquées

# Utiliser un ensemble pour suivre les articles déjà ajoutés
seen_articles = set()
unique_articles = []

for article in articles:
    if article['link'] not in seen_articles:
        seen_articles.add(article['link'])
        unique_articles.append(article)

# Écrire les articles dans un fichier CSV
output_directory = "data"  # Assurez-vous que ce dossier existe ou sera créé
os.makedirs(output_directory, exist_ok=True)
csv_filename = os.path.join(output_directory, f"articles_{end_date}.csv")

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["title", "link", "summary", "published"])
    writer.writeheader()
    for article in unique_articles:
        writer.writerow(article)

print(f"Articles enregistrés dans {csv_filename}")