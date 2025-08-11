import tkinter as tk
from facial_analysis import emotion_result
from voice_transcriber import voice_result
import threading


def update_labels(emotion_label, transcript_label, sentiment_label, filler_label):
    while True:
        emotion_label.config(text=f"Emotion: {emotion_result['emotion']}")
        transcript_label.config(text=f"Transcript: {voice_result['transcript'][:50]}...")
        sentiment_label.config(text=f"Sentiment Score: {voice_result['sentiment']:.2f}")
        filler_label.config(text=f"Filler Words: {voice_result['filler_count']}")

        emotion_label.update()
        transcript_label.update()
        sentiment_label.update()
        filler_label.update()


def launch_gui():
    root = tk.Tk()
    root.title("AI Interview Feedback Lite")
    root.geometry("500x300")

    emotion_label = tk.Label(root, text="Emotion:", font=("Arial", 14))
    transcript_label = tk.Label(root, text="Transcript:", font=("Arial", 12), wraplength=450)
    sentiment_label = tk.Label(root, text="Sentiment:", font=("Arial", 12))
    filler_label = tk.Label(root, text="Filler Words:", font=("Arial", 12))

    emotion_label.pack(pady=10)
    transcript_label.pack(pady=10)
    sentiment_label.pack(pady=10)
    filler_label.pack(pady=10)

    threading.Thread(target=update_labels, args=(emotion_label, transcript_label, sentiment_label, filler_label), daemon=True).start()

    root.mainloop()
