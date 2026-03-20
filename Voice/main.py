"""
Voice entry point
"""

import sys
import logging
from voice import config
from voice.health import run_startup_checks
from voice.app import VoiceApp

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT
)

logger = logging.getLogger(__name__)


def main():
    try:
        # Run startup checks (microphone, speaker, model paths, etc.)
        audio_io = run_startup_checks()
        
        # Initialize and run Voice code
        app = VoiceApp(audio_io)
        app.run()
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        print(f"\nStartup Error:\n   {e}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("User interrupted. Shutting down.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nUnexpected Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
