"""
Health Checks
==============
Startup verification for device availability and model paths.
Raises descriptive exceptions early so failures are clear.

TODO: This should replace SpeakerTests/*, so delete that once this is complete.
"""

import logging
from . import config
from .audio_io import AudioIO

logger = logging.getLogger(__name__)

def check_piper_models():
    """
    Verify Piper ONNX and config files exist
    """
    if not config.PIPER_MODEL_PATH.exists():
        msg = f"Piper model file not found: {config.PIPER_MODEL_PATH}"
        raise Exception(msg)
    
    if not config.PIPER_CONFIG_PATH.exists():
        msg = f"Piper config file not found: {config.PIPER_CONFIG_PATH}"
        raise Exception(msg)
    
    logger.info(f"✓ Piper models found at {config.PIPER_MODEL_PATH}")

def check_microphone(audio_io):
    """
    Verify microphone is available and working
    
    Args:
        audio_io: AudioIO instance
    """
    try:
        audio_io.test_input_stream()
        logger.info("Microphone check passed")
    except Exception as e:
        msg = f"Microphone unavailable: {e}"
        raise Exception(msg) from e

def check_speaker(audio_io):
    """
    Verify speaker is available and working
    
    Args:
        audio_io: AudioIO instance
    """
    try:
        audio_io.test_output_stream()
        logger.info("Speaker check passed")
    except Exception as e:
        msg = f"Speaker unavailable: {e}"
        raise Exception(msg) from e

def check_ollama_reachable():
    """
    Check if Ollama service is reachable. This will not throw an error.
    """
    try:
        import requests
        response = requests.get(f"{config.OLLAMA_HOST}/api/tags", timeout=2)
        if response.status_code == 200:
            logger.info(f"Ollama service reachable at {config.OLLAMA_HOST}")
        else:
            logger.warning(f"Ollama at {config.OLLAMA_HOST} returned status {response.status_code}")
    except Exception as e:
        logger.warning(
            f"Ollama service not reachable at {config.OLLAMA_HOST} (will retry on first use): {e}"
        )

def run_startup_checks():
    """
    Run all startup health checks
            
    Returns:
        AudioIO: Initialized audio subsystem (confirmed working)
    """
    # Check that model files exist
    check_piper_models()
    
    # Initialize and test audio devices
    try:
        audio_io = AudioIO()
    except Exception as e:
        msg = f"Failed to initialize audio system: {e}"
        raise Exception(msg) from e
    
    check_microphone(audio_io)
    check_speaker(audio_io)
    
    # Ollama check
    check_ollama_reachable()
    
    logger.info("Verified that models and audio devices are available.")
    
    return audio_io
