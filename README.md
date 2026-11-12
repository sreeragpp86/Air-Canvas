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

2. Create a Virtual Environment & Install Dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install opencv-python mediapipe numpy

3. Run the Application
python aircanvas.py

Note (macOS Users): On the first run, macOS will ask for Camera permissions for your terminal or IDE. Click Allow (or enable it under System Settings → Privacy & Security → Camera) and run the script again.
🧠 How It Works
Landmark Extraction: MediaPipe detects 21 hand landmarks per frame. By comparing fingertip y-coordinates against their middle joints (landmark[8] vs. landmark[6] for the index finger, and landmark[12] vs. landmark[10] for the middle finger), the app determines which fingers are extended.
Persistent Canvas Buffer: Strokes are drawn onto a separate black NumPy array matching the webcam resolution rather than directly onto the video frames.
Bitwise Masking: Each frame converts the canvas into a binary mask (cv2.threshold), blacks out the drawn pixels on the live camera feed (cv2.bitwise_and), and merges the colored strokes on top (cv2.add).
🔮 Future Improvements
[ ] Dynamic brush size control using thumb-to-index pinch distance
[ ] Stroke smoothing (exponential moving average) to reduce webcam jitter
[ ] Export artwork as a transparent .png file via gesture or hotkey
[ ] Eraser tool and custom color palette
📄 License
This project is open-source and available under the MIT License.
