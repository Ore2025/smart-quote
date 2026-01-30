"""Module de gestion de l'historique des citations"""
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import Counter

class HistoryManager:
    """Gère l'historique des citations générées"""
    
    def __init__(self, db_path: str = 'data/quotes_history.json'):
        """Initialise le gestionnaire d'historique
        
        Args:
            db_path: Chemin vers la base de données TinyDB
        """
        # Créer le dossier parent si nécessaire
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.db = TinyDB(db_path)
        self.quotes = self.db.table('quotes')
        self.stats = self.db.table('stats')
    
    def save_quote(self, quote_data: Dict) -> bool:
        """Sauvegarde une citation dans l'historique
        
        Args:
            quote_data: Dict contenant les données de la citation
                       (content, author, theme, emotion, etc.)
            
        Returns:
            True si succès, False sinon
        """
        try:
            # Ajouter timestamp et ID unique
            quote_data['timestamp'] = datetime.now().isoformat()
            quote_data['date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Générer un ID si absent
            if 'id' not in quote_data or not quote_data['id']:
                quote_data['id'] = f"quote_{datetime.now().timestamp()}"
            
            # Sauvegarder
            self.quotes.insert(quote_data)
            
            # Mettre à jour les statistiques
            self._update_stats(quote_data)
            
            return True
            
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde citation: {e}")
            return False
    
    def is_duplicate(self, quote_id: str, days: int = 30) -> bool:
        """Vérifie si une citation a déjà été utilisée récemment
        
        Args:
            quote_id: ID de la citation à vérifier
            days: Nombre de jours à vérifier en arrière
            
        Returns:
            True si la citation existe déjà, False sinon
        """
        Quote = Query()
        
        # Date limite
        limit_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        # Chercher la citation
        results = self.quotes.search(
            (Quote.id == quote_id) & (Quote.timestamp > limit_date)
        )
        
        return len(results) > 0
    
    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Récupère les citations les plus récentes
        
        Args:
            limit: Nombre de citations à retourner
            
        Returns:
            Liste de citations triées par date (plus récent en premier)
        """
        all_quotes = self.quotes.all()
        
        # Trier par timestamp décroissant
        sorted_quotes = sorted(
            all_quotes,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        
        return sorted_quotes[:limit]
    
    def get_by_theme(self, theme: str, limit: int = 10) -> List[Dict]:
        """Récupère les citations d'un thème spécifique
        
        Args:
            theme: Thème recherché
            limit: Nombre maximum de résultats
            
        Returns:
            Liste de citations du thème
        """
        Quote = Query()
        results = self.quotes.search(Quote.theme == theme)
        
        # Trier par date décroissante
        sorted_results = sorted(
            results,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        
        return sorted_results[:limit]
    
    def get_by_emotion(self, emotion: str, limit: int = 10) -> List[Dict]:
        """Récupère les citations d'une émotion spécifique
        
        Args:
            emotion: Émotion recherchée
            limit: Nombre maximum de résultats
            
        Returns:
            Liste de citations de l'émotion
        """
        Quote = Query()
        results = self.quotes.search(Quote.emotion == emotion)
        
        sorted_results = sorted(
            results,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        
        return sorted_results[:limit]
    
    def get_stats(self) -> Dict:
        """Calcule et retourne des statistiques sur l'historique
        
        Returns:
            Dict avec diverses statistiques
        """
        all_quotes = self.quotes.all()
        
        if not all_quotes:
            return {
                'total_quotes': 0,
                'themes': {},
                'emotions': {},
                'authors': {},
                'favorite_theme': None,
                'favorite_emotion': None,
                'favorite_author': None,
                'first_quote_date': None,
                'last_quote_date': None
            }
        
        # Compter les thèmes
        themes = [q.get('theme', 'unknown') for q in all_quotes if q.get('theme')]
        theme_counts = Counter(themes)
        
        # Compter les émotions
        emotions = [q.get('emotion', 'unknown') for q in all_quotes if q.get('emotion')]
        emotion_counts = Counter(emotions)
        
        # Compter les auteurs
        authors = [q.get('author', 'Unknown') for q in all_quotes if q.get('author')]
        author_counts = Counter(authors)
        
        # Dates
        dates = [q.get('timestamp') for q in all_quotes if q.get('timestamp')]
        dates.sort()
        
        return {
            'total_quotes': len(all_quotes),
            'themes': dict(theme_counts.most_common(5)),
            'emotions': dict(emotion_counts.most_common(5)),
            'authors': dict(author_counts.most_common(5)),
            'favorite_theme': theme_counts.most_common(1)[0][0] if theme_counts else None,
            'favorite_emotion': emotion_counts.most_common(1)[0][0] if emotion_counts else None,
            'favorite_author': author_counts.most_common(1)[0][0] if author_counts else None,
            'first_quote_date': dates[0] if dates else None,
            'last_quote_date': dates[-1] if dates else None,
            'quotes_this_week': self._count_quotes_this_period(7),
            'quotes_this_month': self._count_quotes_this_period(30)
        }
    
    def _count_quotes_this_period(self, days: int) -> int:
        """Compte les citations des N derniers jours
        
        Args:
            days: Nombre de jours
            
        Returns:
            Nombre de citations
        """
        Quote = Query()
        limit_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        results = self.quotes.search(Quote.timestamp > limit_date)
        return len(results)
    
    def _update_stats(self, quote_data: Dict):
        """Met à jour les statistiques globales
        
        Args:
            quote_data: Données de la citation
        """
        # Pour l'instant, les stats sont calculées à la volée
        # Possibilité d'ajouter un cache ici pour optimisation
        pass
    
    def clear_old_quotes(self, days: int = 90) -> int:
        """Supprime les citations plus anciennes que N jours
        
        Args:
            days: Âge minimum en jours pour suppression
            
        Returns:
            Nombre de citations supprimées
        """
        Quote = Query()
        limit_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        # Trouver les anciennes citations
        old_quotes = self.quotes.search(Quote.timestamp < limit_date)
        count = len(old_quotes)
        
        # Supprimer
        self.quotes.remove(Quote.timestamp < limit_date)
        
        return count
    
    def export_history(self, output_path: str, format: str = 'json') -> bool:
        """Exporte l'historique vers un fichier
        
        Args:
            output_path: Chemin du fichier de sortie
            format: Format d'export ('json' ou 'csv')
            
        Returns:
            True si succès, False sinon
        """
        try:
            all_quotes = self.quotes.all()
            
            if format == 'json':
                import json
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(all_quotes, f, indent=2, ensure_ascii=False)
            
            elif format == 'csv':
                import csv
                if all_quotes:
                    keys = all_quotes[0].keys()
                    with open(output_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=keys)
                        writer.writeheader()
                        writer.writerows(all_quotes)
            
            return True
            
        except Exception as e:
            print(f"⚠️ Erreur export: {e}")
            return False
    
    def search_quotes(self, keyword: str) -> List[Dict]:
        """Recherche des citations par mot-clé
        
        Args:
            keyword: Mot-clé à rechercher
            
        Returns:
            Liste de citations contenant le mot-clé
        """
        Quote = Query()
        keyword_lower = keyword.lower()
        
        results = self.quotes.search(
            (Quote.content.test(lambda s: keyword_lower in s.lower())) |
            (Quote.author.test(lambda s: keyword_lower in s.lower()))
        )
        
        return sorted(
            results,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
    
    def get_total_count(self) -> int:
        """Retourne le nombre total de citations
        
        Returns:
            Nombre total
        """
        return len(self.quotes.all())
    
    def clear_all(self) -> bool:
        """Supprime tout l'historique (DANGER!)
        
        Returns:
            True si succès
        """
        try:
            self.quotes.truncate()
            self.stats.truncate()
            return True
        except Exception as e:
            print(f"⚠️ Erreur suppression: {e}")
            return False


# Test du module
if __name__ == "__main__":
    print("🧪 Test du HistoryManager\n")
    
    # Utiliser une DB de test
    manager = HistoryManager('data/test_history.json')
    
    # Test 1: Sauvegarder une citation
    print("1️⃣ Sauvegarde de citations:")
    test_quotes = [
        {
            'id': 'quote_1',
            'content': 'Test quote 1',
            'author': 'Author 1',
            'theme': 'motivation',
            'emotion': 'positive'
        },
        {
            'id': 'quote_2',
            'content': 'Test quote 2',
            'author': 'Author 2',
            'theme': 'wisdom',
            'emotion': 'neutral'
        }
    ]
    
    for quote in test_quotes:
        success = manager.save_quote(quote)
        print(f"   {'✅' if success else '❌'} Citation sauvegardée: {quote['id']}")
    print()
    
    # Test 2: Vérifier duplicatas
    print("2️⃣ Test duplicatas:")
    is_dup = manager.is_duplicate('quote_1')
    print(f"   quote_1 est un duplicata: {is_dup}\n")
    
    # Test 3: Récupérer récentes
    print("3️⃣ Citations récentes:")
    recent = manager.get_recent(limit=5)
    print(f"   {len(recent)} citations trouvées\n")
    
    # Test 4: Statistiques
    print("4️⃣ Statistiques:")
    stats = manager.get_stats()
    print(f"   Total: {stats['total_quotes']}")
    print(f"   Thème favori: {stats['favorite_theme']}")
    print(f"   Émotion favorite: {stats['favorite_emotion']}")