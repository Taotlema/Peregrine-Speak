"""
Kokoro TTS Engine wrapper for Peregrine Speak.

This module provides a high-level interface to the Kokoro text-to-speech
system, featuring natural-sounding AI voices with American and British
English variants. Kokoro offers superior voice quality compared to
traditional TTS engines like eSpeak or pyttsx3.

Key Features:
- 18 high-quality AI voices (American & British, Male & Female)
- GPU acceleration support (with CPU fallback)
- Real-time synthesis and playback
- Multi-threaded audio processing
- Robust error handling and fallbacks

Dependencies:
- kokoro: Main TTS engine with KModel and KPipeline
- torch: Neural network backend for AI voice models
- pygame: Audio playback system
- numpy: Audio data processing
- scipy: Audio file I/O (optional)
"""

import os
import threading
import queue
import tempfile
from typing import Optional, List
import numpy as np
import torch

# Import Kokoro TTS - The core AI voice synthesis engine
try:
    from kokoro import KModel, KPipeline
    KOKORO_AVAILABLE = True
    print("✓ Kokoro TTS successfully imported")
except ImportError as e:
    print(f"✗ Warning: Kokoro TTS not available: {e}")
    KOKORO_AVAILABLE = False

# Import pygame for audio playback
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("✗ Warning: pygame not available")

# Import scipy for advanced audio processing (optional)
try:
    import scipy.io.wavfile
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("✗ Warning: scipy not available")


class Voice:
    """
    Represents a single TTS voice with metadata.
    
    This class encapsulates all information about a voice including its
    display name, language variant, gender, and the internal Kokoro
    voice code used for synthesis.
    
    Attributes:
        name (str): Human-readable voice name (e.g., "🇺🇸 Heart (Female)")
        language (str): Language variant (e.g., "English (US)")
        gender (str): Voice gender ("Male" or "Female")
        voice_code (str): Kokoro internal code (e.g., "af_heart")
    """
    
    def __init__(self, name: str, language: str, gender: str,
                 voice_code: Optional[str] = None):
        """
        Initialize a Voice instance.
        
        Args:
            name: Display name for the voice
            language: Language and regional variant
            gender: Voice gender classification
            voice_code: Internal Kokoro voice identifier
        """
        self.name = name
        self.language = language
        self.gender = gender
        self.voice_code = voice_code  # Kokoro voice code (e.g., 'af_heart')


class KokoroEngine:
    """
    High-level wrapper for the Kokoro TTS system.
    
    This class provides a complete TTS solution with the following features:
    - Automatic model loading and GPU detection
    - Voice management and selection
    - Multi-threaded audio synthesis
    - Real-time playback with pygame
    - Comprehensive error handling
    
    The engine supports 18 high-quality AI voices across American and
    British English variants, with both male and female options.
    
    Example Usage:
        engine = KokoroEngine()
        if engine.is_initialized:
            voices = engine.get_available_voices()
            engine.set_voice(voices[0].name)
            engine.speak("Hello world!", speed=1.0)
    """
    
    def __init__(self):
        """
        Initialize the Kokoro TTS engine.
        
        This constructor sets up all necessary components:
        - Loads Kokoro AI models (CPU/GPU)
        - Initializes voice pipelines for different languages
        - Sets up audio playback system
        - Starts background worker thread
        - Configures voice library
        """
        # Voice and state management
        self.available_voices = []          # List of Voice objects
        self.current_voice = None           # Currently selected Voice
        self.is_initialized = False         # Engine initialization status
        self.is_speaking = False           # Current speech state
        self.is_paused = False             # Pause state
        
        # Threading and queue management
        self.speech_queue = queue.Queue()  # Queue for TTS requests
        self.worker_thread = None          # Background synthesis thread
        self._stop_event = threading.Event()  # Thread shutdown signal
        
        # Kokoro AI components
        self.models = {}                   # Dictionary of loaded AI models
        self.pipelines = {}                # Language processing pipelines
        self.cuda_available = False        # GPU availability flag
        
        # Audio configuration
        self.sample_rate = 24000           # Kokoro uses 24kHz audio
        self.current_audio = None          # Current audio buffer
        self.audio_position = 0            # Playback position
        
        # Initialize pygame mixer for audio playback
        if PYGAME_AVAILABLE:
            pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1)
        
        # Start the initialization process
        self.initialize_engine()
        
    def initialize_engine(self):
        """
        Initialize the Kokoro TTS engine and all its components.
        
        This method performs the following initialization steps:
        1. Check for Kokoro availability
        2. Detect CUDA/GPU support
        3. Load AI models (CPU and optionally GPU)
        4. Initialize language processing pipelines
        5. Set up voice library
        6. Start background worker thread
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            if not KOKORO_AVAILABLE:
                print("❌ Kokoro TTS not available, cannot initialize")
                return False
                
            # Check CUDA availability for GPU acceleration
            self.cuda_available = torch.cuda.is_available()
            print(f"🔍 CUDA available: {self.cuda_available}")
            
            # Initialize Kokoro AI models
            # CPU model is always loaded as fallback
            self.models = {
                'cpu': KModel().to('cpu').eval()
            }
            
            # Load GPU model if CUDA is available
            if self.cuda_available:
                try:
                    self.models['gpu'] = KModel().to('cuda').eval()
                    print("🚀 GPU model loaded successfully")
                except Exception as e:
                    print(f"⚠️ Failed to load GPU model: {e}")
                    self.cuda_available = False
            
            # Initialize pipelines for American and British English
            self.pipelines = {
                'a': KPipeline(lang_code='a', model=False),  # American
                'b': KPipeline(lang_code='b', model=False)   # British
            }
            
            # Set up the voice library with all available voices
            self.setup_kokoro_voices()
            
            # Start background worker thread for audio processing
            self.start_worker_thread()
            
            self.is_initialized = True
            print("✅ Kokoro TTS Engine initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize Kokoro TTS Engine: {e}")
            import traceback
            traceback.print_exc()
            self.is_initialized = False
            return False
            
    def setup_kokoro_voices(self):
        """Set up available Kokoro voices."""
        try:
            # Define available Kokoro voices with friendly names
            kokoro_voices = [
                # American Female Voices
                ('af_heart', '🇺🇸 Heart (Female)', 'English (US)', 'Female'),
                ('af_bella', '🇺🇸 Bella (Female)', 'English (US)', 'Female'),
                ('af_nicole', '🇺🇸 Nicole (Female)', 'English (US)', 'Female'),
                ('af_sarah', '🇺🇸 Sarah (Female)', 'English (US)', 'Female'),
                ('af_nova', '🇺🇸 Nova (Female)', 'English (US)', 'Female'),
                ('af_alloy', '🇺🇸 Alloy (Female)', 'English (US)', 'Female'),
                
                # American Male Voices
                ('am_michael', '🇺🇸 Michael (Male)', 'English (US)', 'Male'),
                ('am_adam', '🇺🇸 Adam (Male)', 'English (US)', 'Male'),
                ('am_echo', '🇺🇸 Echo (Male)', 'English (US)', 'Male'),
                ('am_liam', '🇺🇸 Liam (Male)', 'English (US)', 'Male'),
                ('am_onyx', '🇺🇸 Onyx (Male)', 'English (US)', 'Male'),
                
                # British Female Voices
                ('bf_alice', '🇬🇧 Alice (Female)', 'English (UK)', 'Female'),
                ('bf_emma', '🇬🇧 Emma (Female)', 'English (UK)', 'Female'),
                ('bf_isabella', '🇬🇧 Isabella (Female)',
                 'English (UK)', 'Female'),
                ('bf_lily', '🇬🇧 Lily (Female)', 'English (UK)', 'Female'),
                
                # British Male Voices 
                ('bm_daniel', '🇬🇧 Daniel (Male)', 'English (UK)', 'Male'),
                ('bm_george', '🇬🇧 George (Male)', 'English (UK)', 'Male'),
                ('bm_lewis', '🇬🇧 Lewis (Male)', 'English (UK)', 'Male'),
            ]
            
            # Create Voice objects
            voices = []
            for voice_code, name, language, gender in kokoro_voices:
                voice = Voice(name, language, gender, voice_code)
                voices.append(voice)
                
            self.available_voices = voices
            if voices:
                self.current_voice = voices[0]  # Default to first voice
                
            print(f"Set up {len(voices)} Kokoro voices")
            return True
            
        except Exception as e:
            print(f"Error setting up Kokoro voices: {e}")
            return False
            
    def start_worker_thread(self):
        """Start the worker thread for TTS processing."""
        if self.worker_thread is None or not self.worker_thread.is_alive():
            self._stop_event.clear()
            self.worker_thread = threading.Thread(
                target=self._worker_loop, daemon=True)
            self.worker_thread.start()
            
    def _worker_loop(self):
        """Worker thread loop for processing TTS requests."""
        while not self._stop_event.is_set():
            try:
                task = self.speech_queue.get(timeout=1.0)
                if task is None:  # Shutdown signal
                    break
                    
                if task['action'] == 'speak':
                    self._synthesize_with_kokoro(task['text'], task['speed'])
                elif task['action'] == 'stop':
                    self.is_speaking = False
                    self.is_paused = False
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"TTS worker error: {e}")
                import traceback
                traceback.print_exc()
                
    def get_available_voices(self) -> List[Voice]:
        """Get list of available voices."""
        return self.available_voices
        
    def set_voice(self, voice_name: str) -> bool:
        """Set the current voice by name."""
        for voice in self.available_voices:
            if voice.name == voice_name:
                self.current_voice = voice
                print(f"Voice changed to: {voice_name}")
                return True
        return False
        
    def speak(self, text: str, speed: float = 1.0):
        """
        Queue text for TTS synthesis and playback.
        
        This is the main public interface for text-to-speech conversion.
        The method queues the request and returns immediately, with actual
        synthesis happening in the background worker thread.
        
        Args:
            text: Text to synthesize (supports any length)
            speed: Speech speed multiplier (0.5-2.0 range recommended)
                  1.0 = normal speed, 0.5 = half speed, 2.0 = double speed
        """
        # Validate engine state
        if not self.is_initialized:
            print("❌ TTS engine not initialized")
            return
            
        if not text.strip():
            print("⚠️ Empty text provided")
            return
            
        # Stop any current speech and clear queue
        self.stop()
        
        # Queue the new synthesis request
        self.speech_queue.put({
            'action': 'speak',
            'text': text.strip(),
            'speed': speed
        })
        
        # Update state
        self.is_speaking = True
        self.is_paused = False
        print(f"📝 Queued TTS for: '{text[:50]}...'")
        
    def pause(self):
        """
        Pause current TTS playback.
        
        Temporarily stops audio playback without losing position.
        Use resume() to continue from where it left off.
        """
        if PYGAME_AVAILABLE and pygame.mixer.get_init():
            pygame.mixer.music.pause()
            self.is_paused = True
            print("⏸️ TTS paused")
        
    def resume(self):
        """
        Resume paused TTS playback.
        
        Continues playback from where it was paused.
        Only works if TTS was previously paused, not stopped.
        """
        if PYGAME_AVAILABLE and pygame.mixer.get_init():
            pygame.mixer.music.unpause()
            self.is_paused = False
            print("▶️ TTS resumed")
        
    def stop(self):
        """
        Stop TTS playback and clear all queued requests.
        
        This completely stops current synthesis and playback,
        clearing any pending requests in the queue.
        """
        # Clear all queued requests
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
            except queue.Empty:
                break
                
        # Stop pygame audio playback
        if PYGAME_AVAILABLE and pygame.mixer.get_init():
            pygame.mixer.music.stop()
            
        # Reset state
        self.is_speaking = False
        self.is_paused = False
        print("⏹️ TTS stopped")
        
    def is_speaking_now(self) -> bool:
        """
        Check if TTS is currently active.
        
        Returns:
            bool: True if currently speaking (not paused), False otherwise
        """
        return self.is_speaking and not self.is_paused
        
    def _synthesize_with_kokoro(self, text: str, speed: float):
        """
        Synthesize text using the Kokoro AI TTS system.
        
        This method performs the complete TTS pipeline:
        1. Validate voice selection and parameters
        2. Select appropriate language pipeline (American/British)
        3. Load the specific voice model
        4. Choose AI model (GPU preferred, CPU fallback)
        5. Process text through phoneme generation
        6. Generate audio using neural synthesis
        7. Play audio through pygame
        
        The synthesis process uses advanced AI models to generate
        natural-sounding speech with proper intonation, rhythm, and
        emotional expression.
        
        Args:
            text: Text to synthesize (any length supported)
            speed: Speech speed multiplier (0.5-2.0 recommended)
        """
        try:
            # Validate current voice selection
            if not self.current_voice or not self.current_voice.voice_code:
                print("❌ No voice selected")
                return
                
            voice_code = self.current_voice.voice_code
            voice_name = self.current_voice.name
            
            print(f"🗣️ Synthesizing with Kokoro: '{text[:50]}...' "
                  f"using {voice_name} (speed: {speed}x)")
            
            # Get the appropriate pipeline for this voice
            # First character of voice_code indicates language:
            # 'a' = American English, 'b' = British English
            lang_code = voice_code[0]
            if lang_code not in self.pipelines:
                print(f"❌ Pipeline not available for language: {lang_code}")
                return
                
            pipeline = self.pipelines[lang_code]
            
            # Load the voice pack (neural voice embeddings)
            voice_pack = pipeline.load_voice(voice_code)
            if voice_pack is None or len(voice_pack) == 0:
                print(f"❌ Failed to load voice: {voice_code}")
                return
            
            # Choose AI model based on availability
            # GPU provides faster synthesis, CPU is the fallback
            use_gpu = self.cuda_available and 'gpu' in self.models
            model = self.models['gpu' if use_gpu else 'cpu']
            
            print(f"🚀 Using {'GPU' if use_gpu else 'CPU'} model for synthesis")
            
            # Generate audio through the AI pipeline
            audio_chunks = []
            for _, phonemes, _ in pipeline(text, voice_code, speed):
                # Get reference audio embedding for this phoneme sequence
                ref_s = voice_pack[len(phonemes)-1]
                
                # Move tensors to appropriate device (GPU/CPU)
                if use_gpu:
                    phonemes = phonemes.cuda()
                    ref_s = ref_s.cuda()
                
                # Generate audio chunk using neural synthesis
                audio_chunk = model(phonemes, ref_s, speed)
                
                # Convert back to CPU and numpy for audio playback
                audio_chunk = audio_chunk.cpu().numpy()
                audio_chunks.append(audio_chunk)
            
            if not audio_chunks:
                print("❌ No audio generated")
                return
                
            # Combine all audio chunks into final audio
            full_audio = np.concatenate(audio_chunks, axis=0)
            
            # Play the synthesized audio
            self._play_audio(full_audio)
            
            print("✅ Kokoro synthesis completed successfully")
            
        except Exception as e:
            print(f"❌ Kokoro synthesis error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Always reset speaking state
            self.is_speaking = False
            
    def _play_audio(self, audio_data: np.ndarray):
        """
        Play audio using pygame.
        
        Args:
            audio_data: Audio data as numpy array
        """
        try:
            if not PYGAME_AVAILABLE:
                print("pygame not available for audio playback")
                return
                
            # Ensure audio is in the right format
            if audio_data.dtype != np.int16:
                # Convert from float to int16
                audio_data = (audio_data * 32767).astype(np.int16)
            
            # Create a temporary file for pygame
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                if SCIPY_AVAILABLE:
                    import scipy.io.wavfile as wav
                    wav.write(tmp_file.name, self.sample_rate, audio_data)
                else:
                    # Fallback: write raw audio (less compatible)
                    with open(tmp_file.name, 'wb') as f:
                        f.write(audio_data.tobytes())
                
                # Load and play with pygame
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback to complete
                while pygame.mixer.music.get_busy() and self.is_speaking:
                    pygame.time.wait(100)
                    
                # Clean up temporary file
                os.unlink(tmp_file.name)
                
        except Exception as e:
            print(f"Audio playback error: {e}")
            import traceback
            traceback.print_exc()
            
    def cleanup(self):
        """Clean up resources."""
        try:
            # Stop worker thread
            self._stop_event.set()
            self.speech_queue.put(None)  # Signal shutdown
            
            if self.worker_thread and self.worker_thread.is_alive():
                self.worker_thread.join(timeout=2.0)
            
            # Stop audio
            self.stop()
            
            # Cleanup pygame
            if PYGAME_AVAILABLE:
                pygame.mixer.quit()
                
            print("Kokoro TTS Engine cleaned up")
            
        except Exception as e:
            print(f"Cleanup error: {e}")
            
    def __del__(self):
        """Destructor."""
        self.cleanup()
