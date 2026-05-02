import tkinter as tk
from tkinter import scrolledtext
import threading
import sys
import adventure_game
from queue import Queue

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Adventure Game Menu")
        self.root.geometry("700x500")
        self.root.configure(bg="#1a001f")

        # Header Label
        header_font = ("Courier New", 36, "bold")
        header_label = tk.Label(root, text="ADVENTURE GAME", font=header_font,
                           fg="#c0da4f", bg="#1a001f")
        header_label.pack(pady=20)

        btn_font = ("Consolas", 12)

        # Start New Game Button
        self.start_btn = tk.Button(root, text="Start New Game", font=btn_font,
                  command=self.start_game, bg="#3b0a45", fg="#d8b4ff")
        self.start_btn.pack(pady=10)
        self.start_btn.bind("<Enter>", lambda e: self.on_hover(self.start_btn, True))
        self.start_btn.bind("<Leave>", lambda e: self.on_hover(self.start_btn, False))

        # Load Game Button
        self.load_btn = tk.Button(root, text="Load Game", font=btn_font,
                  command=self.load_game, bg="#3b0a45", fg="#d8b4ff")
        self.load_btn.pack(pady=10)
        self.load_btn.bind("<Enter>", lambda e: self.on_hover(self.load_btn, True))
        self.load_btn.bind("<Leave>", lambda e: self.on_hover(self.load_btn, False))

        # Exit Button
        self.exit_btn = tk.Button(root, text="Exit", font=btn_font,
                  command=root.quit, bg="#3b0a45", fg="#d8b4ff")
        self.exit_btn.pack(pady=10)
        self.exit_btn.bind("<Enter>", lambda e: self.on_hover(self.exit_btn, True))
        self.exit_btn.bind("<Leave>", lambda e: self.on_hover(self.exit_btn, False))

    def start_game(self):       
        self.open_game_window()
        threading.Thread(target=adventure_game.main, args=("new_game",), daemon=True).start()

    def load_game(self):
        self.open_game_window()
        threading.Thread(target=adventure_game.main, args=("load_game",), daemon=True).start()

    def open_game_window(self):
        game_window = tk.Toplevel(self.root)
        game_window.title("Adventure Game")
        game_window.geometry("1000x800")
        game_window.configure(bg="#120016")

        self.text_area = scrolledtext.ScrolledText(
            game_window,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#120016",
            fg="#9562c9",   # purple text
            insertbackground="white",
            state='disabled'
        )
        self.text_area.pack(expand=True, fill="both", padx=10, pady=5)
        self.text_area.tag_configure("user_input", foreground="#c0da4f")  # yellow for user input

        self.entry = tk.Entry(
            game_window,
            font=("Consolas", 12),
            bg="#1a001f",
            fg="#c0da4f",  # yellow text
            insertbackground="white"
        )
        self.entry.pack(fill="x", padx=5, pady=5)
        self.entry.bind("<Return>", self.send_input)

        # Redirect stdout to GUI
        sys.stdout = self
        self.entry.focus()

    def write(self, text):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')

    def flush(self):
        pass

    def send_input(self, event):
        user_input = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        # Echo input in GUI
        self.write(f"> {user_input}\n")

        # Send input back to program
        adventure_game.input_queue.put(user_input)

    def on_hover(self, button, is_hovering):
        if is_hovering:
            button.config(bg="#5a1a6e", fg="#ffff00")  # Darker purple, bright yellow
        else:
            button.config(bg="#3b0a45", fg="#d8b4ff")  # Original colors

if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()