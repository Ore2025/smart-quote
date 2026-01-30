"""Utilitaires - Gestion du session state et initialisation"""
import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.quote_fetcher import QuoteFetcher
from app.core.translator import Translator
from app.core.sentiment_analyzer import SentimentAnalyzer
from app.core.context_detector import ContextDetector
from app.design.image_generator import ImageGenerator
from app.design.color_palette import ColorPalette
from app.intelligence.history_manager import HistoryManager


@st.cache_resource
def init_modules():
    """Initialise tous les modules nécessaires avec cache
    
    Returns:
        Dict contenant tous les modules initialisés
    """
    try:
        modules = {
            'fetcher': QuoteFetcher(),
            'translator': Translator(),
            'analyzer': SentimentAnalyzer(),
            'context': ContextDetector(),
            'generator': ImageGenerator(),
            'palette': ColorPalette(),
            'history': HistoryManager()
        }
        return modules
    except Exception as e:
        st.error(f"❌ Erreur initialisation modules: {str(e)}")
        st.stop()


def init_session_state():
    """Initialise le session state avec toutes les variables nécessaires"""
    
    # Cache des citations déjà vues
    if 'quote_cache' not in st.session_state:
        st.session_state.quote_cache = set()
    
    # Citation actuelle
    if 'current_quote' not in st.session_state:
        st.session_state.current_quote = None
    
    # Image actuelle
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    
    # Émotion détectée
    if 'current_emotion' not in st.session_state:
        st.session_state.current_emotion = None
    
    # Thème utilisé
    if 'current_theme' not in st.session_state:
        st.session_state.current_theme = None
    
    # Affichage bannière bienvenue
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True
    
    # Compteur session
    if 'session_count' not in st.session_state:
        st.session_state.session_count = 0
    
    # Favoris (nouvelle fonctionnalité)
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []


def reset_session_state():
    """Réinitialise le session state (utile pour debugging)"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()


def add_to_favorites(quote_data, image):
    """Ajoute une citation aux favoris
    
    Args:
        quote_data: Données de la citation
        image: Image PIL
    """
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    
    favorite = {
        'quote': quote_data,
        'image': image,
        'timestamp': quote_data.get('timestamp'),
        'emotion': st.session_state.get('current_emotion', 'neutral'),
        'theme': st.session_state.get('current_theme', 'unknown')
    }
    
    st.session_state.favorites.append(favorite)
    st.toast("❤️ Ajouté aux favoris !", icon="❤️")


def get_session_stats():
    """Retourne les statistiques de la session actuelle
    
    Returns:
        Dict avec les stats
    """
    return {
        'quotes_generated': st.session_state.get('session_count', 0),
        'cache_size': len(st.session_state.get('quote_cache', set())),
        'favorites_count': len(st.session_state.get('favorites', [])),
        'has_current_quote': st.session_state.get('current_quote') is not None
    }