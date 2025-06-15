# 🎯 Face Recognition Attendance System

An AI-powered attendance management system that uses facial recognition to automate check-in and check-out. Users can upload an image or use a real-time webcam feed to mark their presence. Attendance logs are saved in a CSV file with timestamps and status.

---

## 🚀 Features

- ✅ Upload a face image or use **webcam** for attendance
- 🧠 Uses **face recognition** for identity verification
- 📅 Automatically logs **check-in/check-out** based on time
- 📄 Saves records to `logs.csv` with name, time, and status
- 🌐 Simple, responsive web interface (HTML + Bootstrap)
- 🔒 Detects unknown faces gracefully

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3 (Bootstrap)
- **AI/ML**: `face_recognition`, `dlib`, `OpenCV`
- **Data Storage**: CSV (can be upgraded to DB)

---

## 🧰 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yuvanedvin/face-recognition-attendance.git
cd face-recognition-attendance
````

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, manually install:

```bash
pip install flask face_recognition opencv-python pandas
```

---

## 🖼️ Prepare Known Faces

* Create a folder named `known_faces/` inside the project directory.
* Add face images named after the person (e.g., `yuvan.jpg`, `vishnu.jpg`).
* These are used for identity matching.

---

## 💻 Run the App

```bash
python app.py
```

* Visit: [http://localhost:5000](http://localhost:5000)
* Upload an image or use the webcam to mark attendance.

---

## 📦 File Structure

```
├── app.py                # Main Flask server
├── templates/
│   └── index.html        # Frontend UI
├── known_faces/          # Folder with known face images
├── log.csv               # Attendance log file (auto-created)
└── static/               # for CSS/images
```

---

## 🧾 Attendance Format

Each entry in `log.csv`:

| Name  | Status    | Timestamp           |
| ----- | --------- | ------------------- |
| Yuvan | Check-in  | 2025-06-15 09:05 AM |
| Yuvan | Check-out | 2025-06-15 05:03 PM |

* Check-in/check-out logic is time-based.

---
