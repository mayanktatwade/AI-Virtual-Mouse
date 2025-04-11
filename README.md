# 🖱️ AI Virtual Mouse

A Python-based virtual mouse powered by **Computer Vision** and **Hand Gesture Recognition** using OpenCV, MediaPipe, and PyAutoGUI. This project enables users to control the mouse pointer and perform click/scroll operations using hand gestures captured via a webcam — no physical mouse needed!

---

## 📌 Features

- 🔍 Hand detection and tracking using a custom MediaPipe-based module
- 🖐️ Cursor control with index finger movement
- 👆✌️ Left click with pinch gesture (index + middle finger)
- 🔃 Scroll using gestures (YO! sign or pinky-only)
- ⚡ Smooth, real-time tracking with low latency
- 📊 FPS counter for performance monitoring

---

## 🧠 How It Works

| Gesture                     | Action         |
|----------------------------|----------------|
| Only Index Finger Up       | Move Mouse     |
| Index + Middle Finger Up   | Click (Pinch)  |
| Index + Pinky Up           | Scroll Down    |
| Only Pinky Up              | Scroll Up      |

The hand is tracked within a defined frame boundary. Gestures are recognized based on finger states and inter-finger distances.

---

## 🛠️ Requirements

- Python 3.6+
- OpenCV (`cv2`)
- NumPy
- PyAutoGUI
- MediaPipe (for `HandDetectionModule`)
- A webcam

Install dependencies:

```bash
pip install opencv-python numpy pyautogui mediapipe


