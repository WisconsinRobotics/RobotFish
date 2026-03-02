"""
Health Checks
==============
Startup verification for device availability and model paths.
Raises descriptive exceptions early so failures are clear.
"""

import logging
from pathlib import Path
from . import config
from .audio_io import AudioIO, AudioIOError

logger = logging.getLogger(__name__)


class HealthCheckError(Exception):
    """Raised when a startup health check fails"""
    pass


def check_microphone(audio_io):
    """
    Verify microphone is available and working
    
    Args:
        audio_io: AudioIO instance
        
    Raises:
        HealthCheckError: If microphone test fails
    """
    try:
        audio_io.test_input_stream()
        logger.info("Microphone check passed")
    except AudioIOError as e:
        msg = f"Microphone unavailable: {e}"
        raise HealthCheckError(msg) from e


def check_speaker(audio_io):
    """
    Verify speaker is available and working
    
    Args:
        audio_io: AudioIO instance
        
    Raises:
        HealthCheckError: If speaker test fails
    """
    try:
        audio_io.test_output_stream()
        logger.info("Speaker check passed")
    except AudioIOError as e:
        msg = f"Speaker unavailable: {e}"
        raise HealthCheckError(msg) from e


def check_piper_models():
    """
    Verify Piper ONNX and config files exist
    
    Raises:
        HealthCheckError: If model files are missing
    """
    if not config.PIPER_MODEL_PATH.exists():
        msg = f"Piper model file not found: {config.PIPER_MODEL_PATH}"
        raise HealthCheckError(msg)
    
    if not config.PIPER_CONFIG_PATH.exists():
        msg = f"Piper config file not found: {config.PIPER_CONFIG_PATH}"
        raise HealthCheckError(msg)
    
    logger.info(f"✓ Piper models found at {config.PIPER_MODEL_DIR}")


def check_ollama_reachable():
    """
    Verify Ollama service is reachable (log only, don't fail startup)
    
    Ollama may not be running yet, so we warn but don't fail.
    The first actual request will fail with a clear error.
    """
    try:
        import requests
        response = requests.get(f"{config.OLLAMA_HOST}/api/tags", timeout=2)
        if response.status_code == 200:
            logger.info(f"✓ Ollama service reachable at {config.OLLAMA_HOST}")
        else:
            logger.warning(f"Ollama at {config.OLLAMA_HOST} returned status {response.status_code}")
    except Exception as e:
        logger.warning(
            f"Ollama service not reachable at {config.OLLAMA_HOST} (will retry on first use): {e}"
        )


def run_startup_checks():
    """
    Run all startup health checks
    
    Raises:
        HealthCheckError: If any critical check fails
        
    Returns:
        AudioIO: Initialized audio subsystem (confirmed working)
    """
    logger.info("=" * 60)
    logger.info("Running startup health checks...")
    logger.info("=" * 60)
    
    # Check model paths first (fast, no hardware needed)
    check_piper_models()
    
    # Initialize and test audio devices
    try:
        audio_io = AudioIO()
    except Exception as e:
        msg = f"Failed to initialize audio system: {e}"
        raise HealthCheckError(msg) from e
    
    check_microphone(audio_io)
    check_speaker(audio_io)
    
    # Ollama check is soft (log only)
    check_ollama_reachable()
    
    logger.info("=" * 60)
    logger.info("✓ All health checks passed!")
    logger.info("=" * 60)
    
    return audio_io
