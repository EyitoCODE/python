# ai_interview_lite_code/voice_transcriber.py

import speech_recognition as sr
from textblob import TextBlob
import time

voice_result = {
    "transcript": "",
    "sentiment": 0.0,
    "filler_count": 0
}

FILLERS = ["um", "uh", "like", "you know"]

def start_voice_analysis():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=10)

        try:
            text = recognizer.recognize_google(audio)
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
            filler_count = sum(text.lower().count(filler) for filler in FILLERS)

            voice_result['transcript'] = text
            voice_result['sentiment'] = sentiment
            voice_result['filler_count'] = filler_count

            print("Transcript:", text)
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            print("API unavailable")
            break

        time.sleep(1)

