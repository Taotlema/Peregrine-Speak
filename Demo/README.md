# Peregrine Speak - Application Specifics

## Project Purpose

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
   
## Architecture

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

## Usage Guide

### Basic Operation
1. **Launch** the application with `python main.py`
2. **Enter text** in the main text area
3. **Select voice** using the Voice button
4. **Adjust speed** with the speed control (x1, x1.5, x2)
5. **Click play** to start synthesis
6. **Use controls** to pause, resume, or stop playback

### Debug Mode
Enable verbose logging by setting environment variable:
```bash
export KOKORO_DEBUG=1
python main.py
```

## Dependencies

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

## Performance

### Synthesis Speed
- **GPU**: ~2-5x real-time (depending on hardware)
- **CPU**: ~0.5-1x real-time (modern processors)
- **Quality**: Consistent high quality regardless of speed

### Memory Usage
- **Base**: ~200MB (models loaded)
- **Peak**: ~500MB (during synthesis)
- **Streaming**: Efficient for long texts

## Contributors

Most definently need to credit the billaint developer behiend Kokoro

## License

Need to update

## Acknowledgments
- **Kokoro TTS**: For the incredible AI voice synthesis technology
- **PyQt6**: For the robust GUI framework
- **PyTorch**: For the machine learning infrastructure
- **Open Source Community**: For the tools and libraries that make this possible

