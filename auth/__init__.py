from .auth0 import auth0_bp, get_auth0_user
from .github import github_bp, get_github_user
import os
from flask import Blueprint, redirect, url_for, request

def is_codespaces():
    return os.getenv("CODESPACES") == "true" or os.getenv("CODESPACE_NAME") is not None

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    if is_codespaces():
        return redirect(url_for('auth0.login_auth0'))
    else:
        return redirect(url_for('github_auth.login_github'))

def get_current_user():
    from flask import session
    user = session.get("user")
    if user:
        return user
    user = get_github_user()
    if user:
        return user
    user = get_auth0_user()
    return user
