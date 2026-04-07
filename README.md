# Talking Fish

Wisconsin Robotics Outreach 2025/2026

## Folder Structure

- Voice: AI voice assistant
- Camera: CV facial tracking
- MotorControl: Servo controls

## Package Manager

This project's dependencies are managed by uv. The pyproject.toml file contains the dependencies list, and descriptions of basic commands can be found [here](https://docs.astral.sh/uv/getting-started/features/#projects).

- `uv run program.py`: Runs your program with up-to-date dependencies.
- `uv add`: Add a dependency to the entire project. (This updates pyproject.toml and runs `uv sync`.)
- `uv remove`: Remove a dependency from the entire project. (This updates pyproject.toml and runs `uv sync`.)
- `uv sync`: Updates your environment to match pyproject.toml.
- [Install uv](https://docs.astral.sh/uv/getting-started/installation/) for development on personal computer

## AI Voice Response

1. Turn on the Bluetooth speaker. It should automatically connect to the Pi.

2. Run: `uv run Voice/main.py`

### File Organization

Voice/  
├── main.py
├── voice/  
│   ├── config.py           *(For constants, settings, and Finley's prompt)*  
│   ├── audio_io.py         *(Microphone & speaker I/O)*  
│   ├── health.py           *(Startup device checks)*  
│   ├── stt_whisper.py      *(Speech to text)*  
│   ├── llm_ollama.py       *(LLM response generation)*  
│   ├── tts_piper.py        *(Text to speech with streaming)*  
│   └── app.py              *(Main loop)*  
├── en_GB-northern_english_male-medium.onnx         *(TTS voice model)*  
└── en_GB-northern_english_male-medium.onnx.json    *(TTS voice model)*  

### To Do

- Add activation trigger (Speak "Hey Finley" or press a button)
- Decrease Time To First Token (Start speech to text before LLM generation is completed, switch to a faster (smaller) LLM, test the AI HAT we ordered)
    - [PiperTTS source code](https://github.com/OHF-Voice/piper1-gpl)
- Give Finley a personality!!!! 🐟🐟🐟
    - Edit his prompt in `Voice/voice/config.py`.
    - Allow mechanical responses? (e.g., Finley says "--shake_head--" and robot shakes its head.)

## Camera & CV Face Tracking



## Servo Controls

Run head servo: See Camera section
Run mouth servo: UNIMPLEMENTED
