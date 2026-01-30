"""Module UI - Actions rapides compactes style pills"""
import streamlit as st


def render_quick_actions():
    """Affiche les boutons d'actions rapides - Style Pills Compact
    
    Returns:
        str: Thème sélectionné ou None
    """
    
    # Configuration des thèmes
    themes_quick = [
        ("💪", "Motivation", "motivation"),
        ("❤️", "Amour", "amour"),
        ("🧠", "Sagesse", "sagesse"),
        ("🎯", "Succès", "succès"),
        ("😊", "Bonheur", "bonheur")
    ]
    
    # Style personnalisé pour pills
    st.markdown("""
    <style>
    /* Container pour les pills */
    .pills-container {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 1rem 0;
        justify-content: center;
    }
    
    /* Style pill button */
    .pill-btn {
        background: rgba(26, 33, 64, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 0.4rem 1rem;
        color: #b8c1ec;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        white-space: nowrap;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    .pill-btn:hover {
        background: linear-gradient(135deg, #00d4ff 0%, #a855f7 50%, #ff006e 100%);
        border-color: transparent;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
    }
    
    .pill-emoji {
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Affichage HTML des pills
    st.markdown('<div class="pills-container">', unsafe_allow_html=True)
    
    selected_theme = None
    
    # Créer les colonnes pour les boutons
    cols = st.columns(len(themes_quick), gap="small")
    
    for col, (emoji, label, theme) in zip(cols, themes_quick):
        with col:
            if st.button(
                f"{emoji} {label}",
                key=f"quick_{theme}",
                use_container_width=True,
                help=f"Citation {label.lower()}"
            ):
                selected_theme = theme
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return selected_theme