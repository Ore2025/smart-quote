"""Détecteur de contexte SUPER intelligent"""
from datetime import datetime
from typing import Dict, Optional
import os

try:
    from pyowm import OWM
    OWM_AVAILABLE = True
except:
    OWM_AVAILABLE = False

class ContextDetector:
    """Détecte TOUT le contexte pour suggestions intelligentes"""
    
    # Thèmes par heure
    TIME_THEMES = {
        'morning': 'motivation',      # 5h-12h : Motivant
        'afternoon': 'inspiration',    # 12h-17h : Inspirant
        'evening': 'sagesse',          # 17h-21h : Réflexion
        'night': 'bonheur'            # 21h-5h : Paix
    }
    
    # Thèmes par jour
    WEEKDAY_THEMES = {
        'Monday': 'motivation',        # Lundi : Besoin de motivation !
        'Tuesday': 'courage',          # Mardi : Persévérance
        'Wednesday': 'inspiration',    # Mercredi : À mi-chemin
        'Thursday': 'succès',          # Jeudi : Presque là
        'Friday': 'bonheur',           # Vendredi : Célébration
        'Saturday': 'amour',           # Samedi : Détente, amour
        'Sunday': 'sagesse'            # Dimanche : Réflexion
    }
    
    # Thèmes par météo
    WEATHER_THEMES = {
        'clear': 'bonheur',            # Soleil : Joie
        'clouds': 'sagesse',           # Nuageux : Réflexion
        'rain': 'courage',             # Pluie : Courage
        'drizzle': 'inspiration',      # Bruine : Inspiration
        'thunderstorm': 'courage',     # Orage : Force
        'snow': 'amour',               # Neige : Douceur
        'mist': 'sagesse'              # Brume : Mystère
    }
    
    def __init__(self):
        self.owm_api_key = os.getenv('OPENWEATHER_API_KEY', '')
        self.weather_enabled = OWM_AVAILABLE and bool(self.owm_api_key)
        
        if self.weather_enabled:
            try:
                self.owm = OWM(self.owm_api_key)
                self.weather_mgr = self.owm.weather_manager()
            except:
                self.weather_enabled = False
    
    def get_time_context(self) -> Dict:
        """Contexte temporel complet"""
        now = datetime.now()
        hour = now.hour
        
        # Période
        if 5 <= hour < 12:
            period = "morning"
            greeting = "Bonjour"
        elif 12 <= hour < 17:
            period = "afternoon"
            greeting = "Bon après-midi"
        elif 17 <= hour < 21:
            period = "evening"
            greeting = "Bonsoir"
        else:
            period = "night"
            greeting = "Bonne soirée"
        
        # Thème suggéré selon l'heure
        time_theme = self.TIME_THEMES.get(period, 'inspiration')
        
        # Jour de la semaine
        day_of_week = now.strftime('%A')
        weekday_theme = self.WEEKDAY_THEMES.get(day_of_week, 'inspiration')
        
        # Weekend ?
        is_weekend = now.weekday() >= 5
        
        return {
            'hour': hour,
            'period': period,
            'greeting': greeting,
            'time_theme': time_theme,
            'day_of_week': day_of_week,
            'weekday_theme': weekday_theme,
            'is_weekend': is_weekend,
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M')
        }
    
    def get_weather_context(self, location: str = 'Cotonou,BJ') -> Optional[Dict]:
        """Contexte météo"""
        if not self.weather_enabled:
            return None
        
        try:
            observation = self.weather_mgr.weather_at_place(location)
            weather = observation.weather
            
            status = weather.status.lower()
            temp = weather.temperature('celsius')['temp']
            
            # Thème selon météo
            weather_theme = None
            for key, theme in self.WEATHER_THEMES.items():
                if key in status:
                    weather_theme = theme
                    break
            
            if not weather_theme:
                weather_theme = 'inspiration'
            
            return {
                'status': status,
                'description': weather.detailed_status,
                'temperature': temp,
                'weather_theme': weather_theme,
                'is_sunny': 'clear' in status,
                'is_rainy': 'rain' in status,
                'emoji': self._get_weather_emoji(status)
            }
            
        except Exception as e:
            print(f"⚠️ Météo indisponible: {e}")
            return None
    
    def _get_weather_emoji(self, status: str) -> str:
        """Emoji météo"""
        if 'clear' in status or 'sun' in status:
            return '☀️'
        elif 'rain' in status:
            return '🌧️'
        elif 'cloud' in status:
            return '☁️'
        elif 'storm' in status:
            return '⛈️'
        elif 'snow' in status:
            return '❄️'
        else:
            return '🌤️'
    
    def suggest_theme_intelligent(
        self,
        use_weather: bool = False,
        location: Optional[str] = None,
        user_preference: Optional[str] = None
    ) -> str:
        """Suggestion SUPER intelligente de thème
        
        Priorité:
        1. Préférence utilisateur (si spécifiée et != Auto)
        2. Météo (si activée)
        3. Jour de la semaine
        4. Heure de la journée
        """
        
        print("🧠 Calcul du thème intelligent...")
        
        # 1. Préférence utilisateur
        if user_preference and user_preference.lower() not in ['auto', 'auto (intelligent)']:
            theme = user_preference.lower()
            print(f"  ✓ Préférence utilisateur: {theme}")
            return theme
        
        # 2. Contexte temporel
        time_ctx = self.get_time_context()
        
        # 3. Météo (si demandée)
        if use_weather and location:
            weather_ctx = self.get_weather_context(location)
            if weather_ctx:
                theme = weather_ctx['weather_theme']
                print(f"  ✓ Thème selon météo ({weather_ctx['status']}): {theme}")
                return theme
        
        # 4. Weekend vs Semaine
        if time_ctx['is_weekend']:
            # Weekend : plus relax
            theme = 'bonheur' if time_ctx['period'] in ['afternoon', 'evening'] else 'amour'
            print(f"  ✓ Weekend détecté: {theme}")
            return theme
        
        # 5. Jour de la semaine (prioritaire en semaine)
        theme = time_ctx['weekday_theme']
        print(f"  ✓ Thème selon {time_ctx['day_of_week']}: {theme}")
        return theme
    
    def get_full_context_message(self, use_weather: bool = False, location: Optional[str] = None) -> str:
        """Message contextuel complet"""
        time_ctx = self.get_time_context()
        weather_ctx = self.get_weather_context(location) if use_weather and location else None
        
        msg = f"{time_ctx['greeting']} ! "
        
        if weather_ctx:
            msg += f"{weather_ctx['emoji']} {weather_ctx['temperature']:.0f}°C • "
        
        msg += f"{time_ctx['day_of_week']}"
        
        # Ajout contextuel
        if time_ctx['day_of_week'] == 'Monday':
            msg += " - Bonne semaine ! 💪"
        elif time_ctx['day_of_week'] == 'Friday':
            msg += " - Bon weekend ! 🎉"
        elif time_ctx['is_weekend']:
            msg += " - Profitez bien ! ☀️"
        
        return msg
