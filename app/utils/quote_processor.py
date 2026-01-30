"""Utilitaires - Traitement et génération des citations"""
import streamlit as st
from app.utils.cache_utils import (
    fetch_unique_quote, 
    generate_image_cached,
    translate_cached,
    analyze_sentiment_cached
)


def process_quote_generation(modules, theme, language, style, font, colors, dark_mode, use_weather=False, location=None):
    """Processus complet de génération
    
    Args:
        modules: Dict des modules
        theme: Thème sélectionné
        language: Langue
        style: Style visuel
        font: Police
        colors: Couleurs ou None
        dark_mode: Mode sombre
        use_weather: Utiliser météo
        location: Localisation pour météo
        
    Returns:
        bool: True si succès, False sinon
    """
    
    with st.spinner("⏳ Génération..."):
        try:
            quote_data = fetch_unique_quote(modules['fetcher'], theme)
            
            if not quote_data:
                st.error("❌ Impossible de récupérer une citation")
                return False
            
            original_content = quote_data.get('content', '')
            
            if language == "Français" and original_content:
                try:
                    translated = translate_cached(original_content, 'en', 'fr')
                    
                    if translated and len(translated) > 10:
                        quote_data['content'] = translated
                        quote_data['original'] = original_content
                except:
                    pass
            
            if not quote_data.get('author') or quote_data['author'].lower() == 'unknown':
                quote_data['author'] = 'Anonyme' if language == "Français" else 'Anonymous'
            
            try:
                sentiment = analyze_sentiment_cached(quote_data.get('content', ''))
                emotion = sentiment.get('emotion', 'neutral')
            except:
                emotion = 'neutral'
            
            if colors:
                palette = colors
            else:
                try:
                    context_data = modules['context'].get_time_context()
                    
                    if use_weather and location:
                        weather_ctx = modules['context'].get_weather_context(location)
                        if weather_ctx:
                            emotion = weather_ctx['weather_theme']
                    
                    palette = modules['palette'].get_intelligent_palette(
                        emotion,
                        time_period=context_data.get('period', 'afternoon'),
                        prefer_dark=dark_mode
                    )
                except:
                    palette = ['#0E1117', '#FAFAFA', '#FF6B6B']
            
            try:
                palette_tuple = tuple(palette)
                
                img = generate_image_cached(
                    quote_data.get('content', ''),
                    quote_data.get('author', 'Unknown'),
                    palette_tuple,
                    style,
                    font
                )
            except Exception as e:
                st.error(f"❌ Erreur génération image: {str(e)}")
                return False
            
            try:
                quote_data['theme'] = theme
                quote_data['emotion'] = emotion
                modules['history'].save_quote(quote_data)
            except:
                pass
            
            st.session_state.current_quote = quote_data
            st.session_state.current_image = img
            st.session_state.current_emotion = emotion
            st.session_state.current_theme = theme
            
            return True
        
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
            return False


def regenerate_with_new_style(modules, style, font, colors=None):
    """Régénère l'image actuelle avec un nouveau style
    
    Args:
        modules: Dict des modules
        style: Nouveau style
        font: Nouvelle police
        colors: Nouvelles couleurs (optionnel)
        
    Returns:
        bool: True si succès
    """
    
    if not st.session_state.current_quote:
        st.warning("⚠️ Aucune citation à régénérer")
        return False
    
    quote_data = st.session_state.current_quote
    
    if not colors:
        emotion = st.session_state.get('current_emotion', 'neutral')
        colors = modules['palette'].get_intelligent_palette(emotion)
    
    try:
        palette_tuple = tuple(colors)
        
        img = generate_image_cached(
            quote_data.get('content', ''),
            quote_data.get('author', 'Unknown'),
            palette_tuple,
            style,
            font
        )
        
        st.session_state.current_image = img
        st.toast("✅ Style mis à jour !", icon="✅")
        return True
    
    except Exception as e:
        st.error(f"❌ Erreur régénération: {str(e)}")
        return False


def validate_quote_data(quote_data):
    """Valide les données d'une citation
    
    Args:
        quote_data: Dict avec les données
        
    Returns:
        tuple: (bool, str) - (valide, message d'erreur)
    """
    
    if not quote_data:
        return False, "Données manquantes"
    
    if not quote_data.get('content'):
        return False, "Contenu manquant"
    
    if len(quote_data.get('content', '')) < 10:
        return False, "Citation trop courte"
    
    if len(quote_data.get('content', '')) > 500:
        return False, "Citation trop longue"
    
    return True, ""


def format_quote_for_display(quote_data):
    """Formate une citation pour l'affichage
    
    Args:
        quote_data: Données brutes
        
    Returns:
        Dict formaté
    """
    
    return {
        'content': quote_data.get('content', '').strip(),
        'author': quote_data.get('author', 'Anonyme').strip(),
        'theme': quote_data.get('theme', 'unknown'),
        'emotion': quote_data.get('emotion', 'neutral'),
        'original': quote_data.get('original'),
        'timestamp': quote_data.get('timestamp')
    }