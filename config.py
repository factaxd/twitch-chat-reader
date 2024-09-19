class Config:
    CLIENT_ID = "your_twitch_client_id"
    CLIENT_SECRET = "your_twitch_client_secret"
    REDIRECT_URI = "http://localhost:3000"
    IRC_TOKEN = "oauth:your_oauth_token"  # Twitch Chat OAuth Token
    USERNAME = "your_twitch_username"
    CHANNEL = "your_twitch_channel"
    PORT = 3000
    SCOPE = ['user:read:email', 'chat:read']
