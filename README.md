# Flask Todo App Starter

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![Render](https://img.shields.io/badge/Deploy-Render-purple)

## Features
<!--
- Flask + SQLAlchemy ORM
   - Webserver with SQL Database 
   - Managed by an Object Relationship Manager which allows you to write classes that define the data
   - Jinja templates 
- **Dual Authentication:**
  - GitHub OAuth (Flask-Dance) for local Windows development
  - Auth0 OAuth for Codespaces and Render production
- Automatic provider detection based on environment
- SQLite (easy to switch to PostgreSQL)
- Ready for Render deployment
- GitHub Actions CI/CD
-->

### Flask

- Webserver with routing (a function for each url endpoint)
- Jinja templates for looping though and outputting data.
- todo.py contains the endpoints for the Todo app

### SQLAlchemy & SQLite / PostgreSQL

- SQL Database 
- Managed by SQLAlchemy an Object Relationship Manager which allows you to write classes that define the data and provides the storage & CRUD for you.
- ORMs build the database for you from your classes, start with SQLite but you can move PostgreSQL or others when you are ready.
- todo.py includes the Todo class that provdes all you need for the building of the database and all the CRUD. 

### Authentication (GitHub + Auth0)

- GitHub OAuth (Flask-Dance) for local Windows development
- Auth0 OAuth for Codespaces and Render production

### Render & Github Actions

- Ready for Render deployment
- GitHub Actions CI/CD

## Setup

### Clone the Repository

**Using Git Command Line:**

```bash
git clone https://github.com/stretchyboy/python-todo.git
cd python-todo
```

**Using GitHub Desktop:**

1. Open GitHub Desktop
2. Click `File` → `Clone repository`
3. Select the `URL` tab
4. Enter: `https://github.com/stretchyboy/python-todo.git`
5. Choose a local path and click `Clone`

### Install Dependencies

```bash
py -m pip install -r requirements.txt
```

### Copy Example Environment File

```bash
# On linux or codespaces
cp .env.example .env
```

### On Windows in VS Code

Open `.env.example` and save as `.env`

## Environment Configuration (.env)

Create a `.env` file in the root directory with the following variables:

```bash
APP_SECRET_KEY=your-secret-key-here
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
AUTH0_DOMAIN=your-auth0-domain.auth0.com
AUTH0_CLIENT_ID=your-auth0-client-id
AUTH0_CLIENT_SECRET=your-auth0-client-secret
AUTH0_CALLBACK_URL=http://localhost:5000/callback
OAUTHLIB_INSECURE_TRANSPORT=1
```

### Generate APP_SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Authentication Setup

### How It Works

This app automatically detects your environment and uses the appropriate authentication provider:

- **Local Windows Machine** → GitHub OAuth (via Flask-Dance)
- **GitHub Codespaces** → Auth0 OAuth
- **Render Production** → Auth0 OAuth

The app checks for Codespaces environment variables (`CODESPACES`, `CODESPACE_NAME`) and routes accordingly.

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

## Running the Application

Start the Flask development server:

```bash
py -m flask run --host=localhost --port=5000  # it maybe python3 on your machine
```

The app will be available at [http://localhost:5000](http://localhost:5000)

## The Database

This code uses [SQLAlchemy](https://www.sqlalchemy.org/) to set up classes that have methods to talk to many [databases](https://docs.sqlalchemy.org/en/20/dialects/index.html). We use **SQLite for simplicity and easy local development**.

### Local Development (SQLite)

The database file is stored in `/instance/todo.db`

## Things we are ignoring

- Persistent records in a database. The current database will be destroyed each time you push to render,  ( You can modify the code once it's on Render to move to PostgreSQL ).
- Changing database structure SQLAlchemy Migrations. Currently we aren't handling changes to the database structure so you need to delete the local .db and start again (render wil do this anyway on a rebuild as mentioned above). They can be handled with Migrations
- Storing any user data in a database (other than an id from github ). To have users on this system to store any other PII refer to [https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy](https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy) and change the privacy statement.
- Adding extra security [https://flask-security.readthedocs.io/en/stable/quickstart.html#basic-flask-sqlalchemy-application](https://flask-security.readthedocs.io/en/stable/quickstart.html#basic-flask-sqlalchemy-application)
- Testing. There are no tests in this code.

## Your Development

Try [ADDING_CATERGORIES.md](ADDING_CATERGORIES.md) to add one-to-many relationship and Catergories for the tasks.

Then what could you make with the same ideas but different entities (things)? 

Books and People could make a library etc ....


## Codespaces Setup

See [CODESPACES_SETUP.md](CODESPACES_SETUP.md) for complete GitHub Codespaces setup instructions.

## Deployment on Render

See [RENDER_SETUP.md](RENDER_SETUP.md) for complete Render deployment instructions, including setup, configuration, environment variables, and continuous deployment.
