from flask import Flask, render_template, request
import face_recognition
import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = 'log.csv'
KNOWN_DIR = 'known_faces'

# Load known face encodings
known_encodings = []
known_names = []

for filename in os.listdir(KNOWN_DIR):
    if filename.endswith(('.jpg', '.png')):
        path = os.path.join(KNOWN_DIR, filename)
        img = face_recognition.load_image_file(path)
        locations = face_recognition.face_locations(img)
        if locations:
            encoding = face_recognition.face_encodings(img, locations)[0]
            known_encodings.append(encoding)
            known_names.append(os.path.splitext(filename)[0])

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=['Name', 'Status', 'Time']).to_csv(LOG_FILE, index=False)

def log_attendance(name):
    df = pd.read_csv(LOG_FILE)
    now = datetime.now()
    status = "Check-In"

    today_entries = df[(df['Name'] == name) & (df['Time'].str.startswith(now.strftime('%Y-%m-%d')))]

    if not today_entries.empty and today_entries.iloc[-1]['Status'] == "Check-In":
        status = "Check-Out"

    df = pd.concat([df, pd.DataFrame([{
        'Name': name,
        'Status': status,
        'Time': now.strftime('%Y-%m-%d %H:%M:%S')
    }])])

    df.to_csv(LOG_FILE, index=False)
    return f"{name} {status} at {now.strftime('%H:%M:%S')}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            image = face_recognition.load_image_file(file)
            locations = face_recognition.face_locations(image)
            encodings = face_recognition.face_encodings(image, locations)

            for encoding in encodings:
                matches = face_recognition.compare_faces(known_encodings, encoding)
                face_distances = face_recognition.face_distance(known_encodings, encoding)

                if any(matches):
                    best_match_index = np.argmin(face_distances)
                    name = known_names[best_match_index]
                    result = log_attendance(name)
                    break
                else:
                    result = "Face not recognized."
        elif "realtime" in request.form:
            result = run_realtime_recognition()
    return render_template("index.html", result=result)

def run_realtime_recognition():
    cap = cv2.VideoCapture(0)
    name = "Unknown"
    result = "Face not recognized."

    while True:
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        for encoding in encodings:
            matches = face_recognition.compare_faces(known_encodings, encoding)
            face_distances = face_recognition.face_distance(known_encodings, encoding)

            if any(matches):
                best_match_index = np.argmin(face_distances)
                name = known_names[best_match_index]
                result = log_attendance(name)
                break
        cv2.imshow("Scan Face - Press Q", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return result

if __name__ == "__main__":
    app.run(debug=True)
