import logging
from transformers import pipeline
from typing import Optional

logger = logging.getLogger(__name__)

class ArticleSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn", max_input_length: int = 1024):
        """
        Initialise le modèle de résumé.

        Args:
            model_name (str): Nom du modèle HuggingFace à utiliser.
            max_input_length (int): Nombre maximal de tokens en entrée (selon le modèle).
        """
        self.model = pipeline("summarization", model=model_name)
        self.max_input_length = max_input_length

    def summarize(self, text: str) -> Optional[str]:
        """
        Résume un article en texte brut avec une longueur de résumé adaptée dynamiquement.

        Args:
            text (str): Texte à résumer.

        Returns:
            Optional[str]: Résumé généré, ou None si problème.
        """
        if not text or len(text.strip()) < 100:
            logger.warning("Texte trop court pour être résumé.")
            return None

        try:
            input_text = text.strip()[:self.max_input_length]
            word_count = len(input_text.split())

            # Longueurs de résumé dynamiques
            if word_count > 1500:
                min_len, max_len = 350, 500
            elif word_count > 1000:
                min_len, max_len = 250, 400
            elif word_count > 600:
                min_len, max_len = 180, 300
            else:
                min_len, max_len = 80, 150

            summary = self.model(
                input_text,
                max_length=max_len,
                min_length=min_len,
                do_sample=False,
                num_beams=4
            )[0]["summary_text"]

            logger.info(f"Résumé généré avec succès ({len(summary.split())} mots).")
            return summary.strip()

        except Exception as e:
            logger.error(f"Erreur lors du résumé de l'article : {e}")
            return None
