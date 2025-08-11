# ai_interview_lite_code/main.py

from facial_analysis import start_emotion_detection
from voice_transcriber import start_voice_analysis
from gui import launch_gui
import threading

if __name__ == '__main__':
    # Start emotion detection in a separate thread
    threading.Thread(target=start_emotion_detection, daemon=True).start()

    # Start voice analysis in a separate thread
    threading.Thread(target=start_voice_analysis, daemon=True).start()

    # Launch GUI to display feedback
    launch_gui()
