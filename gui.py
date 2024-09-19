import tkinter as tk
from tkinter import messagebox
from twitch_api import TwitchAPI
from twitch_irc import TwitchIRC
from config import Config
import webbrowser

class TwitchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitch Chat Reader")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")  # Arka plan rengini hafif gri yapalım

        self.selected_user = None

        # Kanal Label (Twitch Username)
        self.channel_label = tk.Label(root, text="Channel: Not connected", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333")
        self.channel_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="w", padx=20)

        # Kullanıcı Listesi (Genişlik daraltıldı)
        self.user_listbox = tk.Listbox(root, font=("Arial", 12), width=20, height=20)
        self.user_listbox.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        # Kullanıcı Seçimi için Buton
        self.select_user_button = tk.Button(root, text="Select User", command=self.on_user_select, font=("Arial", 12))
        self.select_user_button.grid(row=2, column=0, padx=20, pady=10, sticky="n")

        # Sohbet Mesajları (Geniş bırakıldı)
        self.chat_text = tk.Text(root, font=("Arial", 12), height=20, width=55, state=tk.DISABLED, wrap=tk.WORD)
        self.chat_text.grid(row=1, column=1, rowspan=2, padx=20, pady=10, sticky="nsew")

        # Twitch'e Bağlan Butonu (Küçültüldü ve modern tasarım)
        self.connect_button = tk.Button(root, text="Connect to Twitch", command=self.connect_to_twitch, font=("Arial", 12, "bold"), width=14, height=2, bg="#7F00FF", fg="white", bd=0, activebackground="#1aa34a", cursor="hand2")
        self.connect_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Grid ayarları
        self.root.grid_columnconfigure(1, weight=1)  # Sohbet mesajları için genişletilebilir kolon
        self.root.grid_rowconfigure(1, weight=1)  # Sohbet mesajları için genişletilebilir satır

        self.irc = None
        self.api = TwitchAPI()

    def connect_to_twitch(self):
        try:
            auth_url = self.api.get_authorization_url()
            webbrowser.open(auth_url)
            messagebox.showinfo("Authorization", "Please authorize the app in the opened browser window.")
            auth_code = self.api.start_local_http_server()
            if not auth_code:
                messagebox.showerror("Error", "Failed to retrieve authorization code.")
                return

            self.api.get_token(auth_code)
            messagebox.showinfo("Success", "Successfully obtained access token.")

            user_info = self.api.get_user_info()
            username = user_info.get('login')
            display_name = user_info.get('display_name')
            user_id = user_info.get('id')

            messagebox.showinfo("User Info", f"Connected as: {display_name} (ID: {user_id})")

            # Kanal adını belirleyelim
            channel = username
            print(f"Using channel: {channel}")
            self.channel_label.config(text=f"Channel: #{channel}", fg="#1db954")  # Kanal adı yeşil renkte gösterilsin

            # IRC'ye bağlan ve chat mesajlarını al
            self.connect_to_twitch_chat(username, channel)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def connect_to_twitch_chat(self, username, channel):
        try:
            self.irc = TwitchIRC(
                token=self.api.token['access_token'],
                username=username,
                channel=channel,
                on_message_callback=self.display_chat_message
            )
            self.irc.connect()
            messagebox.showinfo("Success", f"Connected to Twitch Chat on channel #{channel}!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_chat_message(self, user_info, message):
        if self.selected_user and user_info != self.selected_user:
            return

        self.chat_text.config(state=tk.NORMAL)

        if "abone" in message.lower():
            self.chat_text.tag_config("abone", foreground="red")
            self.chat_text.insert(tk.END, f"{user_info}: {message}\n", "abone")
        elif "donate" in message.lower():
            self.chat_text.tag_config("donate", foreground="blue")
            self.chat_text.insert(tk.END, f"{user_info}: {message}\n", "donate")
        elif "bit" in message.lower():
            self.chat_text.tag_config("bit", foreground="purple")
            self.chat_text.insert(tk.END, f"{user_info}: {message}\n", "bit")
        else:
            self.chat_text.insert(tk.END, f"{user_info}: {message}\n")

        if user_info not in self.user_listbox.get(0, tk.END):
            self.user_listbox.insert(tk.END, user_info)

        self.chat_text.yview(tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def on_user_select(self):
        selection = self.user_listbox.curselection()
        if selection:
            self.selected_user = self.user_listbox.get(selection[0])
            messagebox.showinfo("User Selected", f"Now showing messages only from: {self.selected_user}")
        else:
            self.selected_user = None

if __name__ == "__main__":
    root = tk.Tk()
    app = TwitchApp(root)
    root.mainloop()
