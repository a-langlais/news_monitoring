from config import RSS_FEEDS, DAYS_BACK, SUMMARY_MODEL, EMAIL_USER, EMAIL_PASS, EMAIL_RECIPIENTS, SMTP_SERVER, SMTP_PORT
from rss_fetcher import get_recent_articles
from scraper import scrape_article_content
from summarizer import ArticleSummarizer
from formatter import format_articles_markdown
from mailer import send_email_report

from datetime import datetime, timedelta
import time
import logging
from pathlib import Path

# Création des dossiers logs et reports
Path("logs").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

# Configuration du logger
logging.basicConfig(
    filename="logs/veille.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger()


def main():
    print("🚀 Lancement de la veille automatique...\n")
    logger.info("=== DÉBUT DU SCRIPT ===")

    # 1. Récupération des articles RSS récents
    since_date = datetime.now() - timedelta(days=DAYS_BACK)
    print(f"📥 Récupération des articles depuis le {since_date.strftime('%d/%m/%Y')}...")
    logger.info(f"Récupération des articles depuis le {since_date.strftime('%d/%m/%Y')}...")

    try:
        articles = get_recent_articles(RSS_FEEDS, DAYS_BACK)
        print(f"🔎 {len(articles)} articles trouvés.")
        logger.info(f"{len(articles)} articles récupérés depuis les flux RSS.")
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des flux RSS : {e}")
        return

    # 2. Scraping + 3. Résumé
    summarizer = ArticleSummarizer(model_name=SUMMARY_MODEL)
    summarized_articles = []

    for idx, article in enumerate(articles, 1):
        logger.info(f"Traitement article : {article['title']}")
        print(f"📰 ({idx}/{len(articles)}) Traitement de : {article['title'][:60]}...")

        # Scraping
        content = scrape_article_content(article['link'])
        if not content:
            msg = f"Article vide ou inaccessible : {article['link']}"
            print(f"⚠️ {msg}")
            logger.warning(msg)
            continue

        # Résumé
        summary = summarizer.summarize(content)
        if not summary:
            msg = f"Résumé non généré pour l'article : {article['link']}"
            print(f"⚠️ {msg}")
            logger.warning(msg)
            continue

        article["summary"] = summary
        summarized_articles.append(article)

        time.sleep(1)  # Pour éviter les requêtes trop rapprochées

    print(f"✅ {len(summarized_articles)} articles résumés avec succès.\n")
    logger.info(f"{len(summarized_articles)} articles résumés avec succès.")

    # 4. Formatage du rapport Markdown
    markdown_report = format_articles_markdown(summarized_articles)

    # 4.1. Sauvegarde locale
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    filename = f"rapport_veille_{datetime.now().strftime('%Y-%m-%d')}.md"
    report_path = report_dir / filename

    try:
        with report_path.open("w", encoding="utf-8") as f:
            f.write(markdown_report)
        print(f"🗂️ Rapport sauvegardé localement : {report_path.resolve()}\n")
        logger.info(f"Rapport sauvegardé dans {report_path.resolve()}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du rapport local : {e}")
        return

    # 5. Envoi par email
    subject = f"🗞️ Rapport de veille – Semaine du {datetime.now().strftime('%d/%m/%Y')}"
    try:
        send_email_report(
            subject=subject,
            markdown_content=markdown_report,
            sender_email=EMAIL_USER,
            sender_password=EMAIL_PASS,
            recipients=EMAIL_RECIPIENTS,
            smtp_server=SMTP_SERVER,
            smtp_port=SMTP_PORT
        )
        logger.info(f"Email envoyé à {EMAIL_RECIPIENTS}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email : {e}")
        return

    logger.info("=== FIN DU SCRIPT ===\n")


if __name__ == "__main__":
    main()
