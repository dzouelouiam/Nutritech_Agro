# 🌾 Nutritech Agro 🌾

## 📋 Description
*Nutritech Agro* est une application web développée avec Django pour le backend et React pour le frontend. Ce projet vise à fournir une interface pour les utilisateurs afin de créer et de gérer des formulaires liés aux conseils agricoles. 🌱 L'application permet aussi aux utilisateurs de commenter sur chaque formulaire pour offrir des recommandations supplémentaires.

## 📂 Structure du Projet

### ⚙️ Backend (Django)
- *accounts* : Application Django pour gérer les utilisateurs, les formulaires, et les commentaires.
  - 📝 *models.py* : Définit les modèles Form (formulaire) et Comment (commentaire).
  - 👀 *views.py* : Contient les vues API pour créer et récupérer les formulaires, ainsi que pour gérer les commentaires.
  - 🔄 *serializers.py* : Sérialise les modèles en JSON pour les exposer via l'API REST.
  - 🔐 *permissions.py* : Définit les permissions personnalisées pour restreindre l'accès à certaines actions.
  - 🌐 *urls.py* : Gère les routes pour chaque point d'accès de l'API.

### 💻 Frontend (React)
- *App.js* : Gère les routes principales de l'application, dont certaines sont protégées pour les utilisateurs authentifiés.
- *components/* :
  - 🔑 *Login.js* : Page de connexion pour les utilisateurs.
  - 📝 *Signup.js* : Page d'inscription pour les nouveaux utilisateurs.
  - 🏠 *Home.js* : Page principale listant les formulaires.
  - 📄 *FormDetail.js* : Détail de chaque formulaire, y compris la fonctionnalité de commentaires.
  - 🔒 *ProtectedRoute.js* : Composant pour protéger les routes nécessitant une authentification.

## 🛠️ Prérequis
- 🐍 *Python 3.7+*
- 🟢 *Node.js et npm*
- 📦 *Django et Django REST Framework*
- ⚛️ *React*

## 🚀 Installation

### 1️⃣ Cloner le Répertoire
bash
# Cloner le dépôt GitHub
git clone https://github.com/dzouelouiam/Nutritech_Agro.git


### 2️⃣ Configuration du Backend (Django)
 -Créez un environnement virtuel 🌐
bash
python -m venv venv
source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`

 -Installez les dépendances Python 📦
bash
pip install -r requirements.txt


 -Effectuez les migrations de la base de données 📅
bash
python manage.py makemigrations
python manage.py migrate


 -Créez un super utilisateur pour accéder à l'interface d'administration 🔐
bash
python manage.py createsuperuser


 -Lancez le serveur Django 🚀
bash
python manage.py runserver


### 3️⃣ Configuration du Frontend (React)
 -Installez les dépendances JavaScript 📦
bash
cd frontend
npm install


 -Lancez le serveur de développement React 🌐
bash
npm start


### 📌 Utilisation
  - Accédez à l'application via http://localhost:3000.
  - Connectez-vous 🔑 ou inscrivez-vous 📝.
  - Créez, éditez ou supprimez des formulaires ✏️.
  - Ajoutez des commentaires pour fournir des conseils 💬.

### 🎯 Fonctionnalités
  - *CRUD des formulaires*: Les utilisateurs peuvent créer, lire, mettre à jour et supprimer des formulaires.
  - *Commentaires* : Chaque formulaire peut recevoir des commentaires.
  - *Authentification* : Les routes */home* et */form/:id* sont protégées et nécessitent une connexion.
  - *Permissions personnalisées*: Seul le propriétaire ou un super utilisateur peut éditer ou supprimer un formulaire.

### 👤 Auteur
 - *DZOU-EL-OUIAM MOHAMED*
