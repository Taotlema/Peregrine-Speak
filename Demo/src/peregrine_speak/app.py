"""
Main application class for Peregrine Speak.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

from .ui.home_screen import HomeScreen
from .ui.main_screen import MainScreen
from .ui.voice_selection import VoiceSelection
from .tts.kokoro_engine import KokoroEngine


class PeregrineApp:
    """Main application class that manages the entire Peregrine Speak application."""
    
    def __init__(self):
        """Initialize the Peregrine Speak application."""
        self.app = QApplication(sys.argv)
        self.setup_application()
        
        # Initialize TTS engine
        self.tts_engine = KokoroEngine()
        
        # Initialize screens
        self.home_screen = None
        self.main_screen = None
        self.voice_selection = None
        
        self.setup_screens()
    
    def setup_application(self):
        """Set up application-wide settings."""
        self.app.setApplicationName("Peregrine Speak")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("Peregrine AI")
        
        # Set application icon (placeholder for now)
        # TODO: Add actual Peregrine logo
        
        # Set default font
        font = QFont("Arial", 10)
        self.app.setFont(font)
        
        # Set application style
        self.app.setStyle("Fusion")
    
    def setup_screens(self):
        """Initialize all application screens."""
        # Create home screen
        self.home_screen = HomeScreen(self)
        
        # Create main screen (hidden initially)
        self.main_screen = MainScreen(self)
        
        # Create voice selection dialog
        self.voice_selection = VoiceSelection(self)
    
    def show_home_screen(self):
        """Show the home screen."""
        if self.main_screen:
            self.main_screen.hide()
        self.home_screen.show()
    
    def show_main_screen(self):
        """Show the main screen with fade transition."""
        self.home_screen.fade_to_main_screen()
    
    def show_voice_selection(self):
        """Show the voice selection dialog."""
        self.voice_selection.show()
    
    def get_tts_engine(self):
        """Get the TTS engine instance."""
        return self.tts_engine
    
    def close_application(self):
        """Close the application."""
        self.app.quit()
    
    def run(self):
        """Run the application."""
        self.home_screen.show()
        return self.app.exec()
