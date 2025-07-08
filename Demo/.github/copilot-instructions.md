<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Peregrine Speak Development Guidelines

## Project Context
This is a Python desktop application called "Peregrine Speak" - a text-to-speech application using PyQt6 for the GUI and Kokoro TTS for speech synthesis. The application runs locally without requiring internet connectivity.

## Code Style and Standards
- Use Python 3.8+ features and syntax
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write descriptive docstrings for classes and methods
- Prefer composition over inheritance
- Use descriptive variable and function names

## Architecture Guidelines
- Keep UI components separate from business logic
- Use the MVC/MVP pattern where applicable
- Keep TTS engine wrapper modular and testable
- Implement proper error handling and logging
- Use threading for TTS operations to avoid blocking the UI

## PyQt6 Specific Guidelines
- Use signal/slot mechanism for component communication
- Implement proper resource cleanup in destructors
- Use QTimer for animations and delayed operations
- Apply consistent styling with QStyleSheet
- Handle window events properly (show, hide, close)

## TTS Integration Guidelines
- Keep Kokoro TTS integration modular and replaceable
- Implement audio playback controls (play, pause, resume, stop)
- Handle audio device detection and configuration
- Provide voice selection and speed control
- Implement proper audio threading to prevent UI blocking

## Error Handling
- Gracefully handle missing audio devices
- Provide user-friendly error messages
- Log errors for debugging without crashing the app
- Handle missing TTS models or dependencies
- Implement fallback behaviors where possible

## Testing Considerations
- Write unit tests for business logic
- Mock audio operations for testing
- Test UI components independently when possible
- Verify cross-platform compatibility (Windows, Linux, macOS)

## Dependencies
- PyQt6 for GUI framework
- Kokoro for TTS engine
- sounddevice for audio playback
- PyTorch for ML model support
- numpy for audio processing

## File Organization
- Keep UI components in `src/peregrine_speak/ui/`
- Keep TTS components in `src/peregrine_speak/tts/`
- Store assets in `assets/` directory
- Use proper Python package structure with `__init__.py` files
