import os
from flask import Blueprint, session, redirect, render_template, url_for, request
from urllib.parse import urlencode
import requests

auth0_bp = Blueprint('auth0', __name__)

auth0_domain = os.getenv("AUTH0_DOMAIN")
auth0_client_id = os.getenv("AUTH0_CLIENT_ID")
auth0_client_secret = os.getenv("AUTH0_CLIENT_SECRET")
auth0_callback_url = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")
auth0_base_url = f"https://{auth0_domain}"
auth0_authorize_url = f"{auth0_base_url}/authorize"
auth0_token_url = f"{auth0_base_url}/oauth/token"
auth0_userinfo_url = f"{auth0_base_url}/userinfo"

def get_auth0_user():
    return session.get("user")

@auth0_bp.route('/login/auth0')
def login_auth0():
    params = {
        "audience": f"{auth0_base_url}/userinfo",
        "response_type": "code",
        "client_id": auth0_client_id,
        "redirect_uri": auth0_callback_url,
        "scope": "openid profile email"
    }
    return redirect(f"{auth0_authorize_url}?" + urlencode(params))

@auth0_bp.route('/callback/auth0')
def callback_auth0():
    code = request.args.get('code')
    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': auth0_client_id,
        'client_secret': auth0_client_secret,
        'code': code,
        'redirect_uri': auth0_callback_url
    }
    token_info = requests.post(auth0_token_url, json=token_payload).json()
    userinfo_response = requests.get(
        auth0_userinfo_url,
        headers={'Authorization': f"Bearer {token_info['access_token']}"}
    )
    userinfo = userinfo_response.json()
    session['user'] = {
        'id': userinfo['sub'],
        'name': userinfo.get('nickname', userinfo.get('name', '')),
        'email': userinfo.get('email', '')
    }
    return redirect('/')

@auth0_bp.route('/logout/auth0')
def logout_auth0():
    session.clear()
    params = {
        'returnTo': url_for('todo.home', _external=True),
        'client_id': auth0_client_id
    }
    return redirect(f"{auth0_base_url}/v2/logout?" + urlencode(params))
