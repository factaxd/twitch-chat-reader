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

## How It Works

### 1. Twitch IRC Connection

The script uses **OAuth 2.0** for authentication to establish a connection with Twitch's IRC server. The `TwitchIRC` class handles the connection using the following steps:
- Send authentication details (OAuth token, username).
- Join the specified channel.
- Use the **PING-PONG** mechanism to keep the connection alive and prevent timeouts by responding to Twitch’s PING requests with PONG responses.

### 2. Chat Message Processing

- Once connected to the IRC server, the system continuously listens to real-time chat messages from the designated Twitch channel.
- Messages are processed asynchronously using **asyncio** to avoid blocking the GUI and ensure smooth performance.
- Specific keywords (like "abone" or "donate") are detected within chat messages, and based on these, the system dynamically changes the message's appearance (e.g., altering the color of the text).

### 3. Tkinter-based UI

The chat messages are displayed in a **Tkinter**-based graphical user interface (GUI). The key UI features include:
- A **Listbox** that displays incoming chat messages in real-time.
- A **user selection** feature allowing the user to filter messages and only display those from a specific chat participant.
- Keyword-based message highlighting, where detected keywords trigger style changes (e.g., changing the color or font of the messages).

### 4. Error Handling and Debugging

- **Authentication Errors**: Detects and handles OAuth token-related issues such as invalid tokens.
- **Timeout Errors**: Resolves connection timeout issues by using the PING-PONG mechanism to maintain a stable IRC connection.
- **Connection Drops**: Monitors the connection to ensure that dropped IRC connections are re-established automatically to maintain continuous message listening.

