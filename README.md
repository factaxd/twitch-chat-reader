# Twitch Chat Reader with Twitch API & IRC

This project is focused on using **Twitch API** and **IRC** to create a system that processes Twitch chat messages, filters them based on certain criteria (such as keywords or specific users), and integrates with a custom user interface. The main functionality includes real-time chat monitoring, keyword-based actions, and user-specific message filtering.

## Features
- **Twitch IRC Connection**: Establishes a connection to Twitch's IRC chat system using OAuth authentication.
- **Real-time Chat Monitoring**: Listens for real-time chat messages from a Twitch channel.
- **Keyword Detection**: Detects specific keywords in chat messages (e.g., "abone", "donate") and performs corresponding actions such as changing message colors.
- **User Filtering**: Filters chat messages to only show messages from a selected user.
- **Tkinter UI Integration**: Displays chat messages in a user-friendly interface built with Tkinter, updating in real time.

## Prerequisites
Before setting up and running the project, ensure you have the following installed:

- Python 3.x
- `requests`, `websocket-client`, `tkinter`, `asyncio`
- A registered Twitch Developer application (for OAuth token)

### Twitch Developer Application Setup
1. Go to the [Twitch Developer Console](https://dev.twitch.tv/console/apps) and create a new application.
2. Set up the **OAuth Redirect URI** as `http://localhost:3000`.
3. Save your **Client ID** and **Client Secret** for later use.
