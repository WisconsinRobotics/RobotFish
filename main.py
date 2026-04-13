"""
To start the entire system, run this file: `uv run main.py`.

To stop the system, run `ps` and then `kill <pid>` for the uv process.
"""

import subprocess

# Initialize Voice
voice_process = subprocess.Popen(["uv", "run", "Voice/main.py"])
# TODO: Initially tell Finley "Introduce yourself." to speed up the first response.

# Initialize facial tracking
facial_tracking_process = subprocess.Popen(["uv", "run", "Camera/facerocognitionCam.py"])
