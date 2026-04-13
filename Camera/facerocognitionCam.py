import cv2
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from MotorControl.CameraMovement import camera_adjust

def _display_available() -> bool:
    """
    Check if a display is available for OpenCV windows.
    Returns False in headless environments.
    """
    if sys.platform.startswith("linux"):
        return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    return True

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
profile_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_profileface.xml"
)
tracker = None
tracking = False
last_detect_time = 0
detect_interval = 0.5
display_available = _display_available()

# Positive values move the target center right, negative move it left.
CENTER_X_OFFSET_PX = 20 # TODO: TEST START HERE ALISON

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if display_available:
        try:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        except cv2.error:
            # Headless mode (Display failed)
            display_available = False

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
        frontal_faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor = 1.1, 
            minNeighbors = 5, 
            minSize=(60, 60)
        )

        left_profiles = profile_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
        )

        # Detect right-facing profiles by mirroring the image.
        gray_flipped = cv2.flip(gray, 1)
        right_profiles_flipped = profile_cascade.detectMultiScale(
            gray_flipped,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
        )
        right_profiles = [
            (gray.shape[1] - x - w, y, w, h)
            for (x, y, w, h) in right_profiles_flipped
        ]

        all_faces = list(frontal_faces) + list(left_profiles) + right_profiles
        if len(all_faces) > 0:
            x, y, w, h = max(all_faces, key=lambda b: b[2] * b[3])
            face_center_x = x + (w // 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "face_detecting", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, (x, y, w, h))
            tracking = True
        else: 
            cv2.putText(frame, "No face detected yet . . .", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    target_x = (frame.shape[1] / 2.0) + CENTER_X_OFFSET_PX

    servo_value = camera_adjust(
        face_center_x,
        frame.shape[1],
        target_x=target_x,
    )
    cv2.putText(
        frame,
        f"servo={servo_value:.2f} center_offset={CENTER_X_OFFSET_PX}px",
        (10, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2,
    )

    if display_available:
        try:
            cv2.imshow("Face recognition tracking~", frame)
        except cv2.error:
            # Disable preview if imshow fails, but keep control loop running.
            display_available = False

# Destroy resources after loop exits
cap.release()
if display_available:
    cv2.destroyAllWindows()
