import cv2
import os
import sys
import time
from pathlib import Path

# Allow direct execution (e.g., `uv run Camera/facerocognitionCam.py`) to import sibling folders.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from MotorControl.CameraMovement import camera_adjust

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
tracker = None
tracking = False
last_detect_time = 0
detect_interval = 0.5


def _display_available() -> bool:
    if sys.platform.startswith("linux"):
        return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    return True


show_preview = _display_available()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if show_preview:
        try:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        except cv2.error:
            # Fall back to headless mode if GUI support is unavailable at runtime.
            show_preview = False

    face_center_x = -1

    if tracking and tracker is not None:
        success, box = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            face_center_x = x + (w // 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "face detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else :
            tracking = False
            tracker = None

    if not tracking and (time.time() - last_detect_time) >= detect_interval:
        last_detect_time = time.time()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor = 1.1, 
            minNeighbors = 5, 
            minSize=(60, 60)
        )
        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda b: b[2] * b[3])
            face_center_x = x + (w // 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "face_detecting", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, (x, y, w, h))
            tracking = True
        else: 
            cv2.putText(frame, "No face detected yet . . .", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    servo_value = camera_adjust(face_center_x, frame.shape[1])
    cv2.putText(
        frame,
        f"servo={servo_value:.2f}",
        (10, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2,
    )

    if show_preview:
        try:
            cv2.imshow("Face recognition tracking~", frame)
        except cv2.error:
            # Disable preview if imshow fails, but keep control loop running.
            show_preview = False

cap.release()
if show_preview:
    cv2.destroyAllWindows()