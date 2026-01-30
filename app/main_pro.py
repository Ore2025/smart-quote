"""Quote Generator Pro"""
import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from app.ui.header import render_header
from app.ui.sidebar import render_sidebar
from app.ui.quote_display import render_quote_display
from app.ui.download_buttons import render_download_buttons
from app.ui.quick_actions import render_quick_actions
from app.utils.session import init_session_state, init_modules
from app.utils.quote_processor import process_quote_generation

st.set_page_config(
    page_title="Quote Generator Pro",
    page_icon="💫",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    css_file = Path(__file__).parent / "styles.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

def main():
    init_session_state()
    modules = init_modules()
    
    render_header()
    
    config = render_sidebar(modules)
    
    quick_theme = render_quick_actions()
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        gen_btn = st.button("🎲 Aléatoire", use_container_width=True, key="gen")
    
    with col2:
        smart_btn = st.button("✨ Intelligente", use_container_width=True, type="primary", key="smart")
    
    if st.session_state.get('regenerate', False):
        edit_params = st.session_state.get('edit_params', {})
        
        if edit_params.get('style'):
            config['style'] = edit_params['style']
        if edit_params.get('font'):
            config['font'] = edit_params['font']
        if edit_params.get('colors'):
            config['colors'] = edit_params['colors']
        
        from app.utils.cache_utils import generate_image_cached
        
        quote_data = st.session_state.current_quote
        palette = config['colors'] or ['#0E1117', '#FAFAFA', '#FF6B6B']
        
        try:
            img = generate_image_cached(
                quote_data.get('content', ''),
                quote_data.get('author', 'Unknown'),
                tuple(palette),
                config['style'],
                config['font']
            )
            st.session_state.current_image = img
            st.toast("✅ Style mis à jour !", icon="✅")
        except Exception as e:
            st.error(f"❌ {str(e)}")
        
        st.session_state.regenerate = False
        st.rerun()
    
    should_generate = gen_btn or smart_btn or quick_theme
    
    if should_generate:
        with st.spinner("✨ Création..."):
            if quick_theme:
                selected_theme = quick_theme
            elif smart_btn or config['theme'] == 'Auto (IA)':
                try:
                    selected_theme = modules['context'].suggest_theme_intelligent(
                        use_weather=config.get('use_weather', False),
                        location=config.get('location')
                    )
                except:
                    selected_theme = 'inspiration'
            else:
                selected_theme = config['theme'].lower()
            
            success = process_quote_generation(
                modules=modules,
                theme=selected_theme,
                language=config['language'],
                style=config['style'],
                font=config['font'],
                colors=config['colors'],
                dark_mode=config['dark_mode'],
                use_weather=config.get('use_weather', False),
                location=config.get('location')
            )
            
            if success:
                st.session_state.session_count += 1
                st.toast("✅ Citation générée !", icon="✅")
                st.rerun()
            else:
                st.error("❌ Erreur de génération")
    
    if st.session_state.current_quote and st.session_state.current_image:
        render_quote_display(
            quote_data=st.session_state.current_quote,
            image=st.session_state.current_image,
            emotion=st.session_state.get('current_emotion', 'neutral'),
            theme=st.session_state.get('current_theme', 'unknown'),
            style=config['style'],
            font_name=config['font_name'],
            language=config['language']
        )
        
        render_download_buttons(
            image=st.session_state.current_image,
            modules=modules,
            quote_data=st.session_state.current_quote,
            config=config
        )
        
        st.markdown("---")
        if st.button("🔄 Nouvelle citation", use_container_width=True, key="new_quote"):
            st.session_state.current_quote = None
            st.session_state.current_image = None
            st.rerun()
    else:
        st.info("👆 **Pour commencer :** Choisissez un thème ou cliquez sur un bouton")

if __name__ == "__main__":
    main()