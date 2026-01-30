"""QuoteFetcher avec CACHE intelligent contre rate limiting"""
import requests
from typing import Optional, Dict, List
import sys
from pathlib import Path
import time
import random
import json

sys.path.append(str(Path(__file__).parent.parent))
try:
    from app.data.local_quotes import get_random_quote as get_local_quote
    LOCAL_OK = True
except:
    LOCAL_OK = False

class QuoteFetcher:
    """Récupère des citations avec cache anti-rate-limit"""
    
    ZENQUOTES_URL = "https://zenquotes.io/api"
    CACHE_FILE = "data/quotes_cache.json"
    CACHE_DURATION = 3600  # 1 heure
    MIN_REQUEST_DELAY = 2  # 2 secondes entre requêtes
    
    THEME_KEYWORDS = {
        'motivation': ['motivate', 'inspire', 'success', 'achieve', 'goal', 'dream', 'action'],
        'sagesse': ['wisdom', 'knowledge', 'learn', 'understand', 'philosophy', 'truth'],
        'amour': ['love', 'heart', 'compassion', 'kindness', 'care', 'affection'],
        'courage': ['courage', 'brave', 'fear', 'strength', 'perseverance', 'resilience'],
        'succès': ['success', 'achievement', 'win', 'victory', 'accomplish', 'excel'],
        'bonheur': ['happiness', 'joy', 'smile', 'grateful', 'positive', 'delight'],
        'inspiration': ['inspire', 'creative', 'imagine', 'dream', 'vision', 'passion'],
        'auto': None
    }
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.cache = self._load_cache()
        self.last_request_time = 0
    
    def _load_cache(self) -> Dict:
        """Charge le cache depuis le fichier"""
        cache_path = Path(self.CACHE_FILE)
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {'quotes': [], 'timestamp': 0}
    
    def _save_cache(self):
        """Sauvegarde le cache"""
        cache_path = Path(self.CACHE_FILE)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde cache: {e}")
    
    def _wait_for_rate_limit(self):
        """Attend avant la prochaine requête"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.MIN_REQUEST_DELAY:
            wait_time = self.MIN_REQUEST_DELAY - elapsed
            print(f"⏳ Attente {wait_time:.1f}s (rate limit)...")
            time.sleep(wait_time)
        self.last_request_time = time.time()
    
    def _get_from_cache(self, theme: str) -> Optional[Dict]:
        """Récupère une citation du cache"""
        if not self.cache.get('quotes'):
            return None
        
        # Filtrer par thème si nécessaire
        if theme != 'auto' and theme in self.THEME_KEYWORDS:
            matching = [q for q in self.cache['quotes'] if self._matches_theme(q, theme)]
            if matching:
                quote = random.choice(matching)
                print(f"💾 Citation récupérée du cache (thème: {theme})")
                return quote
        
        # Sinon retourner une citation aléatoire du cache
        if self.cache['quotes']:
            quote = random.choice(self.cache['quotes'])
            print(f"💾 Citation récupérée du cache (aléatoire)")
            return quote
        
        return None
    
    def fetch_random_quote(self, theme: str = 'auto') -> Optional[Dict]:
        """Récupère une citation avec gestion intelligente du cache"""
        
        print(f"🎯 Récupération citation, thème: {theme}")
        
        # 1. Essayer le cache d'abord (si moins de 5 minutes)
        cache_age = time.time() - self.cache.get('timestamp', 0)
        if cache_age < 300:  # 5 minutes
            cached = self._get_from_cache(theme)
            if cached:
                return cached
        
        # 2. Essayer l'API avec rate limiting
        self._wait_for_rate_limit()
        
        for attempt in range(3):  # Seulement 3 tentatives au lieu de 5
            quote = self._fetch_single_quote()
            
            if quote:
                # Ajouter au cache
                if 'quotes' not in self.cache:
                    self.cache['quotes'] = []
                
                # Garder max 50 citations dans le cache
                if len(self.cache['quotes']) >= 50:
                    self.cache['quotes'].pop(0)
                
                self.cache['quotes'].append(quote)
                self.cache['timestamp'] = time.time()
                self._save_cache()
                
                # Vérifier si ça match le thème
                if theme != 'auto' and self._matches_theme(quote, theme):
                    print(f"✅ Citation trouvée pour '{theme}' (tentative {attempt+1})")
                    return quote
                elif theme == 'auto':
                    return quote
            
            # Attendre un peu entre les tentatives
            if attempt < 2:
                time.sleep(1)
        
        # 3. Fallback vers cache si disponible
        cached = self._get_from_cache(theme)
        if cached:
            print(f"💾 Utilisation du cache après échec API")
            return cached
        
        # 4. Fallback vers citations locales
        print(f"📚 Utilisation citations locales (thème: {theme})")
        if LOCAL_OK:
            return get_local_quote(theme)
        
        return self._get_fallback_quote()
    
    def _fetch_single_quote(self) -> Optional[Dict]:
        """Récupère UNE citation depuis ZenQuotes"""
        try:
            response = requests.get(
                f"{self.ZENQUOTES_URL}/random",
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                quote = data[0]
                return {
                    'content': quote.get('q', ''),
                    'author': quote.get('a', 'Unknown'),
                    'tags': [],
                    'length': len(quote.get('q', '')),
                    'id': quote.get('h', f"zen_{hash(quote.get('q', ''))}"),
                    'source': 'zenquotes'
                }
            
            return None
            
        except requests.exceptions.HTTPError as e:
            if '429' in str(e):
                print(f"⚠️ Rate limit atteint, utilisation du cache...")
            else:
                print(f"⚠️ Erreur HTTP: {e}")
            return None
        except Exception as e:
            print(f"⚠️ Erreur ZenQuotes: {e}")
            return None
    
    def _matches_theme(self, quote: Dict, theme: str) -> bool:
        """Vérifie si une citation correspond au thème"""
        if theme == 'auto':
            return True
        
        keywords = self.THEME_KEYWORDS.get(theme, [])
        if not keywords:
            return True
        
        content_lower = quote['content'].lower()
        
        for keyword in keywords:
            if keyword in content_lower:
                return True
        
        return False
    
    def _get_fallback_quote(self) -> Dict:
        """Citation de secours"""
        return {
            'content': "Le succès est la somme de petits efforts répétés jour après jour.",
            'author': 'Robert Collier',
            'tags': ['motivation'],
            'length': 68,
            'id': 'fallback',
            'source': 'fallback'
        }
    
    def get_available_themes(self) -> List[str]:
        return list(self.THEME_KEYWORDS.keys())
    
    def get_cache_stats(self) -> Dict:
        """Statistiques du cache"""
        return {
            'size': len(self.cache.get('quotes', [])),
            'age_seconds': time.time() - self.cache.get('timestamp', 0)
        }
