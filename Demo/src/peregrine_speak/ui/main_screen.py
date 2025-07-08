"""
Main Screen for Peregrine Speak application with TTS functionality.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QLabel, QFrame, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon
from enum import Enum


class PlaybackSpeed(Enum):
    """Enumeration for playback speeds."""
    NORMAL = (1.0, "x1")
    FAST = (1.5, "x1.5")
    FASTER = (2.0, "x2")


class MainScreen(QWidget):
    """Main screen widget with TTS controls and text input."""
    
    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance
        self.current_speed = PlaybackSpeed.NORMAL
        self.is_playing = False
        self.is_paused = False
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Peregrine Speak")
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        
        # Set gradient background
        self.setStyleSheet("""
            MainScreen {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #f0f8ff,
                    stop: 0.5 #e6f3ff,
                    stop: 1 #ddeeff
                );
            }
        """)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Control buttons bar
        control_bar = self.create_control_bar()
        layout.addWidget(control_bar)
        
        # Text input area
        text_area = self.create_text_area()
        layout.addWidget(text_area)
        
        # Close button
        close_button = self.create_close_button()
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
    def create_control_bar(self):
        """Create the control buttons bar."""
        control_frame = QFrame()
        control_frame.setStyleSheet("""
            QFrame {
                background: rgba(200, 200, 200, 0.3);
                border-radius: 15px;
                padding: 10px;
            }
        """)
        control_frame.setMaximumHeight(80)
        
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Play button
        self.play_button = QPushButton("▶")
        self.play_button.setMinimumSize(50, 50)
        self.play_button.clicked.connect(self.on_play_clicked)
        
        # Pause button
        self.pause_button = QPushButton("⏸")
        self.pause_button.setMinimumSize(50, 50)
        self.pause_button.clicked.connect(self.on_pause_clicked)
        
        # Discard button
        self.discard_button = QPushButton("🗑")
        self.discard_button.setMinimumSize(50, 50)
        self.discard_button.clicked.connect(self.on_discard_clicked)
        
        # Speed button
        self.speed_button = QPushButton("x1")
        self.speed_button.setMinimumSize(60, 50)
        self.speed_button.clicked.connect(self.on_speed_clicked)
        
        # Voice button
        self.voice_button = QPushButton("Voice")
        self.voice_button.setMinimumSize(80, 50)
        self.voice_button.clicked.connect(self.on_voice_clicked)
        
        # Style all buttons
        button_style = """
            QPushButton {
                background: rgba(100, 100, 100, 0.7);
                border: none;
                border-radius: 25px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(100, 100, 100, 0.9);
            }
            QPushButton:pressed {
                background: rgba(80, 80, 80, 0.9);
            }
        """
        
        for button in [self.play_button, self.pause_button,
                       self.discard_button, self.speed_button,
                       self.voice_button]:
            button.setStyleSheet(button_style)
        
        layout.addStretch()
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.discard_button)
        layout.addWidget(self.speed_button)
        layout.addWidget(self.voice_button)
        layout.addStretch()
        
        control_frame.setLayout(layout)
        return control_frame
        
    def create_text_area(self):
        """Create the text input area."""
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter or paste your text here...")
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(150, 150, 150, 0.3);
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border: 2px solid rgba(100, 150, 200, 0.6);
            }
        """)
        self.text_edit.setMinimumHeight(300)
        
        return self.text_edit
        
    def create_close_button(self):
        """Create the close application button."""
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        
        self.close_button = QPushButton("Close App")
        self.close_button.setMinimumSize(120, 40)
        self.close_button.setStyleSheet("""
            QPushButton {
                background: rgba(200, 100, 100, 0.8);
                border: none;
                border-radius: 20px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: rgba(200, 100, 100, 1.0);
            }
            QPushButton:pressed {
                background: rgba(180, 80, 80, 1.0);
            }
        """)
        self.close_button.clicked.connect(self.on_close_clicked)
        
        close_layout.addWidget(self.close_button)
        close_layout.addStretch()
        
        close_frame = QFrame()
        close_frame.setLayout(close_layout)
        return close_frame
        
    def setup_animations(self):
        """Set up animations for the main screen."""
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
    def showEvent(self, event):
        """Handle show event with fade in."""
        super().showEvent(event)
        self.fade_in()
        
    def fade_in(self):
        """Fade in the main screen."""
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
        
    def on_play_clicked(self):
        """Handle play button click."""
        text = self.text_edit.toPlainText().strip()
        print(f"Play button clicked. Text length: {len(text)}")
        
        if not text:
            print("No text to speak!")
            return
            
        if self.is_paused:
            # Resume playback
            print("Resuming TTS...")
            self.resume_tts()
        else:
            # Start new playback
            print(f"Starting TTS with text: '{text[:50]}...'")
            self.start_tts(text)
            
    def on_pause_clicked(self):
        """Handle pause button click."""
        if self.is_playing:
            self.pause_tts()
            
    def on_discard_clicked(self):
        """Handle discard button click."""
        self.text_edit.clear()
        self.stop_tts()
        
    def on_speed_clicked(self):
        """Handle speed button click - cycle through speeds."""
        speeds = list(PlaybackSpeed)
        current_index = speeds.index(self.current_speed)
        next_index = (current_index + 1) % len(speeds)
        self.current_speed = speeds[next_index]
        
        self.speed_button.setText(self.current_speed.value[1])
        
    def on_voice_clicked(self):
        """Handle voice button click."""
        self.app_instance.show_voice_selection()
        
    def on_close_clicked(self):
        """Handle close button click."""
        self.app_instance.close_application()
        
    def start_tts(self, text):
        """Start text-to-speech synthesis."""
        tts_engine = self.app_instance.get_tts_engine()
        speed = self.current_speed.value[0]
        tts_engine.speak(text, speed)
        self.is_playing = True
        self.is_paused = False
        
    def pause_tts(self):
        """Pause text-to-speech synthesis."""
        tts_engine = self.app_instance.get_tts_engine()
        tts_engine.pause()
        self.is_paused = True
        
    def resume_tts(self):
        """Resume text-to-speech synthesis."""
        tts_engine = self.app_instance.get_tts_engine()
        tts_engine.resume()
        self.is_paused = False
        
    def stop_tts(self):
        """Stop text-to-speech synthesis."""
        tts_engine = self.app_instance.get_tts_engine()
        tts_engine.stop()
        self.is_playing = False
        self.is_paused = False
