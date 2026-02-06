<<<<<<< HEAD
=======
# Wisconsin Robotics Talking Fish

## Folder structure

- Camera: Facial tracking
- MotorControl: Servo controls
- Voice: AI voice assistant


>>>>>>> Sem2-catchup
# 🥧🎙️ OnDevice Pi Voice Assistant

A lightweight, privacy-focused voice assistant that runs entirely offline on your Raspberry Pi 4. Built with OpenAI's Whisper for speech recognition, Ollama for intelligent responses, and KittenTTS for natural-sounding speech synthesis - everything processed locally on your device.

## ✨ Features

- 🏠 **100% On-Device Processing** - No cloud, no internet required after setup
- 🔊 **Real-time Speech Recognition** - Powered by OpenAI Whisper Tiny (39MB)
- 🥧 **Raspberry Pi Optimized** - Designed specifically for Pi 4 performance
- 🧠 **Local AI Responses** - Uses Ollama with ultra-lightweight gemma3:270m model
- 🗣️ **Neural Text-to-Speech** - KittenTTS for natural-sounding voice (25MB)
- 🔒 **Privacy First** - Your conversations never leave your device
- ⚡ **Low Resource Usage** - Runs smoothly on Pi 4 with 4GB RAM
- 🎛️ **Simple CLI Interface** - Easy to use command-line operation
- 🔄 **Conversation Memory** - Maintains context across interactions
- 🎵 **Multiple Voices** - 8 different TTS voice options

## 🚀 Quick Start

### Prerequisites

- **Raspberry Pi 4** (4GB+ RAM recommended)
- Python 3.8+
- Microphone and speakers/headphones
- [Ollama](https://ollama.ai/) installed and running
- MicroSD card (32GB+ recommended)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/dwain-barnes/ondevice-pi-voice-assistant.git
cd ondevice-pi-voice-assistant
```
# Create venv
python -m venv ondevice-voice-env

# Or with specific Python version
python3 -m venv ondevice-voice-env

# Command Prompt
ondevice-voice-env\Scripts\activate

# PowerShell
ondevice-voice-env\Scripts\Activate.ps1

# Git Bash
source ondevice-voice-env/Scripts/activate

# Linux/Mac/Pi
source ondevice-voice-env/bin/activate

2. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl
sudo apt-get install portaudio19-dev
curl -fsSL https://ollama.com/install.sh | sh
```

3. **Setup Ollama (if not already installed):**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the lightweight model (perfect for Pi 4)
ollama run gemma3:270m
```

4. **Run the assistant:**
```bash
python pi-voice-assistant.py
```

> **💡 Pro tip:** The first time you run it, Ollama will automatically download the gemma3:270m model (~270MB). This happens once and then everything runs locally!

## 🎯 Usage

Once running, you can:

- **Press ENTER** to start recording your voice
- **Press ENTER again** to stop recording and get a response
- **Type commands:**
  - `voice` - Change TTS voice (8 options)
  - `clear` - Clear conversation history
  - `quit` - Exit the assistant

### Example Interaction

```
🎤 Recording... Press ENTER to stop
🛑 Recording stopped (3.2s recorded)
🗣️ Converting speech to text with Whisper...
You said: What's the weather like today?

🤖 Thinking...
Pi Assistant: I don't have access to real-time weather data since I'm running locally, 
but I'd be happy to help you find weather information or discuss other topics!

🔊 Generating speech...
🔊 Playing speech...
```

## 📋 Requirements

### Software Dependencies
- `openai-whisper` - Speech recognition
- `torch` - Neural network framework
- `ollama` - Local LLM client
- `kittentts` - Text-to-speech synthesis
- `pyaudio` - Audio I/O
- `soundfile` - Audio file handling
- `numpy` - Numerical operations

### Hardware Requirements

**Minimum (Raspberry Pi 4):**
- 4GB RAM
- MicroSD card (32GB+)
- USB microphone
- Audio output (speakers/headphones)

**Recommended:**
- 8GB RAM for smoother performance
- Fast MicroSD card (Class 10/U3)
- Quality USB microphone for better recognition

## 🔧 Configuration

Edit the configuration in `pi-voice-assistant.py`:

```python
# Ollama settings
self.ollama_host = "http://localhost:11434"
self.ollama_model = "gemma3:270m"  # Lightweight model perfect for Pi 4

# Whisper settings  
self.whisper_model = "tiny"   # Options: tiny, base, small, medium, large

# TTS settings
self.tts_voice = "expr-voice-2-f"  # 8 voice options available
```

## 🎨 Available TTS Voices

1. `expr-voice-2-m` - Male voice 1
2. `expr-voice-2-f` - Female voice 1 (default)
3. `expr-voice-3-m` - Male voice 2
4. `expr-voice-3-f` - Female voice 2
5. `expr-voice-4-m` - Male voice 3
6. `expr-voice-4-f` - Female voice 3
7. `expr-voice-5-m` - Male voice 4
8. `expr-voice-5-f` - Female voice 4

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Microphone    │───▶│   Whisper Tiny   │───▶│     Ollama      │
│   (Audio In)    │    │ (Speech-to-Text) │    │   (AI Model)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐             │
│    Speakers     │◀───│    KittenTTS     │◀────────────┘
│  (Audio Out)    │    │ (Text-to-Speech) │
└─────────────────┘    └──────────────────┘
```

## 📊 Performance

**Model Sizes:**
- Whisper Tiny: ~39MB
- KittenTTS: ~25MB
- Gemma3:270m: ~270MB
- **Total footprint: ~334MB**

**Memory Usage (Pi 4 with gemma3:270m):**
- Idle: ~200MB RAM
- During processing: ~800MB-1.2GB RAM
- Perfect for Pi 4 with 4GB+ RAM!

**Response Times (Pi 4):**
- Speech recognition: ~1-2 seconds
- AI response generation: ~2-5 seconds
- Speech synthesis: ~1-2 seconds
- **Total interaction: ~4-9 seconds**

## 🛠️ Troubleshooting

### Common Issues

**Audio not working:**
```bash
# Check audio devices
python -c "import pyaudio; p=pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"
```

**Ollama not responding:**
```bash
# Check if Ollama is running
ollama list
ollama serve  # Start Ollama if needed
```

**KittenTTS installation issues:**
```bash
# Alternative KittenTTS install
pip install --upgrade pip
pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl --force-reinstall
```


## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Excellent speech recognition
- [Ollama](https://ollama.ai/) - Making local LLMs accessible
- [KittenTTS](https://github.com/KittenML/KittenTTS) - Lightweight neural TTS
- [Raspberry Pi Foundation](https://www.raspberrypi.org/) - Affordable computing for everyone

## 🔗 Related Projects

- [Ollama](https://github.com/ollama/ollama) - Run LLMs locally
- [Whisper](https://github.com/openai/whisper) - Speech recognition by OpenAI
- [Voice Assistant Examples](https://github.com/topics/voice-assistant) - More voice assistant projects

---

**⭐ If this project helped you, please give it a star!**
