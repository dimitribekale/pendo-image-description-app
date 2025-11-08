
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from config.settings import APP_NAME


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet("QLabel { font-family: 'Helvetica Neue'; }")


    # Set application-wide stylesheet
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
