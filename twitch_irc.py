import socket
import threading

class TwitchIRC:
    def __init__(self, token, username, channel, on_message_callback):
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.token = f"oauth:{token}"  # Token 'oauth:' ile başlatılmalı
        self.username = username
        self.channel = f"#{channel}"  # Kanal adı
        self.sock = socket.socket()
        self.on_message_callback = on_message_callback

    def connect(self):
        try:
            print(f"Connecting to Twitch IRC channel: {self.channel} ...")
            self.sock.connect((self.server, self.port))
            print("Connected!")
            self.sock.send(f"PASS {self.token}\n".encode('utf-8'))
            self.sock.send(f"NICK {self.username}\n".encode('utf-8'))
            self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))
            print(f"Joined channel {self.channel}")
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            print(f"Error connecting to IRC: {str(e)}")

    def receive_messages(self):
        try:
            print("Receiving messages...")
            while True:
                response = self.sock.recv(2048).decode('utf-8')
                if response.startswith('PING'):
                    self.sock.send("PONG\n".encode('utf-8'))
                else:
                    self.parse_message(response)
        except Exception as e:
            print(f"Error receiving messages: {str(e)}")

    def parse_message(self, response):
        if "PRIVMSG" in response:
            parts = response.split(":", 2)
            user_info = parts[1].split("!", 1)[0]
            message = parts[2].strip()
            print(f"Received message from {user_info}: {message}")
            self.on_message_callback(user_info, message)
