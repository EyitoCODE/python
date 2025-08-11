
# ai_interview_lite_code/facial_analysis.py

import cv2
from deepface import DeepFace

emotion_result = {"emotion": "neutral"}

def start_emotion_detection():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dominant_emotion = result[0]['dominant_emotion']
            emotion_result['emotion'] = dominant_emotion
        except Exception:
            emotion_result['emotion'] = "neutral"

        cv2.imshow("Webcam Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

