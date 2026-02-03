# Flask Todo App Starter

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![Render](https://img.shields.io/badge/Deploy-Render-purple)

A simple Python Todo Web App to do some improvements on and be a starting point for your own simple web apps.

---

## Features

### Flask

- [Flask](https://flask.palletsprojects.com/en/stable/) based Python Webserver with routing (a function for each url endpoint users can visit)
- HTML / [Jinja templates](https://jinja.palletsprojects.com/en/stable/templates/) for looping though and outputting data.
- todo.py contains the endpoints for the Todo app

---

### SQLAlchemy & SQLite / PostgreSQL

- SQL Databases the modern way
- Managed by [SQLAlchemy](https://www.sqlalchemy.org/) an ORM /  [Object Relationship Mapper](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) which allows you to write classes that define the data and provides the storage & [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) for you.

---
###  [Object Relationship Mapper](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping)

- ORMs build the database for you from your classes so you define what you want to store how it connects together and any extras calculations / functions you need .
- Start with SQLite but you can move to proffesional systems like PostgreSQL or others when you are ready.
- todo.py includes the Todo class that provdes all you need for the building of the database and all the [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete).

---

### Authentication (GitHub + Auth0)

Authentication is the act of proving who you are, in this system we use external authentication systems so we aren't storing usernames & passwords (reducing the DPA responsiblilties ). There are still some so we provide a privacy policy.

- GitHub OAuth (Flask-Dance) for local Windows development
- Auth0 OAuth for Codespaces and Render production

---

### Render & Github Actions

- Ready for [Render](https://render.com/)  deployment so you can publish and use the site online for free (there are some speed limitations)
- GitHub Actions CI/CD to build the site when you commit a working version
- Can be upgraded to use a free PostgreSQL database server (but there are some other steps)

---

## Setup

### Start from the Template

1. Login to [github.com](https://github.com/)
2. Go to the github repository [https://github.com/UTCSheffield/python-flask-todo](https://github.com/UTCSheffield/python-flask-todo)
3. Click the green "Use this template" button at the top of the page
4. Select "Create a new repository"
5. Fill in your new repository details:
   - Choose a repository name (e.g., `python-flask-todo`)
   - Add a description (optional)
   - Choose Public or Private visibility
6. Click "Create repository from template"
7. Your new repository will be created with all the template files

---

### Clone your Repository locally

**Using GitHub Desktop:**

1. On the GitHub page for your new repository
2. Click the green "Code" button
3. Click "Open with GitHub Desktop"
4. You may need to login to GitHub Desktop if you haven't already
5. You may be prompted to choose a local path to clone the repository to
6. Click 'Open in Visual Studio Code' to open the project in VS Code

---

**Using Git Command Line:**

```bash
git clone https://github.com/UTCSheffield/python-flask-todo.git
cd python-flask-todo
```

---

### Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

---

### Environment Configuration (.env)

```bash
cp .env.example .env
```

---

## Authentication Setup

### How It Works

This app automatically detects your environment and uses the appropriate authentication provider:

- **Local Windows Machine** → GitHub OAuth (via Flask-Dance)
- **GitHub Codespaces** → Auth0 OAuth
- **Render Production** → Auth0 OAuth

The app checks for Codespaces environment variables (`CODESPACES`, `CODESPACE_NAME`) and routes accordingly.

---

### GitHub OAuth Setup (Local Development)

For local Windows development with GitHub Desktop:

1. **Create a GitHub OAuth App**
   - Go to [GitHub Settings → Developer settings → OAuth Apps](https://github.com/settings/developers)
   - Click "New OAuth App"
   - Set "Application name": Flask Todo App
   - Set "Homepage URL": `http://localhost:5000`
   - Set "Application description": Local development
   - Set "Authorization callback URL": `http://localhost:5000/login/github/authorized`

2. **Get Your Credentials**
   - Copy the "Client ID" and generate a "Client Secret"
   - Add them to your `.env` file as `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`

3. **Enable Insecure Transport for Local Dev**
   - Set `OAUTHLIB_INSECURE_TRANSPORT=1` in `.env` (only for local development)

---

## Running the Application

Start the Flask development server:

```bash
python3 -m flask run --host=localhost --port=5000
```

The app will be available at [http://localhost:5000](http://localhost:5000)

Try it, login and create a few tasks!

---

## The Database

This code uses [SQLAlchemy](https://www.sqlalchemy.org/) to set up classes that have methods to talk to many [databases](https://docs.sqlalchemy.org/en/20/dialects/index.html). We use **SQLite for simplicity and easy local development**.

### Local Development (SQLite)

The database file is stored in `/instance/todo.db`

Hopefully Visual Code has promoted you to install the recommended extensions including the SQLite extension. and so todo.db should appear in the left hand side explorer view with a red icon.

Have a look, can you see the tables and data?

---

## Things we are ignoring

- Persistent records in a database. The current database will be destroyed each time you push to render,  ( You can modify the code once it's on Render to move to PostgreSQL ).
- Changing database structure SQLAlchemy Migrations. Currently we aren't handling changes to the database structure so you need to delete the local .db and start again (render wil do this anyway on a rebuild as mentioned above). They can be handled with Migrations
- Minimal Autorisation all Authenticated users can do everything on the site.
- Storing any user data in a database (other than an id from github or Auth0 ). To have users on this system to store any other PII refer to [https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy](https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy) and change the privacy statement.
- Adding extra security [https://flask-security.readthedocs.io/en/stable/quickstart.html#basic-flask-sqlalchemy-application](https://flask-security.readthedocs.io/en/stable/quickstart.html#basic-flask-sqlalchemy-application)
- Testing. There are no tests in this code, although Flask, SQL Alchemy and the other libraries used are thoroughly tested and are checked for security issues.

---

## Your Development

Try [ADDING_CATERGORIES.md](ADDING_CATERGORIES.md) to add a one-to-many relationship and Categories for the tasks.

Then what could you make with the same ideas but different entities (things)? 

Books and People could make a library etc ....

---


## Deployment on Render

See [RENDER_SETUP.md](RENDER_SETUP.md) for complete Render deployment instructions, including setup, configuration, environment variables, and continuous deployment.


## Codespaces Setup

See [CODESPACES_SETUP.md](CODESPACES_SETUP.md) for complete GitHub Codespaces setup instructions.