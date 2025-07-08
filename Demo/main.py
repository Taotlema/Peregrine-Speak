#!/usr/bin/env python3
"""
Peregrine Speak - Text-to-Speech Desktop Application
Main entry point for the application.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from peregrine_speak.app import PeregrineApp

def main():
    """Main entry point for Peregrine Speak application."""
    app = PeregrineApp()
    return app.run()

if __name__ == "__main__":
    sys.exit(main())
