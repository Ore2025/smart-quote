# 💫 Quote Generator Pro

Application web moderne de génération de citations inspirantes avec intelligence artificielle.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://votre-app.streamlit.app)

## ✨ Fonctionnalités

- 🎯 **Génération intelligente** : Citations adaptées au contexte (heure, jour, météo)
- 🌍 **Traduction automatique** : Anglais ↔ Français
- 😊 **Analyse émotionnelle** : Détection du sentiment
- 🎨 **3 styles visuels** : Minimal, Moderne, Élégant
- 🌤️ **Météo intelligente** : Thèmes adaptés à la météo
- 📥 **Export multi-format** : PNG, JPEG, WebP + réseaux sociaux
- ❤️ **Système de favoris** : Sauvegarde et export
- 📊 **Historique** : Statistiques et analytics

## 🚀 Démo en ligne

👉 [**Essayer l'application**](https://votre-app.streamlit.app)

## 📸 Screenshots

![Quote Generator Pro](https://via.placeholder.com/800x400?text=Screenshot)

## 🛠️ Technologies

- **Frontend** : Streamlit
- **Design** : CSS custom avec glassmorphism
- **Traduction** : Deep Translator (Google Translate)
- **Sentiment** : TextBlob + VADER
- **Images** : Pillow (PIL)
- **Database** : TinyDB
- **API** : ZenQuotes, OpenWeather

## 📦 Installation locale

```bash
# Cloner le repo
git clone https://github.com/votre-username/quote-generator-pro.git
cd quote-generator-pro

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app/main_pro.py
```

## 🌐 Déploiement

L'application est déployée sur **Streamlit Community Cloud**.

Pour déployer votre propre version :
1. Fork ce repo
2. Connectez-vous sur [share.streamlit.io](https://share.streamlit.io)
3. Déployez depuis votre fork

## ⚙️ Configuration

### Variables d'environnement (optionnel)

Créer `.streamlit/secrets.toml` :

```toml
OPENWEATHER_API_KEY = "votre_clé_api"
```

## 📁 Structure du projet

```
quote-generator-pro/
├── app/
│   ├── core/           # Logique métier
│   ├── design/         # Génération d'images
│   ├── features/       # Fonctionnalités
│   ├── intelligence/   # Historique & analytics
│   ├── ui/             # Interface utilisateur
│   ├── utils/          # Utilitaires
│   ├── data/           # Citations locales
│   ├── main_pro.py     # Point d'entrée
│   └── styles.css      # Styles CSS
├── .streamlit/
│   └── config.toml     # Configuration Streamlit
├── data/               # Données générées
├── requirements.txt
├── packages.txt
└── README.md
```

## 🎨 Thèmes disponibles

- 💪 Motivation
- ❤️ Amour
- 🧠 Sagesse
- 🎯 Succès
- 😊 Bonheur
- 🦁 Courage
- ✨ Inspiration
- 🤖 Auto (IA)

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

MIT License - Voir [LICENSE](LICENSE)

## 👤 Auteur

Votre Nom - [@votre_twitter](https://twitter.com/votre_twitter)

## 🙏 Remerciements

- [Streamlit](https://streamlit.io/)
- [ZenQuotes API](https://zenquotes.io/)
- [OpenWeather API](https://openweathermap.org/)
- [Deep Translator](https://github.com/nidhaloff/deep-translator)

---

⭐ **N'oubliez pas de laisser une étoile si vous aimez le projet !**