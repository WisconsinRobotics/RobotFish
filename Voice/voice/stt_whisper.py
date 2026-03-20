"""
Speech-to-Text using Whisper
==============================
Converts audio arrays to text using OpenAI's Whisper model.
"""

import logging
import torch
import whisper
from . import config

logger = logging.getLogger(__name__)


class WhisperSTT:
    """Speech-to-text using Whisper"""
    
    def __init__(self):
        """Load Whisper model"""
        logger.info(f"Loading Whisper {config.WHISPER_MODEL_NAME} model...")
        try:
            self.model = whisper.load_model(config.WHISPER_MODEL_NAME)
            logger.info("Whisper SST model loaded successfully.")
        except Exception as e:
            msg = f"Failed to load Whisper model: {e}"
            logger.error(msg)
            raise RuntimeError(msg) from e
    
    def transcribe(self, audio_data):
        """
        Convert audio array to text
        
        Args:
            audio_data: numpy array of audio samples (float32, normalized to [-1, 1])
            
        Returns:
            str: Transcribed text, or empty string if no speech detected
        """
        if audio_data is None or len(audio_data) == 0:
            logger.warning("Empty audio data passed to transcribe")
            return ""
        
        logger.info("Transcribing audio with Whisper...")
        
        try:
            result = self.model.transcribe(
                audio_data,
                language="en",
                fp16=torch.cuda.is_available()
            )
            
            text = result["text"].strip()
            
            if text:
                logger.info(f"Transcribed: '{text}'")
                return text
            else:
                logger.info("No speech detected in audio")
                return ""
                
        except Exception as e:
            msg = f"Transcription error: {e}"
            logger.error(msg)
            return ""
