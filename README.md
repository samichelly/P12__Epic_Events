# P12__CRM_Epic_Events

CRM Epic Events is a command-line customer relationship management (CRM) application that allows users to manage customers, contracts, and events. The application provides functionality for creating, updating, and deleting customers, contracts, and events, as well as user authentication and authorization.

## Features

- User Authentication: Create and log in as users with different roles (sales, support, management).
- Customer Management: Create, update, and delete customer records.
- Contract Management: Create, update, and delete contracts associated with customers.
- Event Management: Create, update, and delete events associated with contracts.
- Role-based Permissions: Users have different permissions based on their roles.
- Sentry Integration: Integrated with Sentry for error tracking and logging.



## Table of Contents

- [Installation](#installation)
- [Create and Configure Database](#create-and-configure-database)
- [Running App](#running-app)
- [Logging with Sentry](#logging-with-sentry)


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/samichelly/P12__Epic_Events.git


2. Navigate to the project directory :

   ```bash
   cd P12__Epic_Events
   ```

3. Create a virtual environment to isolate dependencies :

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment (based on your operating system) :

   - On Windows :

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux :

     ```bash
     source venv/bin/activate
     ```

5. Install dependencies :

   ```bash
   pip install -r requirements.txt
   ```

## Create and configure database
1. Install [PostgreSQL](https://www.postgresql.org/download/). Follow the [documentation to configure the database](https://www.postgresql.org/docs/).
2. Configure the database by granting the DATABASE constant in 
   ```bash
   CRM_EPIC_EVENTS\CRM_EPIC_EVENTS\settings.py
   ```

## Running app
1. Navigate to the file to execute, from the project root :
   ```bash
   cd .\CRM_EPIC_EVENTS\users\
   ```

2. Run :
   ```bash
   python views.py main
   ```

3. Follow the menu

## Logging with Sentry
1. Follow this [documentation](https://docs.sentry.io/platforms/python/)
2. Adapt the 'dsn' value in views.py with your personal 'dsn'


