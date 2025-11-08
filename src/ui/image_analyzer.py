from PyQt6.QtCore import QThread, pyqtSignal
from src.services.llm_service import LLMService


class ImageAnalyzerWorker(QThread):
    """Worker thread for image analysis to keep UI responsive"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, image_path: str):
        super().__init__()
        self.image_path = image_path
        self.llm_service = LLMService()

    def run(self):
        try:
            result = self.llm_service.analyze_image(self.image_path)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))