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

## Create and configure database
Install [PostgreSQL](https://www.postgresql.org/download/). Follow the [documentation to configure the database](https://www.postgresql.org/docs/).
Configure the database by granting the DATABASE constant in 
```bash
CRM_EPIC_EVENTS\CRM_EPIC_EVENTS\settings.py
```




