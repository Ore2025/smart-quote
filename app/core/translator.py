"""Traducteur avec Google Translate (gratuit, pas de clé API)"""
from deep_translator import GoogleTranslator
from typing import Optional

class Translator:
    """Traducteur EN -> FR automatique"""
    
    def __init__(self):
        self.translator = GoogleTranslator(source='en', target='fr')
    
    def translate(self, text: str, source_lang: str = 'en', target_lang: str = 'fr') -> str:
        """Traduit un texte EN -> FR
        
        Args:
            text: Texte à traduire
            source_lang: Langue source
            target_lang: Langue cible
            
        Returns:
            Texte traduit (ou original si erreur)
        """
        # Si déjà français, retourner tel quel
        if self._is_french(text):
            return text
        
        try:
            # Configurer langues
            self.translator.source = source_lang.lower()
            self.translator.target = target_lang.lower()
            
            # Traduire
            result = self.translator.translate(text)
            return result if result else text
            
        except Exception as e:
            print(f"⚠️ Erreur traduction: {e}")
            return text  # Retourner original si échec
    
    def _is_french(self, text: str) -> bool:
        """Détection simple si texte déjà français"""
        french_words = ['le', 'la', 'les', 'de', 'des', 'un', 'une', 'et', 'est', 'dans', 'que', 'pour', 'pas']
        text_lower = text.lower()
        
        french_count = sum(1 for word in french_words if f' {word} ' in f' {text_lower} ')
        return french_count >= 2
    
    def detect_language(self, text: str) -> str:
        """Détecte la langue (simple)"""
        if self._is_french(text):
            return 'FR'
        return 'EN'
