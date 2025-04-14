# --- CONFIG ---
import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

### --- Email --- ###
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

### --- RSS Feeds --- ###
RSS_FEEDS = [
    "https://www.databricks.com/fr/feed",       # Databricks
    "hhttps://blogs.microsoft.com/AI/feed/",    # Microsoft AI Blog
    "https://hf.co/blog/feed.xml",              # Hugging-Face Blog
    "https://jamesg.blog/hf-papers.xml",        # Hugging-Face Papers
    "theverge.com/rss/index.xml",               # The Verge
    "http://www.kdnuggets.com/feed"             # KDnuggets
    "https://techcrunch.com/feed/",             # TechCrunch
    "https://towardsdatascience.com/feed",      # Towards Data Science
    "https://www.cnil.fr/fr/rss.xml",           # CNIL
    "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",      # ScienceDaily
]

### --- Autres paramètres --- ###
DAYS_BACK = 7  # Nombre de jours pour filtrer les articles récents
SUMMARY_MODEL = "facebook/bart-large-cnn"
