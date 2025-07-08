"""
Voice Selection dialog for Peregrine Speak application.
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class VoiceItem(QFrame):
    """Individual voice item widget."""
    
    def __init__(self, voice_name, language, flag_emoji, parent_dialog):
        super().__init__()
        self.voice_name = voice_name
        self.language = language
        self.flag_emoji = flag_emoji
        self.parent_dialog = parent_dialog
        self.selected = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the voice item UI."""
        self.setMinimumHeight(80)
        self.setStyleSheet("""
            VoiceItem {
                background: rgba(100, 100, 100, 0.7);
                border-radius: 10px;
                margin: 5px;
            }
            VoiceItem:hover {
                background: rgba(120, 120, 120, 0.8);
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Flag icon
        flag_label = QLabel(self.flag_emoji)
        flag_label.setStyleSheet("""
            font-size: 24px;
            background: white;
            border-radius: 15px;
            padding: 5px;
            min-width: 30px;
            max-width: 30px;
            min-height: 30px;
            max-height: 30px;
        """)
        flag_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Voice name label
        name_label = QLabel(self.voice_name)
        name_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding-left: 15px;
        """)
        
        layout.addWidget(flag_label)
        layout.addWidget(name_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def mousePressEvent(self, event):
        """Handle mouse press to select voice."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent_dialog.select_voice(self)
            
    def set_selected(self, selected):
        """Set the selection state of this voice item."""
        self.selected = selected
        if selected:
            self.setStyleSheet("""
                VoiceItem {
                    background: rgba(100, 150, 200, 0.9);
                    border: 2px solid rgba(100, 150, 200, 1.0);
                    border-radius: 10px;
                    margin: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                VoiceItem {
                    background: rgba(100, 100, 100, 0.7);
                    border-radius: 10px;
                    margin: 5px;
                }
                VoiceItem:hover {
                    background: rgba(120, 120, 120, 0.8);
                }
            """)


class VoiceSelection(QDialog):
    """Voice selection dialog window."""
    
    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance
        self.selected_voice = None
        self.voice_items = []
        
        self.setup_ui()
        self.setup_voices()
        
    def setup_ui(self):
        """Set up the voice selection UI."""
        self.setWindowTitle("Select Voice")
        self.setModal(True)
        self.resize(400, 500)
        
        # Set gradient background
        self.setStyleSheet("""
            VoiceSelection {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #e6f3ff,
                    stop: 1 #ddeeff
                );
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Choose Voice")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #333;
            padding: 10px;
        """)
        layout.addWidget(title_label)
        
        # Scroll area for voices
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        # Container for voice items
        self.voices_container = QWidget()
        self.voices_layout = QVBoxLayout()
        self.voices_layout.setSpacing(10)
        self.voices_container.setLayout(self.voices_layout)
        
        scroll_area.setWidget(self.voices_container)
        layout.addWidget(scroll_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumHeight(40)
        cancel_button.clicked.connect(self.reject)
        
        # Select button
        self.select_button = QPushButton("Select")
        self.select_button.setMinimumHeight(40)
        self.select_button.setEnabled(False)
        self.select_button.clicked.connect(self.accept_selection)
        
        # Style buttons
        button_style = """
            QPushButton {
                background: rgba(100, 100, 100, 0.7);
                border: none;
                border-radius: 20px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: rgba(100, 100, 100, 0.9);
            }
            QPushButton:pressed {
                background: rgba(80, 80, 80, 0.9);
            }
            QPushButton:disabled {
                background: rgba(150, 150, 150, 0.5);
                color: rgba(255, 255, 255, 0.5);
            }
        """
        
        cancel_button.setStyleSheet(button_style)
        self.select_button.setStyleSheet(button_style)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.select_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def setup_voices(self):
        """Set up the available voices."""
        # Get voices from TTS engine
        tts_engine = self.app_instance.get_tts_engine()
        voices = tts_engine.get_available_voices()
        
        # Create UI items for each voice
        for voice in voices:
            # Map language to flag emoji
            flag_emoji = "🇺🇸" if "US" in voice.language else "🇬🇧"
            voice_item = VoiceItem(
                voice.name, voice.language, flag_emoji, self
            )
            self.voice_items.append(voice_item)
            self.voices_layout.addWidget(voice_item)
            
        # Add stretch to push items to top
        self.voices_layout.addStretch()
        
    def select_voice(self, voice_item):
        """Select a voice item."""
        # Deselect all other voices
        for item in self.voice_items:
            item.set_selected(False)
            
        # Select the clicked voice
        voice_item.set_selected(True)
        self.selected_voice = voice_item
        self.select_button.setEnabled(True)
        
    def accept_selection(self):
        """Accept the selected voice."""
        if self.selected_voice:
            voice_name = self.selected_voice.voice_name
            print(f"Selected voice: {voice_name}")
            
            # Apply voice selection to TTS engine
            tts_engine = self.app_instance.get_tts_engine()
            tts_engine.set_voice(voice_name)
            
            self.accept()
            
    def get_selected_voice(self):
        """Get the currently selected voice."""
        return self.selected_voice.voice_name if self.selected_voice else None
