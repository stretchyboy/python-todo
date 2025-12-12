
import os
from flask import Flask
from auth import auth_bp, auth0_bp
from auth.github import github_bp, github_auth_bp
from todo import todo_bp, init_app as init_todo

def is_codespaces():
    return os.getenv("CODESPACES") == "true" or os.getenv("CODESPACE_NAME") is not None

SITE = {
    "WebsiteName": "TodoApp",
    "ControllerName": "UTC Sheffield Olympic Legacy Park",
    "ControllerAddress": "UTC Sheffield Olympic Legacy Park, 2 Old Hall Road, Sheffield, S9 3TU",
    "ControllerURL": "https://www.utcsheffield.org.uk/olp/",
}

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "supersecret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(auth0_bp)
app.register_blueprint(github_bp)
app.register_blueprint(github_auth_bp)
app.register_blueprint(todo_bp)

@app.context_processor
def inject_dict_for_all_templates():
    auth_provider = "Auth0" if is_codespaces() else "GitHub"
    return {"site": SITE, "auth_provider": auth_provider}

# Initialize todo module (db and tables)
init_todo(app)

if __name__ == '__main__':
    app.run(debug=True)
