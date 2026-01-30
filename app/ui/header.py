"""Module UI - Header et bannière de bienvenue"""
import streamlit as st


def render_header():
    """Affiche le header de l'application avec bannière de bienvenue"""
    
    # Header principal toujours visible
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">
            <span class="app-title-emoji">💫</span> Quote Generator Pro
        </h1>
        <p class="app-subtitle">
            Créez des citations inspirantes avec style et intelligence artificielle
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bannière de bienvenue (fermable)
    if st.session_state.get('show_welcome', True):
        col_welcome, col_close = st.columns([0.95, 0.05])
        
        with col_welcome:
            st.markdown("""
            <div class="welcome-banner">
                <div class="welcome-title">👋 Bienvenue sur Quote Generator Pro !</div>
                <div class="welcome-text">
                    Découvrez des citations inspirantes personnalisées grâce à l'intelligence artificielle. 
                    Choisissez votre thème, votre style et générez des images magnifiques en quelques clics.
                    <br><br>
                    <strong>✨ Nouveautés :</strong> Mode intelligent, palettes adaptatives, historique amélioré
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_close:
            if st.button("✕", key="close_welcome", help="Fermer la bannière"):
                st.session_state.show_welcome = False
                st.rerun()