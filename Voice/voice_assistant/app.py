"""
Main Voice Application
Main loop: record input --> transcribe --> generate response --> speak
"""

import logging
import time
import threading
import numpy as np
from . import config
from .audio_io import AudioIO, AudioIOError
from .stt_whisper import WhisperSTT
from .llm_ollama import OllamaChat
from .tts_piper import PiperTTS

logger = logging.getLogger(__name__)


class AssistantApp:
    """Main voice assistant application"""
    
    def __init__(self, audio_io):
        """
        Initialize the assistant with core services
        
        Args:
            audio_io: AudioIO instance (already tested in health checks)
        """
        logger.info("Initializing Voice Assistant App...")
        
        self.audio_io = audio_io
        self.stt = WhisperSTT()
        self.llm = OllamaChat()
        self.tts = PiperTTS(audio_io)
        
        logger.info("✓ Voice Assistant App initialized")
    
    def record_once(self):
        """
        Record audio until user presses ENTER
        
        Returns:
            numpy.ndarray: Audio samples (float32, normalized), or None if no audio
        """
        logger.info("Opening microphone stream for recording...")
        print("\nRecording... Press ENTER to stop (speak for at least 1 second)")
        
        try:
            stream = self.audio_io.open_input_stream()
        except AudioIOError as e:
            logger.error(f"Failed to open microphone: {e}")
            print(f"Error: {e}")
            return None
        
        frames = []
        recording = True
        start_time = time.time()
        
        def stop_recording():
            nonlocal recording
            input()  # Wait for Enter
            recording = False
        
        # Start thread to listen for Enter
        stop_thread = threading.Thread(target=stop_recording, daemon=True)
        stop_thread.start()
        
        # Record until Enter is pressed
        try:
            while recording:
                try:
                    data = stream.read(config.INPUT_CHUNK, exception_on_overflow=False)
                    frames.append(data)
                    
                    # Show progress every second
                    elapsed = time.time() - start_time
                    if int(elapsed) > int(elapsed - 0.1):
                        print(f"Recording: {elapsed:.1f}s", end='\r')
                except Exception as e:
                    logger.error(f"Recording error: {e}")
                    break
        finally:
            stream.stop_stream()
            stream.close()
        
        elapsed = time.time() - start_time
        print(f"\nRecording complete ({elapsed:.1f}s)")
        
        if not frames:
            logger.warning("No audio frames recorded")
            return None
        
        # Convert to numpy array (float32, normalized)
        audio_data = np.frombuffer(b''.join(frames), np.int16).astype(np.float32) / 32768.0
        
        if elapsed < config.MIN_RECORDING_DURATION:
            logger.warning(f"Recording too short ({elapsed:.1f}s < {config.MIN_RECORDING_DURATION}s)")
            print(f"Very short recording! Try speaking for longer next time.")
        
        return audio_data
    
    def process_turn(self):
        """
        Run one complete interaction: record → transcribe → chat → speak
        
        Returns:
            bool: True to continue, False to exit
        """
        audio_data = self.record_once()
        if audio_data is None:
            return True
        
        # Speech to text
        text = self.stt.transcribe(audio_data)
        if not text:
            logger.info("No speech transcribed; continuing...")
            return True
        
        # LLM response
        response = self.llm.chat(text)
        if not response:
            logger.warning("No response from LLM")
            return True
        
        # Text to speech
        self.tts.speak(response)
        
        return True
    
    def run(self):
        """
        Main event loop: prompt for commands or run a voice interaction
        """
        print("\n" + "=" * 60)
        print("Welcome to OnDevice Pi Voice Assistant!")
        print("=" * 60)
        print("Commands:")
        print("  Press ENTER to start recording (speak for at least 1 second)")
        print("  Type 'clear' to clear conversation history")
        print("  Type 'quit' or 'exit' to quit")
        print("=" * 60)
        
        try:
            while True:
                command = input("\nPress ENTER to record, or type a command: ").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    logger.info("User requested shutdown")
                    break
                
                elif command == 'clear':
                    self.llm.clear_history()
                
                elif command == '' or command == 'record':
                    # Run one complete turn
                    should_continue = self.process_turn()
                    if not should_continue:
                        break
                
                else:
                    print("Unknown command. Available: record (ENTER), clear, quit")
        
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
    
    def shutdown(self):
        """Clean shutdown of all services"""
        logger.info("Shutting down Voice Assistant...")
        try:
            self.audio_io.shutdown()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
        logger.info("Voice Assistant shut down complete")
