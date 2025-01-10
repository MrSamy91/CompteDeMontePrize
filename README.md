# 💰 Le Compte de Monte Prize v2.0

Une application web moderne et intuitive pour la mise à jour de vos prix avec des règles d'arrondi personnalisées. Cette nouvelle version apporte une interface utilisateur améliorée et une meilleure expérience utilisateur.

## ✨ Nouvelles Fonctionnalités v2.0

- 🎨 Interface utilisateur complètement repensée
- 📱 Design responsive (compatible mobile)
- 🔄 Sélection multiple des colonnes avec interface visuelle
- 🎯 Menus déroulants personnalisés et intuitifs
- 💫 Animations et transitions fluides
- 🔍 Prévisualisation des colonnes sélectionnées
- ⚡ Traitement optimisé des fichiers

## 🚀 Fonctionnalités Principales

- 📤 Upload simple de fichiers Excel
- 🔢 Règles d'arrondi intelligentes :
  - 1,2,3,4 → arrondi à 0
  - 5 → reste inchangé
  - 6,7,8,9 → arrondi à la dizaine supérieure
- 📊 Conservation des données importantes
- 🚀 Export automatique en CSV
- 🔒 Traitement sécurisé des données

## 💻 Installation

1. **Cloner le repository** :

bash
git clone https://github.com/monte-price/CompteDeMontePrize.git

2. **Créer l'environnement virtuel** 

bash
python -m venv venv

3. **Activer l'environnement virtuel**

bash
source venv/bin/activate

3. **Activer l'environnement** :
- Windows : `venv\Scripts\activate`
- Linux/Mac : `source venv/bin/activate`

4. **Installer les dépendances** :
bash
pip install -r requirements.txt

## 🌐 Utilisation

1. **Lancer l'application** :


2. **Accéder à l'interface** : http://localhost:5000

3. **Processus en 3 étapes** :
   - Étape 1 : Upload du fichier Excel
   - Étape 2 : Sélection des colonnes à conserver
   - Étape 3 : Choix de la colonne prix et du pourcentage

## 🛠️ Technologies

- **Backend** :
  - Flask
  - Pandas
  - Python 3.x
- **Frontend** :
  - HTML5
  - CSS3 (Animations et Flexbox)
  - JavaScript (Vanilla)

## 🔒 Sécurité

- Validation des fichiers uploadés
- Nettoyage automatique des fichiers temporaires
- Traitement sécurisé des données
- Protection contre les injections

## 📋 Format des Fichiers

- Format accepté : `.xlsx`, `.xls`
- Structure requise :
  - Au moins une colonne de prix
  - En-têtes de colonnes obligatoires
  - Données numériques pour les prix

## 🤝 Contribution

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add: nouvelle fonctionnalité'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 License

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## 🌟 Démo

Version de démonstration disponible sur : [comming soon (inshallah)]()

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue.