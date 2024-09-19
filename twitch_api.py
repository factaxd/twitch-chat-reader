# twitch_api.py

import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from requests_oauthlib import OAuth2Session
from config import Config
import requests

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.auth_code = None
        if '/?code=' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authorization successful! You can close this window.</h1></body></html>")
            # URL'den authorization code'u çıkar
            self.server.auth_code = self.path.split('code=')[1].split('&')[0]
        else:
            self.send_response(404)
            self.end_headers()

class TwitchAPI:
    def __init__(self):
        self.oauth = OAuth2Session(Config.CLIENT_ID, redirect_uri=Config.REDIRECT_URI, scope=Config.SCOPE)
        self.token = None

    def get_authorization_url(self):
        authorization_url, state = self.oauth.authorization_url('https://id.twitch.tv/oauth2/authorize')
        return authorization_url

    def start_local_http_server(self):
        server_address = ('', Config.PORT)
        httpd = HTTPServer(server_address, OAuthHandler)
        thread = Thread(target=httpd.handle_request)
        thread.start()
        thread.join()
        return httpd.auth_code

    def get_token(self, authorization_code):
        token_url = 'https://id.twitch.tv/oauth2/token'
        token_params = {
            'client_id': Config.CLIENT_ID,
            'client_secret': Config.CLIENT_SECRET,
            'code': authorization_code,
            'grant_type': 'authorization_code',
            'redirect_uri': Config.REDIRECT_URI
        }
        response = requests.post(token_url, data=token_params)
        if response.status_code == 200:
            self.token = response.json()
            return self.token
        else:
            raise Exception(f"Failed to obtain token: {response.text}")

    def get_user_info(self):
        if not self.token:
            raise Exception("Token not available.")
        headers = {
            'Authorization': f"Bearer {self.token['access_token']}",
            'Client-ID': Config.CLIENT_ID
        }
        response = requests.get('https://api.twitch.tv/helix/users', headers=headers)
        if response.status_code == 200:
            return response.json()['data'][0]
        else:
            raise Exception(f"Failed to fetch user info: {response.text}")
