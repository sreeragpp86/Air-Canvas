import os
import urllib.request
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 1. Auto-download the official MediaPipe Hand Landmarker model if missing
MODEL_PATH = "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

if not os.path.exists(MODEL_PATH):
    print("Downloading hand_landmarker.task model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Download complete!")

# 2. Initialize HandLandmarker (Modern MediaPipe Tasks API)
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.6
)
detector = vision.HandLandmarker.create_from_options(options)

# Standard 21-point hand skeleton connections for drawing
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring
    (0, 17), (13, 17), (17, 18), (18, 19), (19, 20) # Pinky
]

# 3. Color Palette Setup (BGR format)
COLORS = [
    (255, 0, 0),    # Blue
    (0, 255, 0),    # Green
    (0, 0, 255),    # Red
    (0, 0, 0)       # Clear
]
COLOR_NAMES = ["BLUE", "GREEN", "RED", "CLEAR"]
draw_color = COLORS[0]
brush_thickness = 8

canvas = None
prev_x, prev_y = 0, 0

# 4. Start Webcam Capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros_like(frame)

    # Render top color menu bar
    button_w = w // len(COLORS)
    for i, name in enumerate(COLOR_NAMES):
        x1 = i * button_w
        x2 = (i + 1) * button_w
        cv2.rectangle(frame, (x1, 0), (x2, 80), COLORS[i], -1 if name != "CLEAR" else 2)
        text_color = (255, 255, 255) if name != "CLEAR" else (0, 0, 255)
        cv2.putText(frame, name, (x1 + 30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, text_color, 2)

    # Convert frame to MediaPipe Image & run detection
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
    results = detector.detect_for_video(mp_image, timestamp_ms)

    if results.hand_landmarks:
        for lm in results.hand_landmarks:
            ix, iy = int(lm[8].x * w), int(lm[8].y * h)

            index_up = lm[8].y < lm[6].y
            middle_up = lm[12].y < lm[10].y

            # Mode 1: SELECTION / HOVER (Index + Middle Up)
            if index_up and middle_up:
                prev_x, prev_y = 0, 0
                cv2.circle(frame, (ix, iy), 12, (255, 255, 255), cv2.FILLED)

                if iy < 80:
                    selected_idx = ix // button_w
                    if selected_idx < len(COLORS):
                        if COLOR_NAMES[selected_idx] == "CLEAR":
                            canvas = np.zeros_like(frame)
                        else:
                            draw_color = COLORS[selected_idx]

            # Mode 2: DRAWING (Index Up Only)
            elif index_up and not middle_up:
                cv2.circle(frame, (ix, iy), brush_thickness, draw_color, cv2.FILLED)

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = ix, iy

                cv2.line(canvas, (prev_x, prev_y), (ix, iy), draw_color, brush_thickness)
                prev_x, prev_y = ix, iy

            else:
                prev_x, prev_y = 0, 0

            # Draw hand skeleton overlay
            for start_idx, end_idx in HAND_CONNECTIONS:
                x1, y1 = int(lm[start_idx].x * w), int(lm[start_idx].y * h)
                x2, y2 = int(lm[end_idx].x * w), int(lm[end_idx].y * h)
                cv2.line(frame, (x1, y1), (x2, y2), (200, 200, 200), 2)
            for point in lm:
                px, py = int(point.x * w), int(point.y * h)
                cv2.circle(frame, (px, py), 4, (0, 255, 255), cv2.FILLED)

    # 5. Composite Canvas onto Webcam Feed
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_canvas, 10, 255, cv2.THRESH_BINARY)
    inv_mask = cv2.bitwise_not(mask)

    frame_bg = cv2.bitwise_and(frame, frame, mask=inv_mask)
    output = cv2.add(frame_bg, canvas)

    cv2.imshow("Air Canvas (Press 'Q' to Exit)", output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

detector.close()
cap.release()
cv2.destroyAllWindows()
