import torch
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QSplitter
)
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QFont
from pathlib import Path

from config.settings import (
    APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT,
    MAX_IMAGE_SIZE, THUMBNAIL_SIZE, BASE_DIR, HUGGINGFACE_DEVICE
)
from .image_analyzer import ImageAnalyzerWorker
from src.services.image_service import ImageService
from .drop_zone import DropZone


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.current_image_path = None
        self.worker = None
        self.image_service = ImageService()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{APP_NAME} Image Analyzer")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Set app icon
        icon_path = BASE_DIR / 'assets' / 'icons' / 'icon.png'
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create header
        header = self.create_header()
        main_layout.addWidget(header)

        # Create splitter for main content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(2)

        # Left panel - Image display and drop zone
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Right panel - Analysis results
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        splitter.setSizes([500, 700])
        main_layout.addWidget(splitter)

        # Apply futuristic theme
        self.apply_theme()

    def create_header(self) -> QWidget:
        """Create minimalist futuristic header"""

        header = QWidget()
        header.setFixedHeight(70)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 10, 25, 10)

        # App icon and title container
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setSpacing(12)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Circular app icon
        icon_path = BASE_DIR / 'assets' / 'icons' / 'icon.png'
        if icon_path.exists():
            icon_label = QLabel()
            pixmap = QPixmap(str(icon_path))
            # Scale to 45x45 and make circular
            scaled_pixmap = pixmap.scaled(45, 45, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            # Create circular mask
            circular = QPixmap(45, 45)
            circular.fill(Qt.GlobalColor.transparent)
            painter = QPainter(circular)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(Qt.GlobalColor.white)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, 45, 45)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()

            icon_label.setPixmap(circular)

            title_layout.addWidget(icon_label)

        # App name with subtle, elegant styling
        title = QLabel(APP_NAME)
        title_font = QFont("SF Pro Display", 24, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                background: transparent;
                letter-spacing: 1px;
            }
        """)
        title_layout.addWidget(title)

        title_layout.addStretch()
        header_layout.addWidget(title_container)

        header_layout.addStretch()

        # Minimal status indicator (GPU only, no model name)
        device_text = ""
        device_color = "#10b981"
        try:
            if HUGGINGFACE_DEVICE == 'auto':
                if torch.backends.mps.is_available():
                    device_text = "GPU"
                    device_color = "#10b981"
                elif torch.cuda.is_available():
                    device_text = "GPU"
                    device_color = "#3b82f6"
                else:
                    device_text = "CPU"
                    device_color = "#64748b"
        except:
            device_text = "READY"
            device_color = "#64748b"

        device_label = QLabel(device_text)
        device_label.setStyleSheet(f"""
            QLabel {{
                color: {device_color};
                font-size: 10px;
                font-weight: 600;
                background: transparent;
                padding: 6px 14px;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                letter-spacing: 1px;
            }}
        """)
        header_layout.addWidget(device_label)

        # Minimal header background
        header.setStyleSheet("""
            QWidget {
                background: rgba(15, 23, 42, 0.95);
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)

        return header

    def create_left_panel(self) -> QWidget:
        """Create left panel with image display"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.image_dropped.connect(self.handle_image)
        layout.addWidget(self.drop_zone)

        # Image preview
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.hide()
        layout.addWidget(self.image_label)

        # Minimalist action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.clicked.connect(self.analyze_image)
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setFixedHeight(44)
        self.analyze_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background: rgba(96, 165, 250, 0.15);
                color: #60a5fa;
                border: 1px solid rgba(96, 165, 250, 0.3);
                padding: 12px 28px;
                border-radius: 22px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(96, 165, 250, 0.25);
                border-color: rgba(96, 165, 250, 0.5);
            }
            QPushButton:pressed {
                background: rgba(96, 165, 250, 0.35);
            }
            QPushButton:disabled {
                background: rgba(71, 85, 105, 0.1);
                border-color: rgba(71, 85, 105, 0.2);
                color: #64748b;
            }
        """)
        button_layout.addWidget(self.analyze_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_image)
        self.clear_btn.setEnabled(False)
        self.clear_btn.setFixedHeight(44)
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94a3b8;
                border: 1px solid rgba(148, 163, 184, 0.2);
                padding: 12px 28px;
                border-radius: 22px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: rgba(148, 163, 184, 0.1);
                border-color: rgba(148, 163, 184, 0.3);
                color: #cbd5e1;
            }
            QPushButton:pressed {
                background: rgba(148, 163, 184, 0.15);
            }
            QPushButton:disabled {
                background: transparent;
                border-color: rgba(71, 85, 105, 0.2);
                color: #475569;
            }
        """)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)

        return panel

    def create_right_panel(self) -> QWidget:
        """Create minimalist results panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Minimal results header
        results_header = QLabel("Results")
        results_header_font = QFont("SF Pro Display", 14, QFont.Weight.Medium)
        results_header.setFont(results_header_font)
        results_header.setStyleSheet("""
            QLabel {
                color: #94a3b8;
                background: transparent;
                padding: 8px 0px;
                letter-spacing: 0.5px;
            }
        """)
        layout.addWidget(results_header)

        # Minimalist results text area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText(
            "Ready to analyze.\n\n"
            "Drop an image and click Analyze to begin."
        )
        self.results_text.setStyleSheet("""
            QTextEdit {
                background: rgba(15, 23, 42, 0.4);
                color: #e2e8f0;
                border: 1px solid rgba(148, 163, 184, 0.15);
                border-radius: 12px;
                padding: 18px;
                font-size: 14px;
                line-height: 1.6;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTextEdit::placeholder {
                color: #64748b;
            }
            QScrollBar:vertical {
                background: rgba(30, 41, 59, 0.3);
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(96, 165, 250, 0.3);
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(96, 165, 250, 0.5);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        layout.addWidget(self.results_text)

        return panel

    def apply_theme(self):
        """Apply minimalist dark theme to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background: #0f172a;
            }
            QWidget {
                background: transparent;
                color: #f1f5f9;
            }
            QSplitter::handle {
                background: rgba(148, 163, 184, 0.1);
                width: 1px;
            }
            QSplitter::handle:hover {
                background: rgba(96, 165, 250, 0.3);
            }
        """)

    def handle_image(self, file_path: str):
        """Handle image selection/drop"""
        # Validate file size
        file_size = Path(file_path).stat().st_size
        if file_size > MAX_IMAGE_SIZE:
            self.results_text.setText(
                f"Error: File too large\n\n"
                f"Maximum size: {MAX_IMAGE_SIZE / (1024*1024):.1f}MB\n"
                f"Your file: {file_size / (1024*1024):.1f}MB"
            )
            return

        self.current_image_path = file_path

        # Load and display image
        pixmap = QPixmap(file_path)
        scaled_pixmap = pixmap.scaled(
            THUMBNAIL_SIZE[0],
            THUMBNAIL_SIZE[1],
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.show()
        self.drop_zone.hide()

        # Enable buttons
        self.analyze_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)

        # Update results
        self.results_text.setText(
            f"Image loaded\n\n"
            f"Size: {file_size / 1024:.1f} KB\n\n"
            f"Click Analyze to begin."
        )

    def analyze_image(self):
        """Analyze the current image using LLM"""
        if not self.current_image_path:
            return

        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("Analyzing...")
        self.results_text.setText("Analyzing image...\n\nPlease wait.")

        # Create and start worker thread
        self.worker = ImageAnalyzerWorker(self.current_image_path)
        self.worker.finished.connect(self.on_analysis_complete)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.start()

    def on_analysis_complete(self, result: str):
        """Handle analysis completion"""
        self.results_text.setText(f"{result}")
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("Analyze")

    def on_analysis_error(self, error: str):
        """Handle analysis error"""
        self.results_text.setText(
            f"Analysis error\n\n{error}\n\n"
            f"Check configuration in config/settings.py"
        )
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("Analyze")

    def clear_image(self):
        """Clear current image and reset UI"""
        self.current_image_path = None
        self.image_label.hide()
        self.drop_zone.show()
        self.drop_zone.setup_ui()
        self.analyze_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.results_text.clear()
        self.results_text.setPlaceholderText(
            "Ready to analyze.\n\n"
            "Drop an image and click Analyze to begin."
        )
