from PyQt6.QtWidgets import QLabel, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from pathlib import Path

from config.settings import SUPPORTED_FORMATS
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QFileDialog


class DropZone(QLabel):
    """Custom QLabel that accepts drag and drop for images"""
    image_dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(400)
        self.setup_ui()

    def setup_ui(self):
        """Setup the minimalist drop zone appearance"""
        self.setText(
            "Drop image here\n\n"
            "or click to browse"
        )
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed rgba(148, 163, 184, 0.3);
                border-radius: 16px;
                background: rgba(15, 23, 42, 0.4);
                color: #94a3b8;
                font-size: 16px;
                font-weight: 400;
                padding: 50px;
            }
            QLabel:hover {
                border: 2px dashed rgba(96, 165, 250, 0.5);
                background: rgba(30, 41, 59, 0.5);
                color: #cbd5e1;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QLabel {
                    border: 2px solid rgba(96, 165, 250, 0.6);
                    border-radius: 16px;
                    background: rgba(96, 165, 250, 0.1);
                    color: #e2e8f0;
                    font-size: 16px;
                    font-weight: 500;
                    padding: 50px;
                }
            """)

    def dragLeaveEvent(self, event):
        """Handle drag leave event"""
        self.setup_ui()

    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        self.setup_ui()
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            file_path = files[0]
            if Path(file_path).suffix.lower() in SUPPORTED_FORMATS:
                self.image_dropped.emit(file_path)
            else:
                self.setText("Unsupported file format!\n\nPlease drop an image file.")

    def mousePressEvent(self, event):
        """Handle mouse click to open file dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            f"Images (*{' *'.join(SUPPORTED_FORMATS)})"
        )
        if file_path:
            self.image_dropped.emit(file_path)