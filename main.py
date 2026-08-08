import tkinter as tk
from tkinter import font
import random
import time

TEXTS = [
    "Typing speed tests help improve accuracy and focus.",
    "Anime inspired interfaces feel soft, calm and friendly.",
    "Python is a great language for building desktop apps.",
    "Practice makes perfect when learning to code."
]

def soft_button(parent, text, command):
    canvas = tk.Canvas(parent, width=160, height=45, bg="white", highlightthickness=0)

    def round_rect(x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1+r,
            x2, y2-r,
            x2-r, y2,
            x1+r, y2,
            x1, y2-r,
            x1, y1+r
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    round_rect(5, 5, 155, 40, 12, fill="#e8e1ff", outline="#e8e1ff")

    text_id = canvas.create_text(80, 22, text=text, fill="#5a4e88",
                                 font=("Noto Sans JP", 12, "bold"))

    def on_click(event):
        command()

    canvas.bind("<Button-1>", on_click)

    return canvas, text_id

def levenshtein(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # delete
                dp[i][j-1] + 1,      # insert
                dp[i-1][j-1] + cost  # replace
            )

    return dp[len(a)][len(b)]

class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Typing Speed Test")
        self.root.geometry("800x500")
        self.root.configure(bg="#fdfbff")

        # Fake gradient
        self.bg = tk.Frame(root, bg="#f7f4ff")
        self.bg.place(relwidth=1, relheight=1)

        # Fonts
        self.jp_font = font.Font(family="Noto Sans JP", size=12)
        self.title_font = font.Font(family="Noto Sans JP", size=22, weight="bold")

        # Shadow
        self.shadow = tk.Frame(root, bg="#e6e0ff")
        self.shadow.place(relx=0.5, rely=0.5, anchor="center", width=610, height=360)

        # Card
        self.card = tk.Frame(root, bg="white")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=600, height=350)

        self.title = tk.Label(self.card, text="Typing Speed Test", bg="white",
                              fg="#5a4e88", font=self.title_font)
        self.title.pack(pady=10)

        self.text_to_type = tk.Label(
            self.card,
            text=random.choice(TEXTS),
            wraplength=550,
            bg="white",
            fg="#6c6c6c",
            font=self.jp_font
        )
        self.text_to_type.pack(pady=10)

        self.entry = tk.Text(self.card, height=5, width=60, bd=0, bg="#faf7ff", fg="#5a4e88", insertbackground="#5a4e88", font=self.jp_font)
        self.entry.pack(pady=10)

        self.btn_canvas, self.btn_text_id = soft_button(self.card, "Start Test", self.start_test)
        self.btn_canvas.pack(pady=10)
        self.btn_enabled = True

        self.result = tk.Label(self.card, text="", bg="white", fg="#5a4e88", font=self.jp_font)
        self.result.pack()

        self.start_time = None

    def start_test(self):
        if not self.btn_enabled:
            return

        self.entry.delete("1.0", tk.END)
        self.result.config(text="")
        self.start_time = time.time()

        self.disable_button()
        self.countdown(10)

    def finish_test(self):
        typed = self.entry.get("1.0", tk.END).strip()
        original = self.text_to_type.cget("text")

        if not typed:
            self.result.config(text="Nada foi escrito 😅")
            return

        elapsed = time.time() - self.start_time
        words = len(typed.split())
        chars = len(typed)

        wpm = int(words / (elapsed / 60))
        cpm = int(chars / (elapsed / 60))

        dist = levenshtein(typed, original)
        max_len = max(len(typed), len(original))
        accuracy = int((1 - dist / max_len) * 100)

        self.result.config(
            text=f"WPM: {wpm}   |   CPM: {cpm}   |   Accuracy: {accuracy}%"
        )

    def disable_button(self):
        self.btn_enabled = False
        self.btn_canvas.unbind("<Button-1>")
        self.btn_canvas.itemconfig(self.btn_text_id, fill="#b3a8d6")  # cor mais clara

    def enable_button(self):
        self.btn_enabled = True
        self.btn_canvas.bind("<Button-1>", lambda e: self.start_test())
        self.btn_canvas.itemconfig(self.btn_text_id, fill="#5a4e88")  # cor normal

    def update_button_text(self, text):
        self.btn_canvas.itemconfig(self.btn_text_id, text=text)

    def countdown(self, remaining):
        self.update_button_text(f"{remaining}s")

        if remaining > 0:
            self.root.after(1000, lambda: self.countdown(remaining - 1))
        else:
            self.update_button_text("Start Test")
            self.enable_button()
            self.finish_test()

root = tk.Tk()
app = TypingApp(root)
root.mainloop()