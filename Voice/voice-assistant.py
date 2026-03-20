#!/usr/bin/env python3
"""
Voice Entry Point
"""

import sys
import logging
from voice_assistant import config
from voice_assistant.health import HealthCheckError, run_startup_checks
from voice_assistant.app import AssistantApp

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT
)

logger = logging.getLogger(__name__)


def main():
    """Entry point: health checks → app initialization → main loop"""
    try:
        # Run startup checks (microphone, speaker, model paths, etc.)
        audio_io = run_startup_checks()
        
        # Initialize and run the assistant
        app = AssistantApp(audio_io)
        app.run()
        
    except HealthCheckError as e:
        logger.error(f"Startup failed: {e}")
        print(f"\nStartup Error:\n   {e}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("User interrupted; shutting down")
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nUnexpected Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
