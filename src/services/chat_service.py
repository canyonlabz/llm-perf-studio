from openai import OpenAI
import requests
import os
from src.utils.config import load_config
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client (optional)
api_key = os.getenv("OPENAI_API_KEY")
openai_available = bool(api_key)
if openai_available:
    client = OpenAI(api_key=api_key)
else:
    client = None

class ChatService:
    """Service for handling chat interactions with OpenAI or Ollama models.
    This service abstracts the chat functionality for both OpenAI and Ollama models,
    allowing for easy switching between them based on the configuration.
    It uses the OpenAI API for OpenAI models and a REST API for Ollama models.
    """
    def __init__(self):
        self.config = load_config()
        self.ollama_url = self.config['ollama']['ollama_api_url']
        self.ollama_model = self.config['ollama']['ollama_model']
        self.ollama_temp = self.config['ollama']['ollama_temperature']

    # Method to get a response from the chat model based on the provided messages and LLM mode.
    # It checks the LLM mode and calls the appropriate method for OpenAI or Ollama
    def get_response(self, messages, llm_mode):
        if llm_mode == "openai":
            return self._openai_chat(messages)
        else:
            return self._ollama_chat(messages)

    # Private methods to handle chat interactions with OpenAI and Ollama models.
    # These methods are not intended to be called directly outside this class.
    def _openai_chat(self, messages):
        # Check if OpenAI is available
        if not openai_available or client is None:
            return "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable or switch to Ollama mode."
        
        # Get AI response
        response = client.chat.completions.create(
            model=self.config['openai']['openai_model'],
            messages=messages,
            temperature=self.config['openai']['openai_temperature'],
        )
        response_content = response.choices[0].message.content
        return response_content

    # This method handles chat interactions with Ollama models using a REST API.
    # It constructs a payload with the model name, messages, and options, then sends a POST request to the Ollama API.
    # It returns the content of the response message.
    def _ollama_chat(self, messages):
        payload = {
            "model": self.ollama_model,
            "messages": messages,
            "options": {"temperature": self.ollama_temp},
            "stream": False
        }
        response = requests.post(
            f"{self.ollama_url}/api/chat",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()['message']['content']
