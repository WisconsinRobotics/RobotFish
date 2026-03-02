"""
Voice Assistant Package

Modules:
  - config: Central configuration and path resolution
  - audio_io: Microphone and speaker I/O abstraction
  - health: Startup device availability checks
  - stt_whisper: Speech-to-text using OpenAI Whisper
  - llm_ollama: LLM inference with message history using Ollama
  - tts_piper: Text-to-speech using Piper ONNX models
  - app: Main orchestration loop
"""

__version__ = "0.1.0"
