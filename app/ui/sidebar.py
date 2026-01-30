"""Module UI - Sidebar avec configuration"""
import streamlit as st


FONT_OPTIONS = {
    'DejaVu Sans': 'DejaVu Sans',
    'DejaVu Serif': 'DejaVu Serif',
    'Liberation Sans': 'Liberation Sans',
    'Ubuntu': 'Ubuntu'
}


def render_sidebar(modules):
    """Affiche la sidebar avec configuration
    
    Args:
        modules: Dict des modules initialisés
        
    Returns:
        Dict avec la configuration sélectionnée
    """
    
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        language = st.radio(
            "🌍 Langue", 
            ["Français", "Anglais"], 
            index=0
        )
        
        try:
            themes = modules['fetcher'].get_available_themes()
            theme_list = ['Auto (IA)'] + [t.capitalize() for t in themes if t != 'auto']
        except:
            theme_list = ['Auto (IA)', 'Inspiration', 'Motivation', 'Sagesse', 'Amour']
        
        theme = st.selectbox("💡 Thème", theme_list)
        
        style = st.selectbox(
            "🎨 Style", 
            ["Minimal", "Moderne", "Élégant"], 
            index=1
        )
        
        font_name = st.selectbox(
            "✍️ Police", 
            list(FONT_OPTIONS.keys())
        )
        font = FONT_OPTIONS[font_name]
        
        st.divider()
        
        with st.expander("🔧 Options avancées"):
            dark_mode = st.checkbox("🌙 Mode sombre", value=True)
            
            use_weather = st.checkbox("🌤️ Météo intelligente")
            location = None
            if use_weather:
                location = st.text_input(
                    "📍 Ville",
                    value="Cotonou,BJ",
                    help="Format: Ville,Code Pays (ex: Paris,FR)"
                )
            
            custom_colors = st.checkbox("🎨 Couleurs personnalisées")
            
            colors = None
            if custom_colors:
                col_a, col_b = st.columns(2)
                with col_a:
                    bg = st.color_picker("Fond", "#0E1117")
                    text = st.color_picker("Texte", "#FAFAFA")
                with col_b:
                    accent = st.color_picker("Accent", "#FF6B6B")
                
                colors = [bg, text, accent]
        
        st.divider()
        
        _render_context_info(modules, use_weather if 'use_weather' in locals() else False, location)
        
        st.divider()
        
        _render_statistics(modules)
        
        _render_history(modules)
        
        st.divider()
        
        _render_favorites()
    
    return {
        'language': language,
        'theme': theme,
        'style': style.lower(),
        'font': font,
        'font_name': font_name,
        'dark_mode': dark_mode,
        'colors': colors,
        'use_weather': use_weather if 'use_weather' in locals() else False,
        'location': location if 'location' in locals() else None
    }


def _render_context_info(modules, use_weather, location):
    """Affiche contexte avec météo optionnelle"""
    try:
        context = modules['context'].get_time_context()
        
        msg = f"**{context.get('greeting', 'Bonjour')}** 👋\n\n"
        msg += f"📅 {context.get('day_of_week', '')}\n"
        msg += f"🕐 {context.get('time', '')}\n"
        
        if use_weather and location:
            weather_ctx = modules['context'].get_weather_context(location)
            if weather_ctx:
                msg += f"{weather_ctx['emoji']} {weather_ctx['temperature']:.0f}°C\n"
                msg += f"💡 *{weather_ctx['weather_theme'].capitalize()}*"
            else:
                msg += f"🎯 *{context.get('time_theme', 'inspiration').capitalize()}*"
        else:
            msg += f"🎯 *{context.get('time_theme', 'inspiration').capitalize()}*"
        
        st.info(msg)
    except Exception as e:
        st.warning(f"⚠️ Contexte indisponible")


def _render_statistics(modules):
    """Affiche statistiques"""
    with st.expander("📊 Statistiques"):
        try:
            stats = modules['history'].get_stats()
            
            if stats.get('total_quotes', 0) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Total", stats.get('total_quotes', 0))
                    st.metric(
                        "Thème favori", 
                        (stats.get('favorite_theme') or '—').capitalize()
                    )
                
                with col2:
                    st.metric("Thèmes", len(stats.get('themes', {})))
                    st.metric(
                        "Émotion", 
                        (stats.get('favorite_emotion') or '—').capitalize()
                    )
                
                st.divider()
                session_count = st.session_state.get('session_count', 0)
                st.metric("Session", session_count)
            else:
                st.info("Aucune stat disponible")
        
        except Exception as e:
                            st.error(f"❌ Erreur: {str(e)}")


def _render_history(modules):
    """Affiche historique"""
    with st.expander("📜 Historique"):
        search_term = st.text_input(
            "🔎 Rechercher", 
            placeholder="Auteur...",
            key="search_history"
        )
        
        try:
            recent = modules['history'].get_recent(10)
            
            if search_term:
                recent = [
                    q for q in recent 
                    if search_term.lower() in q.get('author', '').lower() 
                    or search_term.lower() in q.get('content', '').lower()
                ]
            
            if recent:
                for i, q in enumerate(recent[:5], 1):
                    st.markdown(f"**{i}. {q.get('author', 'Anonyme')}**")
                    content = q.get('content', '')
                    st.caption(f"{content[:60]}{'...' if len(content) > 60 else ''}")
                    
                    theme = q.get('theme', 'unknown')
                    emotion = q.get('emotion', 'neutral')
                    st.caption(f"🎯 {theme} • 😊 {emotion}")
                    
                    if i < len(recent[:5]):
                        st.markdown("---")
            else:
                st.info("Aucune citation")
        
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
        
        st.divider()
        if st.button("🗑️ Effacer", use_container_width=True):
            try:
                modules['history'].clear_all()
                st.success("✅ Historique effacé")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")


def _render_favorites():
    """Affiche panel favoris"""
    from app.features.favorites import FavoritesManager
    
    with st.expander("❤️ Mes Favoris"):
        mgr = FavoritesManager()
        favorites = mgr.get_all_favorites()
        
        if not favorites:
            st.info("Aucun favori.\nCliquez sur ❤️ sous une citation !")
            return
        
        stats = mgr.get_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", stats['total'])
        with col2:
            if stats['themes']:
                top_theme = list(stats['themes'].keys())[0]
                st.metric("Top", top_theme.capitalize())
        
        st.divider()
        
        search = st.text_input("🔎 Rechercher", key="search_fav")
        
        filtered = favorites
        if search:
            filtered = mgr.search_favorites(search)
        
        for fav in filtered[:5]:
            st.markdown(f"**{fav.get('author', 'Anonyme')}**")
            content = fav.get('content', '')
            st.caption(f"{content[:50]}...")
            st.caption(f"🎯 {fav.get('theme', '')} • 😊 {fav.get('emotion', '')}")
            
            if st.button("🗑️", key=f"del_fav_{fav['id']}", help="Supprimer"):
                mgr.remove_favorite(fav['id'])
                st.rerun()
            
            st.markdown("---")
        
        if len(filtered) > 5:
            st.caption(f"+ {len(filtered) - 5} autres...")
        
        st.divider()
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            txt = mgr.export_favorites('txt')
            st.download_button("📥 TXT", txt, "favoris.txt", use_container_width=True)
        with col_exp2:
            md = mgr.export_favorites('md')
            st.download_button("📥 MD", md, "favoris.md", use_container_width=True)