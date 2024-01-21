# P12__CRM_Epic_Events

CRM Epic Events is a command-line customer relationship management (CRM) application that allows users to manage customers, contracts, and events. The application provides functionality for creating, updating, and deleting customers, contracts, and events, as well as user authentication and authorization.

## Features

- User Authentication: Create and log in as users with different roles (sales, support, management).
- Customer Management: Create, update, and delete customer records.
- Contract Management: Create, update, and delete contracts associated with customers.
- Event Management: Create, update, and delete events associated with contracts.
- Role-based Permissions: Users have different permissions based on their roles.
- Sentry Integration: Integrated with Sentry for error tracking and logging.



## Table des matières

- [Installation](#installation)
- [Create database](#database)
- [Utilisation](#utilisation)
- [Création d'un nouvel utilisateur](#creation)


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/samichelly/P12__Epic_Events.git


2. Accédez au répertoire du projet :

   ```bash
   cd P12__Epic_Events
   ```

3. Créez un environnement virtuel pour isoler les dépendances :

   ```bash
   python -m venv venv
   ```

4. Activez l'environnement virtuel (selon votre système d'exploitation) :

   - Sur Windows :

     ```bash
     venv\Scripts\activate
     ```

   - Sur macOS et Linux :

     ```bash
     source venv/bin/activate
     ```

5. Installez les dépendances à partir du fichier `requirements.txt` :

   ```bash
   pip install -r requirements.txt
   ```

## Create database
Install [PostgreSQL](https://www.postgresql.org/download/). Follow the documentation to run the server.





## Utilisation

1. Démarrez le serveur de développement Django :

   ```bash
   python manage.py runserver
   ```

2. Accédez à l'application depuis le navigateur de votre choix, se rendre à l'adresse → http://127.0.0.1:8000/ .

3. Vous pouvez maintenant vous inscrire, vous connecter, créer des tickets, des reviews, suivre d'autres utilisateurs et intéragir ensemble.
4. 

## Création d'un nouvel utilisateur

Pour créer un nouvel utilisateur, suivez les étapes suivantes :
1. Accédez à la page d'inscription de l'application en se rendant à l'adresse → http://127.0.0.1:8000/signup .
2. Remplissez le formulaire d'inscription en fournissant les informations, telles que le nom d'utilisateur, l'adresse e-mail et le mot de passe.
3. Cliquez sur le bouton "Valider" pour soumettre le formulaire.
4. Une fois le formulaire soumis avec succès, vous serez redirigé vers la page de connexion.
5. Utilisez vos informations d'identification pour vous connecter à l'application.

Comptes utilisateurs :

Identifiant : lecteur1 | Mot de passe : litreview

Identifiant : lecteur2 | Mot de passe : litreview


### Django administration
Identifiant : Admin | Mot de passe : litreview

→ http://127.0.0.1:8000/admin/
