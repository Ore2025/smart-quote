"""Utilitaires - Cache intelligent pour citations et images"""
import streamlit as st
import hashlib
from PIL import Image


def get_quote_hash(quote_content):
    """Génère un hash unique pour une citation
    
    Args:
        quote_content: Contenu de la citation
        
    Returns:
        Hash MD5 de la citation
    """
    return hashlib.md5(quote_content.encode()).hexdigest()


def fetch_unique_quote(fetcher, theme, max_attempts=10):
    """Récupère une citation unique (non vue récemment)
    
    Args:
        fetcher: Instance de QuoteFetcher
        theme: Thème souhaité
        max_attempts: Nombre maximum de tentatives
        
    Returns:
        Dict avec les données de la citation ou None
    """
    for attempt in range(max_attempts):
        try:
            quote_data = fetcher.fetch_random_quote(theme)
            
            if not quote_data:
                continue
            
            # Vérifier si déjà vue
            quote_hash = get_quote_hash(quote_data.get('content', ''))
            
            if quote_hash not in st.session_state.quote_cache:
                # Nouvelle citation, l'ajouter au cache
                st.session_state.quote_cache.add(quote_hash)
                
                # Limiter la taille du cache (garder les 30 dernières)
                if len(st.session_state.quote_cache) > 30:
                    # Convertir en liste, supprimer le premier, reconvertir
                    cache_list = list(st.session_state.quote_cache)
                    cache_list.pop(0)
                    st.session_state.quote_cache = set(cache_list)
                
                return quote_data
        
        except Exception as e:
            print(f"⚠️ Tentative {attempt + 1} échouée: {str(e)}")
            continue
    
    # Si on n'a pas trouvé de citation unique après max_attempts
    # Vider le cache et retourner n'importe quelle citation
    st.session_state.quote_cache.clear()
    
    try:
        return fetcher.fetch_random_quote(theme)
    except Exception as e:
        print(f"❌ Impossible de récupérer une citation: {str(e)}")
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def generate_image_cached(quote_text, author, palette_tuple, style, font_family):
    """Génère une image avec cache (1 heure)
    
    Args:
        quote_text: Texte de la citation
        author: Auteur
        palette_tuple: Tuple (bg, text, accent) - doit être hashable
        style: Style visuel
        font_family: Police
        
    Returns:
        Image PIL
        
    Note:
        Cette fonction est cached pour éviter de régénérer
        les mêmes images plusieurs fois
    """
    from app.design.image_generator import ImageGenerator
    
    generator = ImageGenerator()
    palette = list(palette_tuple)  # Convertir tuple en list pour le générateur
    
    return generator.create_image(
        quote_text,
        author,
        palette,
        style,
        font_family
    )


def clear_image_cache():
    """Vide le cache des images"""
    generate_image_cached.clear()
    st.toast("🗑️ Cache des images vidé", icon="🗑️")


def clear_quote_cache():
    """Vide le cache des citations"""
    if 'quote_cache' in st.session_state:
        st.session_state.quote_cache.clear()
        st.toast("🗑️ Cache des citations vidé", icon="🗑️")


def get_cache_stats():
    """Retourne les statistiques du cache
    
    Returns:
        Dict avec les infos de cache
    """
    return {
        'quote_cache_size': len(st.session_state.get('quote_cache', set())),
        'image_cache_enabled': True,
        'image_cache_ttl': 3600  # 1 heure
    }


@st.cache_data(ttl=1800, show_spinner=False)
def translate_cached(text, source_lang, target_lang):
    """Traduit un texte avec cache (30 minutes)
    
    Args:
        text: Texte à traduire
        source_lang: Langue source
        target_lang: Langue cible
        
    Returns:
        Texte traduit
    """
    from app.core.translator import Translator
    
    translator = Translator()
    return translator.translate(text, source_lang, target_lang)


@st.cache_data(ttl=900, show_spinner=False)
def analyze_sentiment_cached(text):
    """Analyse le sentiment avec cache (15 minutes)
    
    Args:
        text: Texte à analyser
        
    Returns:
        Dict avec les résultats d'analyse
    """
    from app.core.sentiment_analyzer import SentimentAnalyzer
    
    analyzer = SentimentAnalyzer()
    return analyzer.analyze(text)