#importing necessary libraries
import tkinter as tk  # For GUI
import pyttsx3        # For Text-to-Speech (TTS)
import speech_recognition as sr  # For Speech-to-Text (STT)
import json           # For loading responses

# Loading predefined responses from JSON
with open("data/diseases.json", "r") as file:
    responses = json.load(file)

# Initializing TTS engine
engine = pyttsx3.init()

def speak(text):
    """Function to speak out the bot response"""
    engine.say(text)
    engine.runAndWait()

def get_response(user_input):
    user_input = user_input.lower()
    # Try exact match first
    if user_input in responses:
        return responses[user_input]
    # Try substring match
    for key in responses:
        if key in user_input:
            return responses[key]
    return "Sorry, I don't have information about that."

def send_message():
    """Triggered when user clicks 'Send' or presses Enter"""
    user_input = entry.get().strip()
    if not user_input:
        return
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + user_input + "\n")
    entry.delete(0, tk.END)
    bot_response = get_response(user_input)
    chat_log.insert(tk.END, "Bot: " + bot_response + "\n")
    chat_log.config(state=tk.DISABLED)
    chat_log.see(tk.END)
    speak(bot_response)

def listen():
    """Triggered when user clicks the Mic button (Speech-to-Text)"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "Listening...\n")
        chat_log.config(state=tk.DISABLED)
        chat_log.see(tk.END)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            entry.delete(0, tk.END)
            entry.insert(0, text)
            # Show recognized speech as user input in chat area
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, "You: " + text + "\n")
            bot_response = get_response(text)
            chat_log.insert(tk.END, "Bot: " + bot_response + "\n")
            chat_log.config(state=tk.DISABLED)
            chat_log.see(tk.END)
            speak(bot_response)
        except sr.WaitTimeoutError:
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, "Mic timeout. Please try again.\n")
            chat_log.config(state=tk.DISABLED)
            chat_log.see(tk.END)
        except Exception:
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, "Sorry, I couldn't understand you.\n")
            chat_log.config(state=tk.DISABLED)
            chat_log.see(tk.END)

        # --- Beautiful GUI Setup ---
root = tk.Tk()
root.title("Health ChatBot - Medibot")
root.geometry("520x600")
root.configure(bg="#e6f2ff")  # Light blue background

# Header
header = tk.Label(root, text="🤖 Medibot - Your Health Assistant", bg="#3399ff", fg="white",
                  font=("Segoe UI", 18, "bold"), pady=12)
header.pack(fill=tk.X)

# Chat Frame
chat_frame = tk.Frame(root, bg="#e6f2ff", bd=2)
chat_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

# Chat display area
chat_log = tk.Text(chat_frame, bd=0, bg="#e6f2ff", fg="#333333",
                   font=("Segoe UI", 12), wrap=tk.WORD, state=tk.NORMAL)
chat_log.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
chat_log.insert(tk.END, "Bot: Hello! I am your personal Medibot. Feel free to ask me about any health issues.\n")
chat_log.config(state=tk.DISABLED)

# Entry Frame
entry_frame = tk.Frame(root, bg="#e6f2ff")
entry_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

# Text entry box
entry = tk.Entry(entry_frame, bd=1, font=("Segoe UI", 12), bg="white", fg="#333333", relief=tk.GROOVE)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=6)
entry.bind("<Return>", lambda event: send_message())

# Send Button
send_button = tk.Button(entry_frame, text="Send", command=send_message,
                        font=("Segoe UI", 11, "bold"), bg="#3399ff", fg="white", activebackground="#2673b8",
                        relief=tk.FLAT, padx=15, pady=6, cursor="hand2")
send_button.pack(side=tk.LEFT)

# Mic Button
mic_button = tk.Button(entry_frame, text="🎤", command=listen,
                       font=("Segoe UI", 11), bg="#f0ad4e", fg="white", activebackground="#d48806",
                       relief=tk.FLAT, padx=10, pady=6, cursor="hand2")
mic_button.pack(side=tk.LEFT, padx=(10, 0))

# Start the GUI event loop
root.mainloop()
