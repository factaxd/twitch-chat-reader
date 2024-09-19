# main.py

import tkinter as tk
from gui import TwitchApp

def main():
    root = tk.Tk()
    app = TwitchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
