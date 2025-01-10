# 🚀 Price Updater CLI: Mettez à jour vos prix avec style

Un outil en ligne de commande puissant et intuitif pour mettre à jour les prix dans vos fichiers Excel avec des règles d'arrondi personnalisées et un maximum de facilité.

## 🌟 Fonctionnalités

- 🚀 Lecture de fichiers Excel (.xlsx) pour une intégration sans effort
- 💸 Calcul automatique des nouveaux prix avec pourcentage de marge pour une mise à jour rapide
- 🔄 Règles d'arrondi intelligentes pour une précision maximale :
  - 1,2,3,4 → arrondi à 0 pour une simplification
  - 5 → reste inchangé pour une précision totale
  - 6,7,8,9 → arrondi à la dizaine supérieure pour une logique de prix
- 🚀 Génération d'un fichier CSV avec les nouveaux prix pour une exportation facile
- 🔒 Préservation des codes-barres originaux pour une traçabilité parfaite

## 📚 Installation

🔍 Cloner le repository pour commencer
```bash
git clone https://github.com/MrSamy91/CompteDeMontePrize.git
cd price-updater
```
🔑 Créer un environnement virtuel pour une isolation parfaite
```bash
python -m venv venv
```
💻 Activer l'environnement virtuel pour une utilisation sécurisée
```bash
source venv/bin/activate # Linux/Mac
ou
venv\Scripts\activate # Windows
```
📦 Installer les dépendances pour une mise à jour complète
```bash
pip install -r requirements.txt
```

## 📊 Utilisation

1️⃣ Activez votre environnement virtuel pour une sécurité maximale
2️⃣ Lancez le script pour une mise à jour instantanée :
```bash
python hausse_prix.py
```
3️⃣ Suivez les instructions à l'écran pour une expérience utilisateur fluide :
   - Entrez le chemin de votre fichier Excel pour une intégration sans effort
   - Choisissez le pourcentage d'augmentation pour une mise à jour personnalisée
   - Sélectionnez la colonne des prix pour une mise à jour ciblée

## 🚀 Format du fichier Excel

Votre fichier Excel doit contenir :
- Une colonne pour les codes-barres/références pour une identification unique
- Une colonne pour les prix pour une mise à jour facile
- Des en-têtes de colonnes dans la première ligne pour une clarté maximale

## 🚀 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1️⃣ Fork le projet pour une collaboration ouverte
2️⃣ Créer une branche (`git checkout -b feature/AmazingFeature`) pour une gestion de version claire
3️⃣ Commit vos changements (`git commit -m 'Add some AmazingFeature'`) pour une piste d'audit
4️⃣ Push sur la branche (`git push origin feature/AmazingFeature`) pour une mise à jour instantanée
5️⃣ Ouvrir une Pull Request pour une révision collaborative

## 📜 License

Distribué sous la licence MIT pour une liberté maximale. Voir `LICENSE` pour plus d'informations sur les termes de la licence.

## 🤝 Inspiration

Ce projet a été inspiré par le besoin de mettre à jour les prix dans un fichier Excel avec des règles d'arrondi personnalisées.
Je remercie donc un proche a moi qui avait besoin de mettre à jour les prix dans un fichier Excel avec des règles d'arrondi personnalisées. sa prennais de mon temps et ce n'était pas la premiere fois donc je me suis dit autant mettre mes compétence a sa disposition et faire un outil qui me simplifirais la vie au maximum quand il me redemanderais de le faire.