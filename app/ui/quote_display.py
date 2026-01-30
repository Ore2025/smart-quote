"""Module UI - Affichage de la citation générée"""
import streamlit as st
from app.features.favorites import FavoritesManager


def render_quote_display(quote_data, image, emotion, theme, style, font_name, language):
    """Affiche la citation avec ses métadonnées et l'image
    
    Args:
        quote_data: Données de la citation
        image: Image PIL générée
        emotion: Émotion détectée
        theme: Thème utilisé
        style: Style visuel
        font_name: Nom de la police
        language: Langue sélectionnée
    """
    
    st.divider()
    
    # === CARTE CITATION ===
    st.markdown(f"""
    <div class="quote-card">
        <p class="quote-text">{quote_data.get('content', '')}</p>
        <p class="quote-author">— {quote_data.get('author', 'Anonyme')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # === MÉTRIQUES ===
    _render_metrics(emotion, theme, style, font_name)
    
    # === VERSION ORIGINALE (si traduite) ===
    if language == "Français" and 'original' in quote_data:
        with st.expander("🇬🇧 Version originale"):
            st.markdown(f"""
            <div style="
                padding: 1rem;
                background: rgba(6, 182, 212, 0.1);
                border-left: 3px solid #06b6d4;
                border-radius: 8px;
            ">
                <em>"{quote_data['original']}"</em>
            </div>
            """, unsafe_allow_html=True)
    
    # === IMAGE ===
    st.markdown('<div class="img-container">', unsafe_allow_html=True)
    st.image(image, caption="Votre citation générée")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === ACTIONS RAPIDES - SIMPLIFIÉES ===
    _render_quick_image_actions(image, quote_data, emotion, theme)


def _render_metrics(emotion, theme, style, font_name):
    """Affiche les métriques de la citation"""
    
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Émotion</div>
            <div class="metric-value">{_get_emotion_emoji(emotion)} {emotion.capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Thème</div>
            <div class="metric-value">{_get_theme_emoji(theme)} {theme.capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Style</div>
            <div class="metric-value">🎨 {style.capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Police</div>
            <div class="metric-value">✍️ {font_name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def _render_quick_image_actions(image, quote_data, emotion, theme):
    """Affiche les actions rapides sur l'image"""
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    # Bouton Éditer
    with col1:
        if st.button("✏️ Modifier", use_container_width=True, key="edit_img"):
            st.session_state.show_editor = True
            st.rerun()
    
    # Bouton Favoris
    with col2:
        favorites_mgr = FavoritesManager()
        is_fav = favorites_mgr.is_favorite(quote_data.get('content', ''))
        
        if is_fav:
            if st.button("💔 Retirer", use_container_width=True, key="unfav_img"):
                for fav in st.session_state.favorites:
                    if fav.get('content') == quote_data.get('content'):
                        favorites_mgr.remove_favorite(fav['id'])
                        st.toast("Retiré des favoris", icon="💔")
                        st.rerun()
        else:
            if st.button("❤️ Favoris", use_container_width=True, key="fav_img"):
                favorites_mgr.add_favorite(quote_data, emotion, theme)
                st.toast("Ajouté aux favoris !", icon="❤️")
                st.rerun()
    
    # Bouton Partager
    with col3:
        if st.button("📤 Partager", use_container_width=True, key="share_img"):
            st.session_state.show_share = True
            st.rerun()
    
    # === MODALS ===
    if st.session_state.get('show_editor', False):
        _show_editor_modal()
    
    if st.session_state.get('show_share', False):
        _show_share_modal(quote_data)


def _show_editor_modal():
    """Affiche l'éditeur pour modifier le style"""
    
    st.markdown("---")
    st.markdown("### ✏️ Modifier le Style")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_style = st.selectbox(
            "Nouveau style",
            ["Minimal", "Moderne", "Élégant"],
            key="edit_style"
        )
    
    with col2:
        new_font = st.selectbox(
            "Nouvelle police",
            ["DejaVu Sans", "DejaVu Serif", "Liberation Sans"],
            key="edit_font"
        )
    
    use_custom = st.checkbox("Couleurs personnalisées", key="edit_custom_colors")
    
    if use_custom:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            bg = st.color_picker("Fond", "#0F172A", key="edit_bg")
        with col_b:
            text = st.color_picker("Texte", "#F1F5F9", key="edit_txt")
        with col_c:
            accent = st.color_picker("Accent", "#F59E0B", key="edit_acc")
        colors = [bg, text, accent]
    else:
        colors = None
    
    col_apply, col_cancel = st.columns(2)
    
    with col_apply:
        if st.button("✅ Appliquer", key="apply_edit", use_container_width=True, type="primary"):
            st.session_state.edit_params = {
                'style': new_style.lower(),
                'font': new_font,
                'colors': colors
            }
            st.session_state.show_editor = False
            st.session_state.regenerate = True
            st.rerun()
    
    with col_cancel:
        if st.button("✕ Annuler", key="cancel_edit", use_container_width=True):
            st.session_state.show_editor = False
            st.rerun()


def _show_share_modal(quote_data):
    """Modal de partage avec boutons"""
    
    st.markdown("---")
    st.markdown("### 📤 Partager cette citation")
    
    content = quote_data.get('content', '')
    author = quote_data.get('author', 'Anonyme')
    
    share_text = f'"{content}" - {author}'
    
    # Zone de texte pour copier
    st.text_area("Texte à partager :", share_text, height=100, key="share_text")
    
    # Bouton copier dans le presse-papier
    if st.button("📋 Copier le texte", use_container_width=True, key="copy_text"):
        st.toast("📋 Texte copié ! Collez-le où vous voulez", icon="✅")
    
    st.markdown("---")
    st.markdown("**Ou partagez directement :**")
    
    # Boutons de partage avec liens
    col1, col2, col3 = st.columns(3)
    
    import urllib.parse
    encoded_text = urllib.parse.quote(share_text)
    
    with col1:
        whatsapp_url = f"https://wa.me/?text={encoded_text}"
        st.link_button("📱 WhatsApp", whatsapp_url, use_container_width=True)
    
    with col2:
        twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
        st.link_button("🐦 Twitter", twitter_url, use_container_width=True)
    
    with col3:
        facebook_url = f"https://www.facebook.com/sharer/sharer.php?quote={encoded_text}"
        st.link_button("📘 Facebook", facebook_url, use_container_width=True)
    
    st.markdown("---")
    
    if st.button("✕ Fermer", key="close_share", use_container_width=True):
        st.session_state.show_share = False
        st.rerun()


def _get_emotion_emoji(emotion):
    """Retourne l'emoji correspondant à l'émotion"""
    emotion_emojis = {
        'joy': '😊',
        'motivation': '💪',
        'wisdom': '🧠',
        'love': '❤️',
        'sadness': '😢',
        'anger': '😡',
        'fear': '😰',
        'positive': '😃',
        'neutral': '😐',
        'negative': '😔'
    }
    return emotion_emojis.get(emotion, '😊')


def _get_theme_emoji(theme):
    """Retourne l'emoji correspondant au thème"""
    theme_emojis = {
        'motivation': '💪',
        'wisdom': '🧠',
        'sagesse': '🧠',
        'love': '❤️',
        'amour': '❤️',
        'courage': '🦁',
        'success': '🎯',
        'succès': '🎯',
        'happiness': '😊',
        'bonheur': '😊',
        'inspiration': '✨'
    }
    return theme_emojis.get(theme, '💡')