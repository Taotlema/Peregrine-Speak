"""
Home Screen for Peregrine Speak application.
"""

from PyQt6.QtWidgets import (QWidget, QPushButton,
                             QLabel, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import (QFont, QPalette, QLinearGradient, QBrush, QColor, 
                         QPainter, QPainterPath, QPixmap)
import time
import os
from pathlib import Path


class TypewriterLabel(QLabel):
    """A label that displays text with a typewriter animation effect."""
    
    finished = pyqtSignal()
    
    def __init__(self, full_text: str, parent=None):
        super().__init__(parent)
        self.full_text = full_text
        self.current_text = ""
        self.current_index = 0
        
        # Set up the label
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        
        # Timer for typewriter effect
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_next_character)
        
    def start_animation(self, delay_ms: int = 100):
        """Start the typewriter animation."""
        self.current_text = ""
        self.current_index = 0
        self.setText("")
        self.timer.start(delay_ms)
        
    def add_next_character(self):
        """Add the next character to the display."""
        if self.current_index < len(self.full_text):
            self.current_text += self.full_text[self.current_index]
            self.setText(self.current_text)
            self.current_index += 1
        else:
            self.timer.stop()
            self.finished.emit()


class PeregrineLogo(QWidget):
    """Custom widget that draws the Peregrine logo shape."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(300, 300)
        
    def paintEvent(self, event):
        """Paint the Peregrine logo shape."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get widget dimensions
        width = self.width()
        height = self.height()
        
        # Create the logo path (simplified Peregrine shape)
        path = QPainterPath()
        
        # Main body (angular bird-like shape)
        # Start from top-left, create angular peregrine falcon silhouette
        center_x = width // 2
        center_y = height // 2
        
        # Head/beak (top triangle)
        path.moveTo(center_x, center_y - 80)
        path.lineTo(center_x - 30, center_y - 40)
        path.lineTo(center_x + 10, center_y - 40)
        path.lineTo(center_x, center_y - 80)
        
        # Body (diamond-like shape)
        path.moveTo(center_x - 30, center_y - 40)
        path.lineTo(center_x - 60, center_y)
        path.lineTo(center_x - 30, center_y + 60)
        path.lineTo(center_x + 40, center_y + 40)
        path.lineTo(center_x + 60, center_y - 20)
        path.lineTo(center_x + 10, center_y - 40)
        path.lineTo(center_x - 30, center_y - 40)
        
        # Wing detail (additional angular element)
        wing_path = QPainterPath()
        wing_path.moveTo(center_x - 20, center_y - 20)
        wing_path.lineTo(center_x + 20, center_y - 10)
        wing_path.lineTo(center_x + 30, center_y + 20)
        wing_path.lineTo(center_x - 10, center_y + 30)
        wing_path.lineTo(center_x - 20, center_y - 20)
        
        # Set gradient fill
        gradient = QLinearGradient(0, 0, width, height)
        gradient.setColorAt(0, QColor(60, 60, 120, 200))  # Dark blue
        gradient.setColorAt(0.5, QColor(80, 80, 140, 180))  # Medium blue
        gradient.setColorAt(1, QColor(100, 100, 160, 160))  # Light blue
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QColor(40, 40, 80, 220))
        
        # Draw main shape
        painter.drawPath(path)
        
        # Draw wing detail with different opacity
        painter.setBrush(QBrush(QColor(120, 120, 180, 100)))
        painter.drawPath(wing_path)
        
        painter.end()


class HomeScreen(QWidget):
    """Home screen widget with Peregrine logo and start button."""
    
    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Peregrine Speak")
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        
        # Set up gradient background
        self.setup_gradient_background()
        
        # Main layout - use absolute positioning for overlay effect
        main_widget = QWidget()
        main_widget.setParent(self)
        main_widget.resize(self.size())
        
        # Background logo that fills most of the screen
        self.logo_label = QLabel(main_widget)
        
        # Get the absolute path to the logo file
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent.parent
        logo_path = (project_root / "assets" / "icons" /
                     "peregrine_ai_logo.jpeg")
        
        print(f"Looking for logo at: {logo_path}")
        print(f"Logo file exists: {os.path.exists(logo_path)}")
        
        if os.path.exists(logo_path):
            self.original_pixmap = QPixmap(str(logo_path))
            print(f"Pixmap loaded: {not self.original_pixmap.isNull()}, " +
                  f"size: {self.original_pixmap.size()}")
            
            if not self.original_pixmap.isNull():
                # Scale the logo to fill most of the screen
                scaled_pixmap = self.original_pixmap.scaled(
                    700, 500,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.logo_label.setPixmap(scaled_pixmap)
                print("Logo image loaded successfully!")
            else:
                print("Failed to load pixmap from file")
                self.original_pixmap = None
                self.logo_label.setText("🦅")
                self.logo_label.setStyleSheet(
                    "font-size: 200px; color: rgba(255, 255, 255, 0.8);"
                )
        else:
            # Fallback if image not found
            print(f"Logo file not found at {logo_path}")
            self.original_pixmap = None
            self.logo_label.setText("🦅")
            self.logo_label.setStyleSheet(
                "font-size: 200px; color: rgba(255, 255, 255, 0.8);"
            )
        
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setGeometry(50, 50, 700, 500)
        
        # Welcome text overlay at the top
        self.welcome_label = TypewriterLabel("Welcome to Peregrine Speak")
        self.welcome_label.setParent(main_widget)
        self.welcome_label.setGeometry(0, 30, 800, 50)
        self.welcome_label.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 10px;
        """)
        
        # Start button overlay at the bottom
        self.start_button = QPushButton("Start", main_widget)
        self.start_button.setGeometry(350, 580, 200, 60)
        self.start_button.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.95);
                border: 2px solid rgba(100, 100, 100, 0.8);
                border-radius: 30px;
                font-size: 20px;
                font-weight: bold;
                color: #333;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 1.0);
                border: 2px solid rgba(80, 80, 80, 1.0);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: rgba(240, 240, 240, 1.0);
            }
        """)
        self.start_button.clicked.connect(self.on_start_clicked)
        
    def setup_gradient_background(self):
        """Set up the gradient background matching Peregrine colors."""
        self.setStyleSheet("""
            HomeScreen {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #a8e6cf,
                    stop: 0.5 #7fcdcd,
                    stop: 1 #6a5acd
                );
            }
        """)
        
    def setup_animations(self):
        """Set up fade and other animations."""
        # Opacity effect for fade transitions
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        # Fade animation
        self.fade_animation = QPropertyAnimation(
            self.opacity_effect, b"opacity"
        )
        self.fade_animation.setDuration(1000)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
    def showEvent(self, event):
        """Handle show event with fade in and typewriter animation."""
        super().showEvent(event)
        self.fade_in()
        
        # Start typewriter animation after a short delay
        QTimer.singleShot(1000, lambda: self.welcome_label.start_animation(80))
        
    def fade_in(self):
        """Fade in the home screen."""
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
        
    def fade_to_main_screen(self):
        """Fade out and transition to main screen."""
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.show_main_screen)
        self.fade_animation.start()
        
    def show_main_screen(self):
        """Show the main screen after fade out."""
        self.hide()
        self.app_instance.main_screen.show()
        self.fade_animation.finished.disconnect()
        
    def on_start_clicked(self):
        """Handle start button click."""
        self.app_instance.show_main_screen()
        
    def resizeEvent(self, event):
        """Handle window resize to maintain responsive layout."""
        super().resizeEvent(event)
        
        # Update positions and sizes based on new window size
        width = self.width()
        height = self.height()
        
        # Logo takes up most of the screen
        logo_margin = 50
        logo_width = width - (2 * logo_margin)
        logo_height = height - 150  # Leave space for text and button
        
        self.logo_label.setGeometry(logo_margin, 80, logo_width, logo_height)
        
        # Welcome text at the top
        self.welcome_label.setGeometry(50, 20, width - 100, 50)
        
        # Start button at the bottom center
        button_width = 200
        button_x = (width - button_width) // 2
        button_y = height - 80
        self.start_button.setGeometry(button_x, button_y, button_width, 60)
        
        # Re-scale the logo image if needed
        if hasattr(self, 'original_pixmap') and self.original_pixmap:
            scaled_pixmap = self.original_pixmap.scaled(
                logo_width - 50, logo_height - 50,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled_pixmap)
