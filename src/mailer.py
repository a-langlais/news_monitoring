import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List
import markdown

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
    # Conversion Markdown → HTML
    html_content = markdown.markdown(markdown_content, extensions=["extra", "sane_lists"])

    # Création du message multipart
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)

    # Attachments : version texte brut + HTML
    part1 = MIMEText(markdown_content, "plain")
    part2 = MIMEText(html_content, "html")

    msg.attach(part1)
    msg.attach(part2)

    # Envoi
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, msg.as_string())
            print("✅ Rapport envoyé avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {e}")
