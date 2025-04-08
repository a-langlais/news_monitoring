from transformers import pipeline
from typing import Optional


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
        Résume un article en texte brut.

        Args:
            text (str): Texte à résumer.

        Returns:
            Optional[str]: Résumé généré, ou None si problème.
        """
        if not text or len(text.strip()) < 100:
            return None

        try:
            # Tronquage si nécessaire (le modèle ne gère qu'un nombre limité de tokens)
            input_text = text.strip()[:self.max_input_length]

            summary = self.model(input_text, max_length=180, min_length=60, do_sample=False)[0]["summary_text"]
            return summary.strip()

        except Exception as e:
            print(f"[Erreur résumé] : {e}")
            return None
