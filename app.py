from flask import Flask, redirect, url_for, session, request
from requests_oauthlib import OAuth2Session
import os

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para sesiones

# Información del cliente de OAuth (GitHub)
CLIENT_ID = 'Ov23li1M7h1lURG3Cmum'         # Reemplaza con tu Client ID de GitHub
CLIENT_SECRET = '55cb810eef849459444448ae663c0264e020d8df' # Reemplaza con tu Client Secret de GitHub
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'
REDIRECT_URI = 'https://localhost:443/callback'  # La URL de redirección configurada en GitHub

@app.route("/")
def home():
    return "Bienvenido a la aplicación OAuth2. Visita /login para iniciar sesión con GitHub."

# Ruta para iniciar la autenticación
@app.route("/login")
def login():
    session.clear()  # Limpia la sesión antes de iniciar un nuevo flujo de autenticación
    github = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    authorization_url, state = github.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth_state'] = state
    return redirect(authorization_url)

# Ruta de callback para la autenticación
@app.route("/callback")
def callback():
    github = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=session.get('oauth_state'))
    token = github.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)
    session['oauth_token'] = token
    return redirect(url_for('.profile'))

# Ruta para mostrar la información del perfil del usuario
@app.route("/profile")
def profile():
    github = OAuth2Session(CLIENT_ID, token=session['oauth_token'])
    user_info = github.get('https://api.github.com/user').json()
    return f"Nombre de usuario: {user_info['login']}<br>URL de GitHub: {user_info['html_url']}"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))
