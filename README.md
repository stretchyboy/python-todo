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

This code uses [SQLAlchemy](https://www.sqlalchemy.org/) to set up classes that have methods to talk to many [databases](https://docs.sqlalchemy.org/en/20/dialects/index.html). We use **SQLite for simplicity and easy local development**.

### Local Development (SQLite)

The database file is stored in `/instance/todo.db`

### Production Deployment (SQLite)

For initial deployment on Render, SQLite works fine for testing and small user bases. The database persists in Render's filesystem.

### Upgrading to PostgreSQL

Once your app grows and you need a more robust database, see [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) for a complete migration guide.

## Deployment on Render

### Prerequisites

1. **GitHub Repository**: Your code must be pushed to a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com) (free tier available)
3. **Auth0 Application**: Configured with your production callback URL

### Step 1: Prepare Your Repository

Ensure your repository contains:
- `render.yaml` (blueprint configuration file)
- `requirements.txt` (Python dependencies)
- All application code pushed to GitHub

### Step 2: Create a Blueprint on Render

1. **Log in to Render Dashboard**
   - Go to [dashboard.render.com](https://dashboard.render.com)

2. **Create New Blueprint**
   - Click the "New +" button in the top right
   - Select "Blueprint" from the dropdown menu
   - [Direct Link to Create Blueprint](https://dashboard.render.com/select-repo?type=blueprint)

3. **Connect Your GitHub Repository**
   - Click "Connect account" if this is your first time
   - Authorize Render to access your GitHub repositories
   - Search for and select `mr-eggleton/python-flask-todo` (or your fork)
   - Click "Connect"

4. **Review Blueprint Configuration**
   - Render will detect your `render.yaml` file
   - Review the services that will be created (web service, database, etc.)
   - Give your blueprint instance a name (e.g., "flask-todo-app")
   - Click "Apply"

### Step 3: Configure Environment Variables

After the blueprint is created, you need to add your environment variables:

1. **Navigate to Your Web Service**
   - In the Render dashboard, click on your web service
   - Go to the "Environment" tab

2. **Add Environment Variables**
   - Click "Add Environment Variable"
   - Add each variable:
     ```
     APP_SECRET_KEY=<generate-new-secret-key>
     AUTH0_DOMAIN=<your-auth0-domain>.auth0.com
     AUTH0_CLIENT_ID=<your-auth0-client-id>
     AUTH0_CLIENT_SECRET=<your-auth0-client-secret>
     AUTH0_CALLBACK_URL=https://<your-app-name>.onrender.com/callback
     ```
   - **Important**: Generate a NEW `APP_SECRET_KEY` for production (don't reuse your local one)
   - **Note**: Do NOT set `OAUTHLIB_INSECURE_TRANSPORT` in production
   - Click "Save Changes"

3. **Automatic Deployment**
   - Render will automatically build and deploy your application
   - Wait for the build to complete (check the "Logs" tab)
   - Your app will be available at `https://<your-app-name>.onrender.com`
   - **Note**: The SQLite database file will persist on Render's filesystem

### Step 4: Update Auth0 Settings

1. **Add Production Callback URL**
   - Go to [Auth0 Dashboard](https://manage.auth0.com)
   - Navigate to your application settings
   - Add to "Allowed Callback URLs": `https://<your-app-name>.onrender.com/callback`
   - Add to "Allowed Logout URLs": `https://<your-app-name>.onrender.com/`
   - Add to "Allowed Web Origins": `https://<your-app-name>.onrender.com`
   - Click "Save Changes"

### Step 5: Test Your Deployment

1. Visit your Render URL: `https://<your-app-name>.onrender.com`
2. Click "Login" - should redirect to Auth0
3. Complete authentication
4. Verify you can create and manage todos

### Continuous Deployment

Once set up, Render automatically deploys when you push to your main branch:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```
3. Render detects the push and automatically rebuilds/redeploys
4. Monitor deployment progress in the Render dashboard

### Troubleshooting

- **Build Fails**: Check the "Logs" tab in Render dashboard for errors
- **Auth0 Redirect Error**: Verify callback URLs match exactly (including https://)
- **Environment Variables**: Ensure all required variables are set in Render
- **Database Issues**: Render free tier databases sleep after inactivity; first request may be slow

### Useful Links

- [Render Blueprint Documentation](https://render.com/docs/infrastructure-as-code)
- [Render Python Deployment Guide](https://render.com/docs/deploy-flask)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Auth0 Production Checklist](https://auth0.com/docs/deploy-monitor/deploy/production-checklist)

## Things we are ignoring

- Persistent records in a database. The current database will be destroyed each time you push to render,  ( we are only testing, not building a real system that works for years).
- Changing database structure SQLAlchemy Migrations. Currently we aren't handling changes to the database structure so you need to delete the local .db and start again (render wil do this anyway on a rebuild as mentioned above). They can be handled with Migrations
- Storing any user data in a database (other than an id from github ). To have users on this system to store any other PII refer to [https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy](https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy) and change the privacy statement.
- Adding extra security [https://flask-security.readthedocs.io/en/stable/quickstart.html#basic-flask-sqlalchemy-application](https://flask-security.readthedocs.io/en/stable/quickstart.html#basic-flask-sqlalchemy-application)
- Testing. There are no tests in this code.
