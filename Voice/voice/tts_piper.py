"""
Text-to-Speech using Piper
============================
Converts text to speech using Piper ONNX models with in-memory
synthesis and direct speaker streaming. Speech playback runs in
a background thread to avoid blocking the main loop.
"""

import logging
import re
import threading
import numpy as np
from piper.voice import PiperVoice
from . import config

logger = logging.getLogger(__name__)


class PiperTTS:
    """Text-to-speech using Piper ONNX models"""
    
    def __init__(self, audio_io):
        """
        Initialize Piper TTS
        
        Args:
            audio_io: AudioIO instance for speaker output
        """
        logger.info("Loading Piper TTS models...")
        try:
            self.tts = PiperVoice.load(
                str(config.PIPER_MODEL_PATH),
                str(config.PIPER_CONFIG_PATH)
            )
            logger.info("Piper TTS models loaded.")
        except Exception as e:
            msg = f"Failed to load Piper models: {e}"
            logger.error(msg)
            raise RuntimeError(msg) from e
        
        self.audio_io = audio_io
        self.is_speaking = False
    
    def _clean_text_for_tts(self, text):
        """
        Clean text for TTS by removing problematic characters
        
        Args:
            text: Input text
            
        Returns:
            str: Cleaned text safe for speech synthesis
        """
        if not text:
            return ""
        
        # Remove text between asterisks (like *smiles* or *laughs*)
        text = re.sub(r'\*[^*]*\*', '', text)
        
        # Remove standalone asterisks
        text = re.sub(r'\*', '', text)
        
        # Remove common emoji ranges
        text = re.sub(r'[\U0001F600-\U0001F64F]', '', text)  # emoticons
        text = re.sub(r'[\U0001F300-\U0001F5FF]', '', text)  # symbols & pictographs
        text = re.sub(r'[\U0001F680-\U0001F6FF]', '', text)  # transport & map
        text = re.sub(r'[\U0001F1E0-\U0001F1FF]', '', text)  # flags
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def speak(self, text):
        """
        Convert text to speech and stream to speakers
        
        Runs synthesis and playback in background thread to avoid blocking.
        Multiple calls will queue (previous call must finish before next starts).
        
        Args:
            text: Text to speak
        """
        if not text or self.is_speaking:
            return
        
        def speak_task():
            try:
                self.is_speaking = True
                logger.info("Generating and streaming speech...")
                
                # Clean text
                cleaned_text = self._clean_text_for_tts(text)
                
                if not cleaned_text.strip():
                    logger.warning("No speakable text after cleaning")
                    return
                
                # Truncate if too long
                if len(cleaned_text) > config.TTS_MAX_TEXT_LENGTH:
                    text_to_speak = cleaned_text[:config.TTS_MAX_TEXT_LENGTH].rsplit('.', 1)[0]
                    if text_to_speak:
                        text_to_speak += "."
                    else:
                        text_to_speak = cleaned_text[:config.TTS_MAX_TEXT_LENGTH]
                    logger.info(f"Text truncated: {len(cleaned_text)} → {len(text_to_speak)} chars")
                else:
                    text_to_speak = cleaned_text
                
                # Synthesize audio
                audio_chunks = self.tts.synthesize(text_to_speak)
                
                # Stream to speakers
                self._stream_to_speakers(audio_chunks)
                
            except Exception as e:
                logger.error(f"TTS error: {e}")
            finally:
                self.is_speaking = False
        
        # Run in background thread
        thread = threading.Thread(target=speak_task, daemon=True)
        thread.start()
    
    def _stream_to_speakers(self, audio_chunks):
        """
        Stream synthesized audio directly to speakers
        
        Args:
            audio_chunks: Iterable of audio chunk objects from Piper
        """
        try:
            stream = self.audio_io.open_output_stream(config.TTS_SAMPLE_RATE)
            
            for chunk in audio_chunks:
                audio_data = chunk.audio_float_array
                
                # Convert float to int16
                if audio_data.dtype != np.int16:
                    audio_data = (audio_data * 32767).astype(np.int16)
                
                # Write in chunks
                for i in range(0, len(audio_data), config.AUDIO_STREAM_CHUNK_SIZE):
                    chunk_data = audio_data[i:i + config.AUDIO_STREAM_CHUNK_SIZE]
                    stream.write(chunk_data.tobytes())
            
            stream.stop_stream()
            stream.close()
            logger.info("✓ Speech playback complete")
            
        except Exception as e:
            logger.error(f"Failed to stream audio to speakers: {e}")
        except Exception as e:
            logger.error(f"Audio streaming error: {e}")
