"""
Audio I/O Abstraction
Manages microphone input and speaker output streams, device discovery,
and audio data conversion.
"""

import logging
import pyaudio
from . import config

logger = logging.getLogger(__name__)

class AudioIO:
    """Manages PyAudio lifecycle, microphone input, and speaker output"""
    
    def __init__(self):
        """Initialize PyAudio and detect available devices"""
        logger.info("Initializing audio subsystem...")
        self.audio = pyaudio.PyAudio()
        self._pulse_device_index = self._find_pulse_device()
        logger.info(f"Audio subsystem initialized. Pulse device index: {self._pulse_device_index}")
    
    def _find_pulse_device(self):
        """Find PulseAudio device index, return None if not found"""
        for i in range(self.audio.get_device_count()):
            dev = self.audio.get_device_info_by_index(i)
            if 'pulse' in dev['name'].lower():
                logger.debug(f"Found PulseAudio device at index {i}: {dev['name']}")
                return i
        logger.warning("PulseAudio device not found; will use system default")
        return None
    
    def open_input_stream(self):
        """
        Open microphone input stream
        
        Returns:
            pyaudio.Stream: Input stream ready for reading
        """
        try:
            stream = self.audio.open(
                format=config.INPUT_FORMAT,
                channels=config.INPUT_CHANNELS,
                rate=config.INPUT_RATE,
                input=True,
                frames_per_buffer=config.INPUT_CHUNK,
                input_device_index=self._pulse_device_index
            )
            logger.debug("Opened microphone input stream")
            return stream
        except Exception as e:
            msg = f"Failed to open microphone input: {e}"
            logger.error(msg)
            raise Exception(msg) from e
    
    def open_output_stream(self, sample_rate=config.TTS_SAMPLE_RATE):
        """
        Open speaker output stream
        
        Args:
            sample_rate: Audio sample rate in Hz
            
        Returns:
            pyaudio.Stream: Output stream ready for writing
            
        Raises:
            Exception: If speaker cannot be opened
        """
        try:
            stream = self.audio.open(
                format=config.OUTPUT_FORMAT,
                channels=config.OUTPUT_CHANNELS,
                rate=int(sample_rate),
                output=True,
                frames_per_buffer=config.OUTPUT_CHUNK,
                output_device_index=self._pulse_device_index
            )
            logger.debug(f"Opened speaker output stream (sample_rate={sample_rate})")
            return stream
        except Exception as e:
            msg = f"Failed to open speaker output: {e}"
            logger.error(msg)
            raise Exception(msg) from e
    
    def test_input_stream(self):
        """
        Test if microphone input is available
        
        Raises:
            Exception: If microphone test fails
        """
        try:
            stream = self.open_input_stream()
            stream.close()
            logger.info("✓ Microphone test passed")
        except Exception as e:
            msg = f"Microphone test failed: {e}"
            logger.error(msg)
            raise Exception(msg) from e
    
    def test_output_stream(self):
        """
        Test if speaker output is available
        
        Raises:
            Exception: If speaker test fails
        """
        try:
            stream = self.open_output_stream()
            stream.close()
            logger.info("✓ Speaker test passed")
        except Exception as e:
            msg = f"Speaker test failed: {e}"
            logger.error(msg)
            raise Exception(msg) from e
    
    def shutdown(self):
        """Clean up PyAudio resources"""
        try:
            self.audio.terminate()
            logger.info("Audio subsystem shut down")
        except Exception as e:
            logger.error(f"Error during audio shutdown: {e}")
