"""Système de palettes de couleurs intelligentes et adaptatives"""
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import random
import logging

logger = logging.getLogger(__name__)


class TimeOfDay(Enum):
    """Périodes de la journée"""
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"


class Emotion(Enum):
    """Émotions supportées"""
    JOY = "joy"
    MOTIVATION = "motivation"
    WISDOM = "wisdom"
    LOVE = "love"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class ColorScheme:
    """Schéma de couleurs complet"""
    background: str
    text: str
    accent: str
    name: Optional[str] = None
    
    def to_list(self) -> List[str]:
        """Convertit en liste [bg, text, accent]"""
        return [self.background, self.text, self.accent]
    
    def __repr__(self) -> str:
        return f"ColorScheme({self.name or 'unnamed'}: bg={self.background}, text={self.text}, accent={self.accent})"


class ColorPalette:
    """Gestionnaire intelligent de palettes de couleurs"""
    
    # Palettes modernes et professionnelles par émotion
    EMOTION_SCHEMES = {
        Emotion.JOY: [
            ColorScheme('#FFD93D', '#2C2C2C', '#FF6B6B', 'Sunshine'),
            ColorScheme('#F9A825', '#FFFFFF', '#EF5350', 'Golden Hour'),
            ColorScheme('#FFC107', '#1A1A1A', '#FF7043', 'Radiant'),
        ],
        
        Emotion.MOTIVATION: [
            ColorScheme('#E63946', '#FFFFFF', '#457B9D', 'Power'),
            ColorScheme('#D62828', '#F8F9FA', '#023E8A', 'Drive'),
            ColorScheme('#C9184A', '#FFFFFF', '#0077B6', 'Ambition'),
        ],
        
        Emotion.WISDOM: [
            ColorScheme('#2C3E50', '#ECF0F1', '#95A5A6', 'Sage'),
            ColorScheme('#34495E', '#FDFEFE', '#7F8C8D', 'Philosopher'),
            ColorScheme('#283747', '#EAECEE', '#85929E', 'Scholar'),
        ],
        
        Emotion.LOVE: [
            ColorScheme('#E91E63', '#FFFFFF', '#F06292', 'Passion'),
            ColorScheme('#AD1457', '#FAFAFA', '#EC407A', 'Romance'),
            ColorScheme('#C2185B', '#FFFFFF', '#F48FB1', 'Affection'),
        ],
        
        Emotion.SADNESS: [
            ColorScheme('#546E7A', '#ECEFF1', '#90A4AE', 'Melancholy'),
            ColorScheme('#455A64', '#F5F5F5', '#78909C', 'Contemplation'),
            ColorScheme('#37474F', '#FAFAFA', '#607D8B', 'Reflection'),
        ],
        
        Emotion.ANGER: [
            ColorScheme('#B71C1C', '#FFFFFF', '#E53935', 'Fury'),
            ColorScheme('#C62828', '#FAFAFA', '#EF5350', 'Rage'),
            ColorScheme('#D32F2F', '#F5F5F5', '#F44336', 'Intensity'),
        ],
        
        Emotion.FEAR: [
            ColorScheme('#263238', '#ECEFF1', '#546E7A', 'Shadow'),
            ColorScheme('#37474F', '#E0E0E0', '#607D8B', 'Unease'),
            ColorScheme('#455A64', '#CFD8DC', '#78909C', 'Anxiety'),
        ],
        
        Emotion.POSITIVE: [
            ColorScheme('#00BCD4', '#FFFFFF', '#0097A7', 'Optimism'),
            ColorScheme('#00ACC1', '#FAFAFA', '#00838F', 'Hope'),
            ColorScheme('#0097A7', '#F5F5F5', '#006064', 'Brightness'),
        ],
        
        Emotion.NEUTRAL: [
            ColorScheme('#607D8B', '#FFFFFF', '#455A64', 'Balance'),
            ColorScheme('#78909C', '#FAFAFA', '#546E7A', 'Equilibrium'),
            ColorScheme('#90A4AE', '#F5F5F5', '#37474F', 'Calm'),
        ],
        
        Emotion.NEGATIVE: [
            ColorScheme('#5D4037', '#EFEBE9', '#8D6E63', 'Somber'),
            ColorScheme('#4E342E', '#F5F5F5', '#795548', 'Grave'),
            ColorScheme('#3E2723', '#FAFAFA', '#6D4C41', 'Heavy'),
        ],
    }
    
    # Palettes par moment de la journée
    TIME_SCHEMES = {
        TimeOfDay.MORNING: [
            ColorScheme('#FFB74D', '#FFFFFF', '#FF9800', 'Sunrise'),
            ColorScheme('#FFA726', '#FAFAFA', '#FB8C00', 'Dawn'),
            ColorScheme('#FF9800', '#F5F5F5', '#F57C00', 'Morning Light'),
        ],
        
        TimeOfDay.AFTERNOON: [
            ColorScheme('#42A5F5', '#FFFFFF', '#1E88E5', 'Blue Sky'),
            ColorScheme('#2196F3', '#FAFAFA', '#1976D2', 'Clear Day'),
            ColorScheme('#1E88E5', '#F5F5F5', '#1565C0', 'Daylight'),
        ],
        
        TimeOfDay.EVENING: [
            ColorScheme('#7E57C2', '#FFFFFF', '#5E35B1', 'Dusk'),
            ColorScheme('#673AB7', '#FAFAFA', '#512DA8', 'Twilight'),
            ColorScheme('#5E35B1', '#F5F5F5', '#4527A0', 'Sunset'),
        ],
        
        TimeOfDay.NIGHT: [
            ColorScheme('#1A237E', '#E8EAF6', '#283593', 'Midnight'),
            ColorScheme('#0D47A1', '#E3F2FD', '#1565C0', 'Deep Night'),
            ColorScheme('#01579B', '#E1F5FE', '#0277BD', 'Starry'),
        ],
    }
    
    # Palettes dark mode optimisées
    DARK_SCHEMES = [
        ColorScheme('#0F172A', '#F1F5F9', '#06B6D4', 'Slate Dark'),
        ColorScheme('#1E293B', '#E2E8F0', '#8B5CF6', 'Navy Dark'),
        ColorScheme('#18181B', '#FAFAFA', '#A855F7', 'Zinc Dark'),
        ColorScheme('#0A0A0A', '#F5F5F5', '#EC4899', 'Black Dark'),
    ]
    
    def __init__(self):
        """Initialise le gestionnaire de palettes"""
        self._cache = {}
        logger.info(f"ColorPalette initialisé - {len(self.EMOTION_SCHEMES)} émotions, {len(self.TIME_SCHEMES)} périodes")
    
    def get_scheme_for_emotion(
        self,
        emotion: str,
        variant: int = 0
    ) -> ColorScheme:
        """Récupère un schéma de couleurs pour une émotion
        
        Args:
            emotion: Nom de l'émotion
            variant: Index de variante (0, 1, 2...)
            
        Returns:
            ColorScheme correspondant
        """
        # Normaliser l'émotion
        try:
            emotion_enum = Emotion(emotion.lower())
        except ValueError:
            logger.warning(f"Émotion inconnue: {emotion}, utilisation de NEUTRAL")
            emotion_enum = Emotion.NEUTRAL
        
        schemes = self.EMOTION_SCHEMES[emotion_enum]
        variant_index = variant % len(schemes)
        return schemes[variant_index]
    
    def get_random_scheme_for_emotion(self, emotion: str) -> ColorScheme:
        """Récupère un schéma aléatoire pour une émotion
        
        Args:
            emotion: Nom de l'émotion
            
        Returns:
            ColorScheme aléatoire
        """
        try:
            emotion_enum = Emotion(emotion.lower())
        except ValueError:
            emotion_enum = Emotion.NEUTRAL
        
        schemes = self.EMOTION_SCHEMES[emotion_enum]
        return random.choice(schemes)
    
    def get_scheme_for_time(self, period: str) -> ColorScheme:
        """Récupère un schéma pour un moment de la journée
        
        Args:
            period: 'morning', 'afternoon', 'evening', 'night'
            
        Returns:
            ColorScheme correspondant
        """
        try:
            time_enum = TimeOfDay(period.lower())
        except ValueError:
            logger.warning(f"Période inconnue: {period}, utilisation de AFTERNOON")
            time_enum = TimeOfDay.AFTERNOON
        
        schemes = self.TIME_SCHEMES[time_enum]
        return random.choice(schemes)
    
    def get_dark_scheme(self) -> ColorScheme:
        """Récupère un schéma dark mode
        
        Returns:
            ColorScheme dark
        """
        return random.choice(self.DARK_SCHEMES)
    
    def get_intelligent_palette(
        self,
        emotion: str,
        time_period: Optional[str] = None,
        prefer_dark: bool = False
    ) -> List[str]:
        """Sélectionne intelligemment une palette optimale
        
        Args:
            emotion: Émotion détectée
            time_period: Moment de la journée (optionnel)
            prefer_dark: Si True, préfère les fonds sombres
            
        Returns:
            Liste [background, text, accent]
        """
        cache_key = f"{emotion}_{time_period}_{prefer_dark}"
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Dark mode prioritaire
        if prefer_dark:
            scheme = self.get_dark_scheme()
        # Nuit = dark automatique
        elif time_period == 'night':
            scheme = self.get_scheme_for_time('night')
        # Sinon, émotion
        else:
            scheme = self.get_random_scheme_for_emotion(emotion)
        
        palette = scheme.to_list()
        self._cache[cache_key] = palette
        
        logger.info(f"Palette sélectionnée: {scheme.name} pour {emotion}")
        return palette
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convertit hex en RGB
        
        Args:
            hex_color: Couleur #RRGGBB
            
        Returns:
            Tuple (R, G, B)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convertit RGB en hex
        
        Args:
            rgb: Tuple (R, G, B)
            
        Returns:
            Couleur #RRGGBB
        """
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def calculate_brightness(self, hex_color: str) -> float:
        """Calcule la luminosité perçue d'une couleur
        
        Args:
            hex_color: Couleur hex
            
        Returns:
            Luminosité (0-255)
        """
        rgb = self.hex_to_rgb(hex_color)
        # Formule de luminosité perçue
        return (rgb[0] * 0.299 + rgb[1] * 0.587 + rgb[2] * 0.114)
    
    def ensure_contrast(
        self,
        bg_color: str,
        text_color: str,
        min_brightness_diff: float = 125
    ) -> str:
        """Vérifie et ajuste le contraste
        
        Args:
            bg_color: Couleur de fond
            text_color: Couleur de texte
            min_brightness_diff: Différence minimum de luminosité
            
        Returns:
            Couleur de texte ajustée si nécessaire
        """
        bg_brightness = self.calculate_brightness(bg_color)
        
        # Fond clair → texte sombre
        if bg_brightness > 128:
            return '#1A1A1A'
        # Fond sombre → texte clair
        else:
            return '#FAFAFA'
    
    def get_available_emotions(self) -> List[str]:
        """Liste des émotions disponibles
        
        Returns:
            Liste de noms d'émotions
        """
        return [e.value for e in Emotion]
    
    def get_all_variants(self, emotion: str) -> List[ColorScheme]:
        """Récupère toutes les variantes d'une émotion
        
        Args:
            emotion: Nom de l'émotion
            
        Returns:
            Liste de ColorSchemes
        """
        try:
            emotion_enum = Emotion(emotion.lower())
            return self.EMOTION_SCHEMES[emotion_enum]
        except ValueError:
            return self.EMOTION_SCHEMES[Emotion.NEUTRAL]
    
    def create_custom_scheme(
        self,
        background: str,
        text: str,
        accent: str,
        name: Optional[str] = None
    ) -> ColorScheme:
        """Crée un schéma personnalisé
        
        Args:
            background: Couleur de fond
            text: Couleur de texte
            accent: Couleur d'accent
            name: Nom du schéma (optionnel)
            
        Returns:
            ColorScheme personnalisé
        """
        # Vérifier le contraste
        adjusted_text = self.ensure_contrast(background, text)
        
        scheme = ColorScheme(
            background=background,
            text=adjusted_text,
            accent=accent,
            name=name or 'Custom'
        )
        
        logger.info(f"Schéma personnalisé créé: {scheme}")
        return scheme
    
    def get_complementary_color(self, hex_color: str) -> str:
        """Calcule la couleur complémentaire
        
        Args:
            hex_color: Couleur de base
            
        Returns:
            Couleur complémentaire en hex
        """
        rgb = self.hex_to_rgb(hex_color)
        # Complémentaire = inverse RGB
        comp_rgb = (255 - rgb[0], 255 - rgb[1], 255 - rgb[2])
        return self.rgb_to_hex(comp_rgb)
    
    def get_scheme_preview(self, emotion: str) -> Dict[str, ColorScheme]:
        """Aperçu de toutes les variantes d'une émotion
        
        Args:
            emotion: Nom de l'émotion
            
        Returns:
            Dict {nom_variante: ColorScheme}
        """
        schemes = self.get_all_variants(emotion)
        return {
            f"{scheme.name}": scheme
            for scheme in schemes
        }


# Point d'entrée pour tests
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🎨 Test ColorPalette Professionnel\n")
    
    palette = ColorPalette()
    
    # Test 1: Émotions
    print("1️⃣ Schémas par émotion:")
    for emotion in ['joy', 'motivation', 'wisdom']:
        scheme = palette.get_scheme_for_emotion(emotion)
        print(f"   {emotion.capitalize()}: {scheme}")
    print()
    
    # Test 2: Moments
    print("2️⃣ Schémas par moment:")
    for period in ['morning', 'afternoon', 'evening', 'night']:
        scheme = palette.get_scheme_for_time(period)
        print(f"   {period.capitalize()}: {scheme}")
    print()
    
    # Test 3: Palette intelligente
    print("3️⃣ Palette intelligente:")
    smart_palette = palette.get_intelligent_palette('motivation', 'morning', False)
    print(f"   Résultat: {smart_palette}")
    print()
    
    # Test 4: Contraste
    print("4️⃣ Ajustement contraste:")
    adjusted = palette.ensure_contrast('#FFD700', '#FFFFFF')
    print(f"   Fond: #FFD700, Texte ajusté: {adjusted}")
    print()
    
    print("✅ Tests terminés")