"""Module UI - Boutons de téléchargement multi-formats"""
import streamlit as st
from io import BytesIO
from datetime import datetime


def render_download_buttons(image, modules, quote_data, config):
    """Affiche les options de téléchargement
    
    Args:
        image: Image PIL à télécharger
        modules: Dict des modules (pour export multi-format)
        quote_data: Données de la citation
        config: Configuration utilisateur
    """
    
    st.divider()
    st.subheader("📥 Téléchargements")
    
    # Timestamp pour noms de fichiers
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # === FORMATS STANDARDS ===
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        _download_png(image, ts)
    
    with col_d2:
        _download_jpeg(image, ts)
    
    with col_d3:
        _download_webp(image, ts)
    
    st.divider()
    
    # === FORMATS RÉSEAUX SOCIAUX ===
    with st.expander("📱 Formats réseaux sociaux"):
        st.write("**Formats optimisés pour différentes plateformes**")
        
        social_formats = [
            ("📸 Instagram Post", (1080, 1080), "instagram_post"),
            ("📱 Instagram Story", (1080, 1920), "instagram_story"),
            ("👥 Facebook Post", (1200, 630), "facebook_post"),
            ("🐦 Twitter/X", (1200, 675), "twitter_post"),
            ("💼 LinkedIn", (1200, 627), "linkedin_post"),
        ]
        
        col_social1, col_social2 = st.columns(2)
        
        for idx, (name, size, key) in enumerate(social_formats):
            col = col_social1 if idx % 2 == 0 else col_social2
            
            with col:
                if st.button(name, key=f"social_{key}", use_container_width=True):
                    with st.spinner(f"Génération {name}..."):
                        try:
                            social_img = _generate_social_format(
                                modules, quote_data, config, size
                            )
                            
                            buf = BytesIO()
                            social_img.save(buf, format='PNG', optimize=True)
                            
                            st.download_button(
                                f"💾 Télécharger {name}",
                                buf.getvalue(),
                                f"quote_{key}_{ts}.png",
                                "image/png",
                                use_container_width=True,
                                key=f"dl_{key}"
                            )
                            st.success(f"✅ {name} prêt !")
                        except Exception as e:
                            st.error(f"❌ Erreur: {str(e)}")


def _download_png(image, timestamp):
    """Bouton téléchargement PNG"""
    buf_png = BytesIO()
    image.save(buf_png, format='PNG', optimize=True)
    
    st.download_button(
        "📄 PNG",
        buf_png.getvalue(),
        f"quote_{timestamp}.png",
        "image/png",
        use_container_width=True,
        key="dl_png",
        help="Meilleure qualité, fichier plus lourd"
    )


def _download_jpeg(image, timestamp):
    """Bouton téléchargement JPEG"""
    buf_jpg = BytesIO()
    img_rgb = image.convert('RGB')
    img_rgb.save(buf_jpg, format='JPEG', quality=95, optimize=True)
    
    st.download_button(
        "🖼️ JPEG",
        buf_jpg.getvalue(),
        f"quote_{timestamp}.jpg",
        "image/jpeg",
        use_container_width=True,
        key="dl_jpg",
        help="Bonne qualité, fichier léger"
    )


def _download_webp(image, timestamp):
    """Bouton téléchargement WebP"""
    buf_webp = BytesIO()
    image.save(buf_webp, format='WEBP', quality=90, optimize=True)
    
    st.download_button(
        "🌐 WebP",
        buf_webp.getvalue(),
        f"quote_{timestamp}.webp",
        "image/webp",
        use_container_width=True,
        key="dl_webp",
        help="Format moderne, très léger"
    )


def _generate_social_format(modules, quote_data, config, size):
    """Génère une image dans un format social spécifique
    
    Args:
        modules: Dict des modules
        quote_data: Données citation
        config: Configuration
        size: Tuple (width, height)
        
    Returns:
        Image PIL redimensionnée
    """
    # Sauvegarder taille originale
    original_size = modules['generator'].size
    
    try:
        # Changer temporairement la taille
        modules['generator'].size = size
        
        # Régénérer avec la nouvelle taille
        palette = config.get('colors') or ['#0F172A', '#F1F5F9', '#F59E0B']
        
        img = modules['generator'].create_image(
            quote_data.get('content', ''),
            quote_data.get('author', 'Unknown'),
            palette,
            style=config['style'],
            font_family=config['font']
        )
        
        return img
    
    finally:
        # Restaurer taille originale
        modules['generator'].size = original_size