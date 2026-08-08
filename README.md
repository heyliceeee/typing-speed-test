# 🌸 Typing Speed Test

A lightweight desktop application built with **Python + Tkinter** that measures typing speed and accuracy.  
It features an **pastel interface**, rounded buttons, soft shadows, and an intelligent accuracy system powered by **Levenshtein distance**.

---

## ✨ Features

- Pastel anime‑style UI with *Noto Sans JP* typography  
- Random typing prompts  
- Rounded pastel “Start Test” button with countdown  
- Button disables during the test and resets afterward  
- Smart metrics:
  - **WPM** — Words Per Minute  
  - **CPM** — Characters Per Minute  
  - **Accuracy** using Levenshtein distance  
- Clean result display inside a centered card

---

## 🧠 Intelligent Accuracy (Levenshtein)

Accuracy is calculated using the Levenshtein distance between the typed text and the original prompt:

```
accuracy = (1 - dist / max_len) * 100
```

This method handles small mistakes gracefully, providing a fair and realistic score.
