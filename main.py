import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtWidgets import QMessageBox


class CustomExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # z-index of the window -1
        self.setWindowFlags(self.windowFlags() | 0x4000000)
        # full screen
        self.showFullScreen()

    def initUI(self):
        self.setWindowTitle('Custom Explorer')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Add buttons for different functionalities
        open_file_explorer_button = QPushButton('Open File Explorer', self)
        open_file_explorer_button.clicked.connect(self.open_file_explorer)

        open_file_note_button = QPushButton('Open File Note', self)
        open_file_note_button.clicked.connect(self.open_file_note)

        shutdown_button = QPushButton('Shutdown System', self)
        shutdown_button.clicked.connect(self.shutdown_system)

        restart_button = QPushButton('Restart System', self)
        restart_button.clicked.connect(self.restart_system)

        layout.addWidget(QLabel("Welcome to Custom Explorer", self))
        layout.addWidget(open_file_explorer_button)
        layout.addWidget(shutdown_button)
        layout.addWidget(restart_button)

        self.setLayout(layout)

    def open_file_explorer(self):
        # Open the default Windows file explorer
        subprocess.Popen('explorer')

    def open_file_note(self):
        # Open the default Windows file explorer
        subprocess.Popen('notepad')

    def shutdown_system(self):
        # Shutdown the system
        subprocess.Popen('shutdown /s /t 0')

    def restart_system(self):
        # Restart the system
        subprocess.Popen('shutdown /r /t 0')

    def closeEvent(self, event):
        event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomExplorer()
    window.show()
    sys.exit(app.exec())
