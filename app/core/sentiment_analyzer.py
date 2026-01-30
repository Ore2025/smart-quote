"""Module d'analyse de sentiment avec TextBlob et VADER"""
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List

class SentimentAnalyzer:
    """Analyse le sentiment émotionnel d'un texte"""
    
    def __init__(self):
        """Initialise l'analyseur avec VADER"""
        self.vader = SentimentIntensityAnalyzer()
        
        # Mots-clés par émotion pour affiner l'analyse
        self.emotion_keywords = {
            'joy': ['heureux', 'joie', 'bonheur', 'rire', 'sourire', 'célébrer', 'happy', 'joy', 'celebrate'],
            'motivation': ['réussir', 'succès', 'gagner', 'victoire', 'courage', 'force', 'success', 'win', 'courage'],
            'wisdom': ['sagesse', 'apprendre', 'connaissance', 'comprendre', 'wisdom', 'learn', 'knowledge'],
            'love': ['amour', 'aimer', 'cœur', 'tendresse', 'affection', 'love', 'heart', 'care'],
            'sadness': ['triste', 'tristesse', 'pleurer', 'larmes', 'malheur', 'sad', 'cry', 'tears'],
            'anger': ['colère', 'rage', 'furieux', 'énerver', 'anger', 'rage', 'fury'],
            'fear': ['peur', 'crainte', 'anxiété', 'inquiétude', 'fear', 'anxiety', 'worry']
        }
    
    def analyze(self, text: str, language: str = 'en') -> Dict:
        """Analyse le sentiment d'un texte
        
        Args:
            text: Texte à analyser
            language: Langue du texte ('en' ou 'fr')
            
        Returns:
            Dict avec polarity, subjectivity, emotion, scores
        """
        # Analyse TextBlob (simple)
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Analyse VADER (plus robuste)
        vader_scores = self.vader.polarity_scores(text)
        
        # Combiner les deux analyses
        combined_polarity = (polarity + vader_scores['compound']) / 2
        
        # Déterminer l'émotion principale
        emotion = self._categorize_emotion(combined_polarity, text)
        
        # Intensité émotionnelle
        intensity = abs(combined_polarity)
        
        return {
            'polarity': combined_polarity,
            'subjectivity': subjectivity,
            'emotion': emotion,
            'intensity': intensity,
            'vader_scores': vader_scores,
            'emotion_category': self._get_emotion_label(combined_polarity),
            'keywords': self._extract_emotion_keywords(text, emotion)
        }
    
    def _categorize_emotion(self, polarity: float, text: str) -> str:
        """Catégorise l'émotion basée sur la polarité et les mots-clés
        
        Args:
            polarity: Score de polarité (-1 à 1)
            text: Texte analysé
            
        Returns:
            Émotion dominante
        """
        text_lower = text.lower()
        
        # Vérifier les mots-clés spécifiques
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return emotion
        
        # Fallback sur la polarité
        if polarity > 0.5:
            return 'joy'
        elif polarity > 0.1:
            return 'motivation'
        elif polarity > -0.1:
            return 'wisdom'
        elif polarity > -0.5:
            return 'sadness'
        else:
            return 'anger'
    
    def _get_emotion_label(self, polarity: float) -> str:
        """Retourne un label simple d'émotion
        
        Args:
            polarity: Score de polarité
            
        Returns:
            'positive', 'neutral', ou 'negative'
        """
        if polarity > 0.3:
            return 'positive'
        elif polarity < -0.3:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_emotion_keywords(self, text: str, emotion: str) -> List[str]:
        """Extrait les mots-clés émotionnels du texte
        
        Args:
            text: Texte à analyser
            emotion: Émotion détectée
            
        Returns:
            Liste de mots-clés trouvés
        """
        text_lower = text.lower()
        keywords = self.emotion_keywords.get(emotion, [])
        
        found_keywords = [kw for kw in keywords if kw in text_lower]
        return found_keywords[:3]  # Maximum 3 mots-clés
    
    def analyze_multiple(self, texts: List[str]) -> List[Dict]:
        """Analyse plusieurs textes à la fois
        
        Args:
            texts: Liste de textes à analyser
            
        Returns:
            Liste de résultats d'analyse
        """
        return [self.analyze(text) for text in texts]
    
    def get_dominant_emotion(self, text: str) -> str:
        """Retourne uniquement l'émotion dominante
        
        Args:
            text: Texte à analyser
            
        Returns:
            Nom de l'émotion
        """
        analysis = self.analyze(text)
        return analysis['emotion']


# Test du module
if __name__ == "__main__":
    print("🧪 Test du SentimentAnalyzer\n")
    
    analyzer = SentimentAnalyzer()
    
    # Tests avec différentes citations
    test_quotes = [
        "Le bonheur n'est pas quelque chose que vous remettez à plus tard, c'est quelque chose que vous créez maintenant.",
        "Le succès n'est pas final, l'échec n'est pas fatal : c'est le courage de continuer qui compte.",
        "La tristesse fait partie de la vie, mais elle ne doit pas la dominer.",
        "Dans les moments les plus sombres, nous devons nous concentrer pour voir la lumière."
    ]
    
    for i, quote in enumerate(test_quotes, 1):
        print(f"{i}️⃣ Citation: \"{quote[:60]}...\"")
        result = analyzer.analyze(quote)
        print(f"   Émotion: {result['emotion']}")
        print(f"   Catégorie: {result['emotion_category']}")
        print(f"   Polarité: {result['polarity']:.2f}")
        print(f"   Intensité: {result['intensity']:.2f}")
        print(f"   Mots-clés: {', '.join(result['keywords']) if result['keywords'] else 'Aucun'}\n")