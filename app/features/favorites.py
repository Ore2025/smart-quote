"""Système de favoris avec persistance"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import streamlit as st


class FavoritesManager:
    """Gestion des citations favorites avec persistance"""
    
    def __init__(self, storage_file: str = "data/favorites.json"):
        """
        Args:
            storage_file: Chemin du fichier de stockage
        """
        self.storage_file = Path(storage_file)
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_favorites()
    
    def _load_favorites(self):
        """Charge les favoris depuis le fichier"""
        if self.storage_file.exists():
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    st.session_state.favorites = data.get('favorites', [])
            except Exception as e:
                print(f"⚠️ Erreur chargement favoris: {e}")
                st.session_state.favorites = []
        else:
            st.session_state.favorites = []
    
    def _save_favorites(self):
        """Sauvegarde les favoris dans le fichier"""
        try:
            data = {
                'favorites': st.session_state.favorites,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde favoris: {e}")
    
    def add_favorite(self, quote_data: Dict, emotion: str, theme: str) -> bool:
        """Ajoute une citation aux favoris
        
        Args:
            quote_data: Données de la citation
            emotion: Émotion détectée
            theme: Thème utilisé
            
        Returns:
            True si ajouté avec succès
        """
        # Vérifier si déjà en favoris
        if self.is_favorite(quote_data.get('content', '')):
            st.warning("⚠️ Cette citation est déjà dans vos favoris")
            return False
        
        favorite = {
            'id': len(st.session_state.favorites) + 1,
            'content': quote_data.get('content', ''),
            'author': quote_data.get('author', 'Unknown'),
            'emotion': emotion,
            'theme': theme,
            'timestamp': datetime.now().isoformat(),
            'tags': []
        }
        
        st.session_state.favorites.append(favorite)
        self._save_favorites()
        
        st.toast("❤️ Ajouté aux favoris !", icon="❤️")
        return True
    
    def remove_favorite(self, favorite_id: int) -> bool:
        """Supprime un favori
        
        Args:
            favorite_id: ID du favori à supprimer
            
        Returns:
            True si supprimé avec succès
        """
        initial_count = len(st.session_state.favorites)
        st.session_state.favorites = [
            f for f in st.session_state.favorites 
            if f.get('id') != favorite_id
        ]
        
        if len(st.session_state.favorites) < initial_count:
            self._save_favorites()
            st.toast("🗑️ Retiré des favoris", icon="🗑️")
            return True
        
        return False
    
    def is_favorite(self, content: str) -> bool:
        """Vérifie si une citation est en favoris
        
        Args:
            content: Contenu de la citation
            
        Returns:
            True si en favoris
        """
        return any(
            f.get('content', '') == content 
            for f in st.session_state.favorites
        )
    
    def get_all_favorites(self) -> List[Dict]:
        """Retourne tous les favoris"""
        return st.session_state.favorites
    
    def get_favorites_by_theme(self, theme: str) -> List[Dict]:
        """Filtre les favoris par thème
        
        Args:
            theme: Thème à filtrer
            
        Returns:
            Liste des favoris du thème
        """
        return [
            f for f in st.session_state.favorites 
            if f.get('theme', '').lower() == theme.lower()
        ]
    
    def get_favorites_by_emotion(self, emotion: str) -> List[Dict]:
        """Filtre les favoris par émotion
        
        Args:
            emotion: Émotion à filtrer
            
        Returns:
            Liste des favoris de l'émotion
        """
        return [
            f for f in st.session_state.favorites 
            if f.get('emotion', '').lower() == emotion.lower()
        ]
    
    def search_favorites(self, query: str) -> List[Dict]:
        """Recherche dans les favoris
        
        Args:
            query: Terme de recherche
            
        Returns:
            Liste des favoris correspondants
        """
        query_lower = query.lower()
        return [
            f for f in st.session_state.favorites
            if query_lower in f.get('content', '').lower()
            or query_lower in f.get('author', '').lower()
        ]
    
    def add_tag(self, favorite_id: int, tag: str):
        """Ajoute un tag à un favori
        
        Args:
            favorite_id: ID du favori
            tag: Tag à ajouter
        """
        for favorite in st.session_state.favorites:
            if favorite.get('id') == favorite_id:
                if 'tags' not in favorite:
                    favorite['tags'] = []
                if tag not in favorite['tags']:
                    favorite['tags'].append(tag)
                    self._save_favorites()
                    return True
        return False
    
    def get_stats(self) -> Dict:
        """Retourne des statistiques sur les favoris
        
        Returns:
            Dict avec les stats
        """
        favorites = st.session_state.favorites
        
        if not favorites:
            return {
                'total': 0,
                'themes': {},
                'emotions': {},
                'authors': {}
            }
        
        themes = {}
        emotions = {}
        authors = {}
        
        for fav in favorites:
            # Compter thèmes
            theme = fav.get('theme', 'unknown')
            themes[theme] = themes.get(theme, 0) + 1
            
            # Compter émotions
            emotion = fav.get('emotion', 'neutral')
            emotions[emotion] = emotions.get(emotion, 0) + 1
            
            # Compter auteurs
            author = fav.get('author', 'Unknown')
            authors[author] = authors.get(author, 0) + 1
        
        return {
            'total': len(favorites),
            'themes': dict(sorted(themes.items(), key=lambda x: x[1], reverse=True)),
            'emotions': dict(sorted(emotions.items(), key=lambda x: x[1], reverse=True)),
            'authors': dict(sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5])
        }
    
    def export_favorites(self, format: str = 'json') -> str:
        """Exporte les favoris
        
        Args:
            format: Format d'export ('json', 'txt', 'md')
            
        Returns:
            Contenu exporté
        """
        favorites = st.session_state.favorites
        
        if format == 'json':
            return json.dumps(favorites, indent=2, ensure_ascii=False)
        
        elif format == 'txt':
            lines = []
            for fav in favorites:
                lines.append(f'"{fav.get("content", "")}"')
                lines.append(f'— {fav.get("author", "Unknown")}')
                lines.append(f'Thème: {fav.get("theme", "")} | Émotion: {fav.get("emotion", "")}')
                lines.append('-' * 60)
                lines.append('')
            return '\n'.join(lines)
        
        elif format == 'md':
            lines = ['# Mes Citations Favorites', '']
            for fav in favorites:
                lines.append(f'## {fav.get("author", "Unknown")}')
                lines.append(f'> {fav.get("content", "")}')
                lines.append(f'**Thème:** {fav.get("theme", "")} | **Émotion:** {fav.get("emotion", "")}')
                lines.append('')
            return '\n'.join(lines)
        
        return ''
    
    def clear_all(self):
        """Supprime tous les favoris"""
        st.session_state.favorites = []
        self._save_favorites()
        st.toast("🗑️ Tous les favoris supprimés", icon="🗑️")


def render_favorites_panel():
    """Affiche le panneau des favoris dans Streamlit"""
    
    manager = FavoritesManager()
    
    st.header("❤️ Mes Favoris")
    
    favorites = manager.get_all_favorites()
    
    if not favorites:
        st.info("Aucune citation favorite pour le moment.\nCliquez sur ❤️ pour ajouter une citation !")
        return
    
    # Statistiques
    stats = manager.get_stats()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total", stats['total'])
    with col2:
        if stats['themes']:
            top_theme = list(stats['themes'].keys())[0]
            st.metric("Thème favori", top_theme.capitalize())
    with col3:
        if stats['emotions']:
            top_emotion = list(stats['emotions'].keys())[0]
            st.metric("Émotion", top_emotion.capitalize())
    
    st.divider()
    
    # Filtres
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        filter_theme = st.selectbox(
            "Filtrer par thème",
            ['Tous'] + list(stats['themes'].keys()),
            key='filter_theme'
        )
    
    with col_filter2:
        search_query = st.text_input(
            "🔎 Rechercher",
            placeholder="Auteur ou mot-clé...",
            key='search_fav'
        )
    
    # Filtrer les favoris
    filtered = favorites
    
    if filter_theme != 'Tous':
        filtered = manager.get_favorites_by_theme(filter_theme)
    
    if search_query:
        filtered = manager.search_favorites(search_query)
    
    st.write(f"**{len(filtered)} citation(s)**")
    
    # Afficher les favoris
    for fav in filtered:
        with st.container():
            col_content, col_actions = st.columns([0.85, 0.15])
            
            with col_content:
                st.markdown(f"""
                <div style="
                    background: rgba(30, 41, 59, 0.5);
                    border-left: 3px solid #ec4899;
                    border-radius: 8px;
                    padding: 1rem;
                    margin: 0.5rem 0;
                ">
                    <p style="color: #f1f5f9; margin: 0; font-size: 1rem;">
                        {fav.get('content', '')}
                    </p>
                    <p style="color: #ec4899; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                        — {fav.get('author', 'Unknown')}
                    </p>
                    <p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.8rem;">
                        🎯 {fav.get('theme', 'unknown').capitalize()} • 
                        😊 {fav.get('emotion', 'neutral').capitalize()}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_actions:
                if st.button("🗑️", key=f"del_{fav['id']}", help="Supprimer"):
                    manager.remove_favorite(fav['id'])
                    st.rerun()
    
    st.divider()
    
    # Actions globales
    col_export1, col_export2, col_export3 = st.columns(3)
    
    with col_export1:
        if st.button("📥 Export TXT", use_container_width=True):
            txt_content = manager.export_favorites('txt')
            st.download_button(
                "💾 Télécharger TXT",
                txt_content,
                "favorites.txt",
                "text/plain",
                use_container_width=True
            )
    
    with col_export2:
        if st.button("📥 Export MD", use_container_width=True):
            md_content = manager.export_favorites('md')
            st.download_button(
                "💾 Télécharger MD",
                md_content,
                "favorites.md",
                "text/markdown",
                use_container_width=True
            )
    
    with col_export3:
        if st.button("🗑️ Tout effacer", use_container_width=True):
            if st.session_state.get('confirm_clear'):
                manager.clear_all()
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Cliquez à nouveau pour confirmer")