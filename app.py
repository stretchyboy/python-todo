# Load environment variables from .env file (needed for gunicorn)
from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask
from auth import auth_bp, auth0_bp, github_bp, github_auth_bp
from auth import is_codespaces, is_render
from todo import todo_bp, init_app as init_todo 

SITE = {
    "WebsiteName": "TodoApp",
    "ControllerName": "UTC Sheffield Olympic Legacy Park",
    "ControllerAddress": "UTC Sheffield Olympic Legacy Park, 2 Old Hall Road"
    + ", Sheffield, S9 3TU",
    "ControllerURL": "https://www.utcsheffield.org.uk/olp/",
}

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "supersecret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'sqlite:///todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(auth0_bp)
app.register_blueprint(github_bp, url_prefix="/login")
app.register_blueprint(github_auth_bp)
app.register_blueprint(todo_bp)


@app.context_processor
def inject_dict_for_all_templates():
    auth_provider = "Auth0" if is_codespaces() or is_render() else "GitHub"
    return {"site": SITE, "auth_provider": auth_provider}


# Initialize todo module (db and tables)
init_todo(app)

# Set AUTH0_CALLBACK_URL dynamically based on Render's hostname
if 'RENDER_EXTERNAL_HOSTNAME' in os.environ:
    auth0_callback_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/callback"
else:
    auth0_callback_url = os.environ.get('AUTH0_CALLBACK_URL', 'http://localhost:5000/callback')

# Use auth0_callback_url in your Auth0 configuration

if __name__ == '__main__':
    app.run(debug=True)
