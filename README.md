# Talking Fish

Wisconsin Robotics Outreach 2025/2026

## Folder Structure

- Voice: AI voice assistant
- Camera: CV facial tracking
- MotorControl: Servo controls

## Package Manager

This project's dependencies are managed by uv. The pyproject.toml file contains the dependencies list.

- `uv run program.py`: Runs your program with up-to-date dependencies.
- `uv add`: Add a dependency to the entire project. (This updates pyproject.toml and runs `uv sync`.)
- `uv remove`: Remove a dependency from the entire project. (This updates pyproject.toml and runs `uv sync`.)
- `uv sync`: Updates your environment to match pyproject.toml.
- [Install uv](https://docs.astral.sh/uv/getting-started/installation/) for development on personal computer

## AI Voice Assistant

Run: `uv run Voice/pi-voice-assistant.py`

## Facial Tracking



## Servo Controls


