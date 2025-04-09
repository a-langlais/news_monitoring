import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List
import markdown
import logging

logger = logging.getLogger(__name__)

def send_email_report(
    subject: str,
    markdown_content: str,
    sender_email: str,
    sender_password: str,
    recipients: List[str],
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587,
):
    """
    Envoie un e-mail contenant le rapport en HTML (généré depuis Markdown).

    Args:
        subject (str): Sujet du mail.
        markdown_content (str): Contenu Markdown à envoyer.
        sender_email (str): Adresse e-mail de l'expéditeur.
        sender_password (str): Mot de passe ou token SMTP.
        recipients (List[str]): Liste d'adresses e-mail des destinataires.
        smtp_server (str): Serveur SMTP.
        smtp_port (int): Port SMTP.
    """
    try:
        html_content = markdown.markdown(markdown_content, extensions=["extra", "sane_lists"])

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipients)

        # Ajoute la version texte et HTML
        msg.attach(MIMEText(markdown_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        logger.info("Connexion au serveur SMTP...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, msg.as_string())
        logger.info("✅ Rapport envoyé avec succès.")

    except smtplib.SMTPAuthenticationError:
        logger.error("❌ Échec de l'authentification SMTP : vérifie ton email/mot de passe ou utilise un mot de passe d'application Gmail.")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'envoi de l'email : {e}")
