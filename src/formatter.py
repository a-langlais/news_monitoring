from typing import List, Dict
from datetime import datetime


def format_articles_markdown(articles: List[Dict]) -> str:
    """
    Formate une liste d'articles résumés en Markdown.

    Args:
        articles (List[Dict]): Liste d'articles enrichis avec leur résumé.

    Returns:
        str: Texte au format Markdown prêt à être envoyé ou affiché.
    """
    if not articles:
        return "Aucun article trouvé cette semaine."

    # Tri par date décroissante
    articles.sort(key=lambda a: a.get("published", datetime.min), reverse=True)

    md_lines = [
        "# 📰 Rapport de veille hebdomadaire",
        f"_Généré automatiquement le {datetime.now():%d/%m/%Y}_\n"
    ]

    for article in articles:
        title = article.get("title", "Sans titre")
        link = article.get("link", "")
        published = article.get("published")
        published_str = f"{published:%d/%m/%Y}" if published else "Date inconnue"
        source = article.get("source", "Source inconnue")
        summary = article.get("summary", "Pas de résumé disponible.")

        md_lines.append(f"## [{title}]({link})")
        md_lines.append(f"**🕓 Date** : {published_str}  \n**📡 Source** : {source}")
        md_lines.append("")
        md_lines.append(f"> {summary}")
        md_lines.append("---")

    return "\n".join(md_lines)
