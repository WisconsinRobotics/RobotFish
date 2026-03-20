"""
Language Model Interface using Ollama
Chat interface with message history management and system prompt.
"""

import logging
import ollama
from . import config

logger = logging.getLogger(__name__)


class OllamaChat:
    """Chat interface with Ollama LLM, including conversation history"""
    
    def __init__(self):
        """Initialize Ollama client and conversation history"""
        logger.info(f"Initializing Ollama client (host={config.OLLAMA_HOST}, model={config.OLLAMA_MODEL})")
        self.client = ollama.Client(host=config.OLLAMA_HOST)
        self.conversation_history = []
        logger.info("Ollama client initialized.")
    
    def chat(self, user_message):
        """
        Send a message and get a response
        
        Args:
            user_message: str, the user's message
            
        Returns:
            str: Assistant response text
        """
        if not user_message:
            return ""
        
        logger.info(f"User: {user_message}")
        
        # Build system prompt
        system_prompt = {
            "role": "system",
            "content": config.OLLAMA_SYSTEM_PROMPT
        }
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Build message list: system + recent history
        messages = [system_prompt] + self.conversation_history[-config.MAX_HISTORY_LENGTH:]
        
        try:
            logger.info(f"Sending request to Ollama (model={config.OLLAMA_MODEL})...")
            response = self.client.chat(
                model=config.OLLAMA_MODEL,
                messages=messages
            )
            
            assistant_response = response['message']['content']
            
            # Add response to history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Trim history if too long
            if len(self.conversation_history) > config.MAX_HISTORY_LENGTH * 2:
                old_len = len(self.conversation_history)
                self.conversation_history = self.conversation_history[-config.MAX_HISTORY_LENGTH * 2:]
                logger.debug(f"Trimmed history: {old_len} → {len(self.conversation_history)} messages")
            
            logger.info(f"Assistant: {assistant_response}")
            return assistant_response
            
        except Exception as e:
            msg = f"Ollama error: {e}"
            logger.error(msg)
            error_msg = "Sorry, I encountered an error. Please try again."
            logger.info(f"Assistant: {error_msg}")
            return error_msg
    
    def clear_history(self):
        """Clear conversation history"""
        old_len = len(self.conversation_history)
        self.conversation_history = []
        logger.info(f"Conversation history cleared ({old_len} messages removed)")
