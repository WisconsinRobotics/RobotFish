"""
Centralized settings for audio, models, and service endpoints.
Paths are resolved relative to this module's location for portability.
"""

from pathlib import Path

# ============================================================================
# Paths - Resolved Relative to This Module
# ============================================================================

VOICE_ASSISTANT_DIR = Path(__file__).parent.parent  # Voice/ directory
VOICE_MODEL_DIR = VOICE_ASSISTANT_DIR

# Piper TTS model paths
PIPER_MODEL_PATH = VOICE_MODEL_DIR / "en_GB-northern_english_male-medium.onnx"
PIPER_CONFIG_PATH = VOICE_MODEL_DIR / "en_GB-northern_english_male-medium.onnx.json"

# ============================================================================
# Audio Configuration
# ============================================================================

# Input (microphone)
INPUT_FORMAT = 8  # pyaudio.paInt16 = 8
INPUT_CHANNELS = 1
INPUT_RATE = 16000
INPUT_CHUNK = 1024

# Output (speaker)
OUTPUT_FORMAT = 8  # pyaudio.paInt16 = 8
OUTPUT_CHANNELS = 1
OUTPUT_CHUNK = 1024

# ============================================================================
# Speech-to-Text (Whisper)
# ============================================================================

WHISPER_MODEL_NAME = "tiny"


OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "gemma3:1b" # TODO: I want to try qwen3.5 but am having issues downloading it

# System prompt for voice assistant personality
OLLAMA_SYSTEM_PROMPT = (
    "You are a fish named Finley. You primarily interact with children and love to share information about the sea!"
    "Keep responses brief, conversational, and under 100 words. Speak naturally as if having a casual conversation"
    "You are obsessed with tea and always talking about it."
)

# Conversation history management
MAX_HISTORY_LENGTH = 10  # Keep last N messages

# ============================================================================
# Text-to-Speech (Piper)
# ============================================================================

# Piper output sample rate
TTS_SAMPLE_RATE = 24000
TTS_SPEED = 1.0

# Text truncation for TTS safety
TTS_MAX_TEXT_LENGTH = 200

# ============================================================================
# Device & Stream Configuration
# ============================================================================

# Audio streaming buffer size
AUDIO_STREAM_CHUNK_SIZE = 1024

# Minimum recording duration for a valid input (seconds)
MIN_RECORDING_DURATION = 0.5

# ============================================================================
# Logging
# ============================================================================

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = "INFO"

# Button pin
BUTTON_PIN = 4
