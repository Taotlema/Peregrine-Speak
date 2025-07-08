#!/usr/bin/env python3
"""
Test script for Kokoro TTS integration.
"""

import sys
import os

# Add the src path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from peregrine_speak.tts.kokoro_engine import KokoroEngine


def test_kokoro_engine():
    """Test the Kokoro TTS engine."""
    print("Testing Kokoro TTS Engine...")
    
    # Initialize the engine
    engine = KokoroEngine()
    
    if not engine.is_initialized:
        print("❌ Engine failed to initialize")
        return False
        
    print("✅ Engine initialized successfully")
    
    # Test voice listing
    voices = engine.get_available_voices()
    print(f"📢 Found {len(voices)} voices:")
    for voice in voices:
        print(f"  - {voice.name} ({voice.language}, {voice.gender})")
        
    if not voices:
        print("❌ No voices available")
        return False
        
    # Test synthesis
    test_text = "Hello! This is a test of the Kokoro TTS engine."
    print(f"\n🗣️ Testing synthesis with text: '{test_text}'")
    
    try:
        engine.speak(test_text, speed=1.0)
        print("✅ Synthesis started successfully")
        
        # Wait a bit for synthesis to complete
        import time
        time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"❌ Synthesis failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        engine.cleanup()


if __name__ == "__main__":
    success = test_kokoro_engine()
    if success:
        print("\n🎉 Kokoro TTS test completed successfully!")
    else:
        print("\n❌ Kokoro TTS test failed!")
    
    sys.exit(0 if success else 1)
