# 🎨 Air Canvas — Gesture-Controlled Virtual Drawing

A real-time computer vision application that turns your webcam into an interactive mid-air drawing canvas. Powered by **OpenCV** and **Google MediaPipe**, Air Canvas tracks 21 3D hand landmarks in real time so you can draw, switch colors, and clear the screen without touching your mouse or keyboard.

---

## ✨ Features

- **Real-Time Hand Tracking:** Uses MediaPipe's `HandLandmarker` Tasks API for low-latency CPU tracking.
- **Gesture-Driven Modes:** Seamlessly switch between drawing, hovering, and menu selection using natural finger gestures.
- **Opaque Bitwise Compositing:** Overlays crisp, vibrant strokes directly onto the live webcam feed without washing out colors.
- **Auto Model Setup:** Automatically downloads the official `hand_landmarker.task` model on first launch.

---

## 🖐️ Gesture Controls

| Gesture | Mode | Action |
| :--- | :--- | :--- |
| ☝️ **Index Finger Up** *(middle finger down)* | **Draw** | Paints continuous strokes following your index fingertip. |
| ✌️ **Index + Middle Fingers Up** *(peace sign)* | **Hover & Select** | Lifts the brush to move freely; hover over the top bar to pick **BLUE**, **GREEN**, **RED**, or **CLEAR**. |
| ✊ **Closed Fist** *(index finger down)* | **Pause** | Lifts the pen and breaks stroke continuity so you can reposition your hand. |
| ⌨️ **`Q` Key** | **Quit** | Closes the application window safely. |

---

## 🛠️ Tech Stack

- **Python 3.9 – 3.12**
- **OpenCV (`opencv-python`)** — Webcam capture, UI rendering, and bitwise frame compositing
- **MediaPipe (`mediapipe`)** — 21-point hand landmark detection (`HandLandmarker`)
- **NumPy (`numpy`)** — Persistent canvas matrix operations

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/sreeragpp86/air-canvas.git](https://github.com/sreeragpp86/air-canvas.git)
cd air-canvas
