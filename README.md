# RSS Summarizer
## Présentation

Ce petit programme permet de récupérer les derniers articles sur une durée déterminée via plusieurs flux RSS, de les résumer puis de les envoyer par mail.
Avec un cronjob hebdomadaire par exemple, ce programme permet d'automatiser complètement sa veille informative sur autant de flux que nécessaire.
Un log est généré à chaque session afin d'avoir un suivi régulier des erreurs potentielles et maintenir un suivi du nombre d'articles lus et résumés.

- Dans un premier temps, le programme récupère les derniers articles des différents flux RSS saisis dans le fichier `config.py`, avec leur titre, leur URL et leur date de publication grâce au package `feedparser`.
- Puis, les contenus sont scrapés afin d'obtenir le contenu complet des articles en format HTML grâce aux packages `requests` et `BeautifulSoup`.
- Les contenus aggrégés sont alors nettoyés puis résumés en parallèle grâce à un modèle de summarization open-source (facebook/bart-large-cnn) disponible via l'[API Hugging-Face](https://huggingface.co/facebook/bart-large-cnn) grâce au package `transformers`. Ce modèle est spécialisé dans la réalisation de court résumés journalistiques et fonctionne très bien pour du contenu en français comme en anglais.
- Enfin, les contenus résumés sont formatés de manière standardisée en Markdown avec un output en *.md dans un premier temps, puis un envoi du rapport par mail dans un second temps.

<img src="/images/report_screenshot.png" alt="Exemple d'une sortie du programme" width="60%" />

## Organisation du répértoire

Ce répértoire suit une hiérarchie classique et facile à explorer.

```
RSS_SUMMARIZER/
├── logs/
│   └── log.log                             # Fichier log
├── reports/
│   └── rapport_veille_YYYY-MM-DD.md        # Sortie du rapport
├── src/
│   ├── config.py                           # Fichier de configuration (flux RSS et ID)
│   ├── formatter.py                        # Programme de formattage des contenus agrégés
│   ├── mailer.py                           # Programme d'envoi de mail
│   ├── main.py                             # Programme principal
│   ├── rss_fetcher.py                      # Programme de récupération des flux
│   ├── scraper.py                          # Programme de data scraping
│   └── summarizer.py                       # Programme de summarization
├── .env                                    # Fichier environnement (variables sensibles, tokens, config SMTP)
├── .gitignore                              # Fichier .gitignore
├── README.md                               # Lisez-moi
└── requirements.txt                        # Liste des packages nécessaires pour le projet

```

## Installation
### Environnement virtuel

Dans un premier temps, clonez le dépôt sur votre machine locale via votre méthode préférée ou en utilisant la commande suivante :
``` git clone https://github.com/a-langlais/rss-summarizer.git ```

Ensuite, vous pouvez créer un environnement virtuel en téléchargeant spécifiquement les dépéndances Python nécessaires via le fichier `requirements.txt`.

```pip install -r requirements.txt```

### Création du fichier `.env` (indispensable)

Dans le dossier `src`, créez votre fichier `.env` avec ce contenu, complété par vos soins :

```
# Adresse email et mot de passe (idéalement un token applicatif)
EMAIL_USER=
EMAIL_PASS=

# Destinataires (séparés par des virgules si plusieurs)
EMAIL_RECIPIENTS=

# Paramètres SMTP
SMTP_SERVER=
SMTP_PORT=
```