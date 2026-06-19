import tkinter as tk
from tkinter import scrolledtext
from groq import Groq
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


def ask_groq(user_input):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are ICHIGO, a helpful AI assistant. Keep answers short and clear."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI unavailable. Error: {e}"


def get_response(clean_input):
    responses = {
        "hello": "Hey there! I'm ICHIGO. How can I help?",
        "hi": "Hi! What's on your mind?",
        "hey": "Hey! Ask me anything.",
        "how are you": "I'm always fine — I'm a bot!",
        "who are you": "I'm ICHIGO — built by an AI intern at DecodeLabs.",
        "what is your name": "My name is ICHIGO!",
        "what can you do": "I can answer anything! Try me.",
        "what is ai": "AI is the simulation of human intelligence by machines.",
        "what is machine learning": "ML is a subset of AI where machines learn from data.",
        "what is deep learning": "Deep learning uses neural networks with many layers.",
        "what is a chatbot": "A chatbot is a program that simulates conversation with humans.",
        "what is decodelabs": "DecodeLabs is a tech company helping students build real AI projects.",
        "what is this project": "This is Project 1 — a Hybrid AI Chatbot built with Python.",
        "help": "Just type anything and I'll answer!",
        "thanks": "You're welcome! Keep building.",
        "bye": "Goodbye! Keep coding.",
    }

    if clean_input in responses:
        return responses[clean_input]

    for key in responses:
        if key in clean_input:
            return responses[key]

    return ask_groq(clean_input)


def send_message(event=None):
    user_text = entry.get().strip()
    if not user_text:
        return

    # Show user message
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"You: {user_text}\n", "user")
    entry.delete(0, tk.END)

    # Show typing indicator
    chat_box.insert(tk.END, "ICHIGO: typing...\n", "typing")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)
    window.update()

    # Get response
    clean_input = user_text.lower().strip()
    reply = get_response(clean_input)

    # Replace typing indicator with actual reply
    chat_box.config(state=tk.NORMAL)
    chat_box.delete("end-2l", "end-1l")
    chat_box.insert(tk.END, f"ICHIGO: {reply}\n\n", "bot")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)


# --- Window setup ---
window = tk.Tk()
window.title("ICHIGO — AI Chatbot")
window.geometry("600x650")
window.resizable(False, False)
window.configure(bg="#1a1a2e")

# --- Title bar ---
title = tk.Label(
    window,
    text="⚡ ICHIGO THE AI CHATBOT",
    font=("Helvetica", 16, "bold"),
    bg="#16213e",
    fg="#e94560",
    pady=12
)
title.pack(fill=tk.X)

# --- Chat display ---
chat_box = scrolledtext.ScrolledText(
    window,
    state=tk.DISABLED,
    wrap=tk.WORD,
    font=("Helvetica", 11),
    bg="#0f3460",
    fg="#ffffff",
    insertbackground="white",
    padx=10,
    pady=10,
    relief=tk.FLAT,
    height=30
)
chat_box.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

# Text color tags
chat_box.tag_config("user", foreground="#00d4ff", font=("Helvetica", 11, "bold"))
chat_box.tag_config("bot", foreground="#ffffff")
chat_box.tag_config("typing", foreground="#888888", font=("Helvetica", 10, "italic"))

# Welcome message
chat_box.config(state=tk.NORMAL)
chat_box.insert(tk.END, "ICHIGO: Hey! I'm ICHIGO. Ask me anything!\n\n", "bot")
chat_box.config(state=tk.DISABLED)

# --- Input area ---
input_frame = tk.Frame(window, bg="#1a1a2e")
input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

entry = tk.Entry(
    input_frame,
    font=("Helvetica", 12),
    bg="#16213e",
    fg="#ffffff",
    insertbackground="white",
    relief=tk.FLAT,
    bd=8
)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
entry.bind("<Return>", send_message)  # Enter key sends message
entry.focus()

send_btn = tk.Button(
    input_frame,
    text="Send",
    font=("Helvetica", 11, "bold"),
    bg="#e94560",
    fg="white",
    relief=tk.FLAT,
    padx=20,
    cursor="hand2",
    command=send_message
)
send_btn.pack(side=tk.RIGHT, padx=(8, 0), ipady=8)

window.mainloop()