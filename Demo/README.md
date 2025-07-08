# Peregrine Speak - AI Text-to-Speech Application

A modern, high-quality text-to-speech application powered by Kokoro AI voices and built with PyQt6.

## 🎯 Overview

Peregrine Speak provides natural-sounding text-to-speech synthesis using state-of-the-art AI voices. The application features an intuitive GUI with real-time playback controls and a selection of 18 high-quality voices in American and British English variants.

## ✨ Features

### 🎤 High-Quality AI Voices
- **18 Premium Voices**: 11 American English + 7 British English
- **Both Genders**: Male and female voice options
- **Natural Sound**: AI-powered synthesis with human-like intonation
- **Voice Variety**: Multiple personalities and speaking styles

### 🎛️ Advanced Controls
- **Real-time Playback**: Play, pause, resume, and stop controls
- **Speed Control**: Adjustable speech speed (0.5x to 2.0x)
- **Voice Selection**: Easy switching between available voices
- **Text Management**: Large text area with clear/discard functionality

### 🔧 Technical Features
- **GPU Acceleration**: Automatic CUDA detection with CPU fallback
- **Multi-threading**: Non-blocking audio synthesis
- **Error Handling**: Robust error recovery and logging
- **Modern UI**: Beautiful gradient interface with smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Linux, macOS, or Windows
- Audio output device

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Peregrine-Speak/Demo
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## 🎵 Available Voices

### American English 🇺🇸
**Female Voices:**
- Heart ❤️ (Warm and friendly)
- Bella 🔥 (Energetic and clear)
- Nicole 🎧 (Professional and smooth)
- Sarah (Natural and versatile)
- Nova (Modern and crisp)
- Alloy (Balanced and reliable)

**Male Voices:**
- Michael (Deep and authoritative)
- Adam (Friendly and approachable)
- Echo (Clear and resonant)
- Liam (Young and dynamic)
- Onyx (Rich and expressive)

### British English 🇬🇧
**Female Voices:**
- Alice (Elegant and refined)
- Emma (Professional and clear)
- Isabella (Sophisticated and warm)
- Lily (Light and pleasant)

**Male Voices:**
- Daniel (Distinguished and clear)
- George (Traditional and authoritative)
- Lewis (Modern and friendly)

## 🏗️ Architecture

### Core Components

```
src/
├── peregrine_speak/
│   ├── app.py              # Main application controller
│   ├── tts/
│   │   └── kokoro_engine.py # Kokoro TTS integration
│   └── ui/
│       ├── home_screen.py   # Welcome screen
│       ├── main_screen.py   # Main TTS interface
│       └── voice_selection.py # Voice picker
```

### Key Technologies
- **Kokoro TTS**: AI voice synthesis engine
- **PyQt6**: Modern GUI framework
- **PyTorch**: Neural network backend
- **pygame**: Audio playback system
- **numpy**: Audio data processing

## 🔧 Configuration

### Audio Settings
The application automatically detects your audio hardware and configures optimal settings:
- **Sample Rate**: 24kHz (Kokoro native)
- **Channels**: Mono output
- **Format**: 16-bit PCM

### Performance Tuning
- **GPU Detection**: Automatic CUDA utilization when available
- **CPU Fallback**: Seamless fallback for systems without GPU
- **Memory Management**: Efficient audio buffer handling

## 📝 Usage Guide

### Basic Operation
1. **Launch** the application with `python main.py`
2. **Enter text** in the main text area
3. **Select voice** using the Voice button
4. **Adjust speed** with the speed control (x1, x1.5, x2)
5. **Click play** to start synthesis
6. **Use controls** to pause, resume, or stop playback

### Advanced Features
- **Large Text Support**: Handle documents of any size
- **Speed Control**: Fine-tune speech rate for different content
- **Voice Switching**: Change voices mid-session
- **Real-time Control**: Interrupt and control playback instantly

## 🧪 Testing

### Quick Test
```bash
python test_kokoro_integration.py
```

This will verify:
- ✅ Kokoro engine initialization
- ✅ Voice loading and availability
- ✅ Audio synthesis and playback
- ✅ Cleanup and resource management

### Expected Output
```
✓ Kokoro TTS successfully imported
Testing Kokoro TTS Engine...
✅ Engine initialized successfully
📢 Found 18 voices
🗣️ Testing synthesis...
✅ Synthesis started successfully
🎉 Kokoro TTS test completed successfully!
```

## 🛠️ Troubleshooting

### Common Issues

**No Audio Output**
- Check system audio settings
- Verify audio device connection
- Try different output device

**Slow Performance**
- Install CUDA drivers for GPU acceleration
- Close other resource-intensive applications
- Use shorter text segments

**Voice Loading Errors**
- Check internet connection (first-time setup)
- Verify disk space for model downloads
- Clear cache and restart application

### Debug Mode
Enable verbose logging by setting environment variable:
```bash
export KOKORO_DEBUG=1
python main.py
```

## 📦 Dependencies

### Core Requirements
```
PyQt6>=6.4.0          # GUI framework
torch>=2.0.0           # Neural network backend
numpy>=1.21.0          # Numerical computing
pygame>=2.1.0          # Audio playback
kokoro                 # AI TTS engine
```

### Audio Processing
```
sounddevice>=0.4.0     # Audio device interface
scipy>=1.9.0           # Signal processing
soundfile>=0.12.0      # Audio file I/O
```

### Language Processing
```
misaki[en]             # English phonemization
espeak-ng              # Phoneme generation
```

## 🎯 Performance

### Synthesis Speed
- **GPU**: ~2-5x real-time (depending on hardware)
- **CPU**: ~0.5-1x real-time (modern processors)
- **Quality**: Consistent high quality regardless of speed

### Memory Usage
- **Base**: ~200MB (models loaded)
- **Peak**: ~500MB (during synthesis)
- **Streaming**: Efficient for long texts

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for:
- Code style and standards
- Testing requirements
- Documentation updates
- Feature requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Kokoro TTS**: For the incredible AI voice synthesis technology
- **PyQt6**: For the robust GUI framework
- **PyTorch**: For the machine learning infrastructure
- **Open Source Community**: For the tools and libraries that make this possible

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the test scripts for examples

---

**Peregrine Speak** - Bringing natural AI voices to everyone! 🦅🗣️
