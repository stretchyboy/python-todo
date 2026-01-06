
# Flask Todo App with Dual Authentication

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![Render](https://img.shields.io/badge/Deploy-Render-purple)

## Features

- Flask + SQLAlchemy ORM
- **Dual Authentication:**
  - GitHub OAuth (Flask-Dance) for local Windows development
  - Auth0 OAuth for Codespaces and Render production
- Automatic provider detection based on environment
- SQLite (easy to switch to PostgreSQL)
- Ready for Render deployment
- GitHub Actions CI/CD

### Flask

### SQLAlchemy & SQLite

### Authentication (GitHub + Auth0)

### Render

### Github Actions

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

```
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

### Auth0 Setup (Codespaces & Production)

For Codespaces and Render deployment:

1. **Create an Auth0 Account**
   - Go to [auth0.com](https://auth0.com) and sign up

2. **Create an Application**
   - Dashboard → Applications → Create Application
   - Choose "Regular Web Applications"
   - Name: Flask Todo App

3. **Configure Application Settings**
   - "Allowed Callback URLs": 
     - Local: `http://localhost:5000/callback`
     - Codespaces: `https://<codespace-url>/callback`
     - Production: `https://your-app.onrender.com/callback`
   - "Allowed Logout URLs": 
     - Local: `http://localhost:5000/`
     - Production: `https://your-app.onrender.com/`
   - "Allowed Web Origins": Same as callback URLs
    - Codespaces URL format: `https://<CODESPACE_NAME>-5000.<GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN>/` (use `/callback` for the callback and `/` for logout)

4. **Copy Credentials**
   - Add Auth0 Domain, Client ID, and Client Secret to `.env`

## Running the Application

Start the Flask development server:

```bash
python -m flask run
```

The app will be available at [http://localhost:5000](http://localhost:5000)

### Important: Codespaces Port Configuration

If you're running in **GitHub Codespaces**, you must set the forwarded port to **Public** for Auth0 callbacks to work:

1. Open the **Ports** panel (bottom of VS Code)
2. Right-click the port 5000
3. Select "Port Visibility" → **Public**

Without this, Auth0 cannot reach your callback URL and login will fail.

**To use the app:**
1. Visit [http://localhost:5000](http://localhost:5000)
2. Click "Login" - it will automatically route to GitHub (local) or Auth0 (Codespaces)
3. After successful login, manage your todos

## Authentication Resources

- [Flask-Dance Documentation](https://flask-dance.readthedocs.io/)
- [Auth0 Python Quickstart](https://auth0.com/docs/quickstart/webapp/python)
- [Auth0 Dashboard](https://manage.auth0.com/)

## The Database

This code uses [SQLAlchemy](https://www.sqlalchemy.org/) to set up classes that have methods to talk to many [databases](https://docs.sqlalchemy.org/en/20/dialects/index.html) we use SQLite for simplicity here.

### SQLite Viewer extension

The database file is in /instance/

The database can be changed to

## First deployment

Once you have your code how you want

## Deployment on Render

- Add `render.yaml` to repo
- Push to GitHub
- Create Blueprint on Render
- Add environment variables in Render dashboard

## Things we are ignoring

- Persistent records in a database. The current database will be destroyed each time you push to render,  ( we are only testing, not building a real system that works for years).
- Changing database structure SQLAlchemy Migrations. Currently we aren't handling changes to the database structure so you need to delete the local .db and start again (render wil do this anyway on a rebuild as mentioned above). They can be handled with Migrations
- Storing any user data in a database (other than an id from github ). To have users on this system to store any other PII refer to [https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy](https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy) and change the privacy statement.
- Adding extra security [https://flask-security.readthedocs.io/en/stable/quickstart.html#basic-flask-sqlalchemy-application](https://flask-security.readthedocs.io/en/stable/quickstart.html#basic-flask-sqlalchemy-application)
- Testing. There are no tests in this code.
