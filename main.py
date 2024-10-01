import sys
import os
import subprocess
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtGui import QGuiApplication


class CustomExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Remove window title bar (but not staying on top of all windows)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()  # Make window full screen

    def initUI(self):
        self.setWindowTitle('Custom Explorer')

        layout = QVBoxLayout()

        # Add buttons for different functionalities
        open_file_explorer_button = QPushButton('Open File Explorer', self)
        open_file_explorer_button.clicked.connect(self.open_file_explorer)

        open_file_chrome_button = QPushButton('Open Chrome', self)
        open_file_chrome_button.clicked.connect(self.open_file_chrome)

        open_file_note_button = QPushButton('Open Notepad', self)
        open_file_note_button.clicked.connect(self.open_file_note)

        shutdown_button = QPushButton('Shutdown System', self)
        shutdown_button.clicked.connect(self.shutdown_system)

        restart_button = QPushButton('Restart System', self)
        restart_button.clicked.connect(self.restart_system)

        layout.addWidget(QLabel("Welcome to Custom Explorer", self))
        layout.addWidget(open_file_explorer_button)
        layout.addWidget(open_file_note_button)
        layout.addWidget(open_file_chrome_button)
        layout.addWidget(shutdown_button)
        layout.addWidget(restart_button)

        self.setLayout(layout)

    def open_file_explorer(self):
        # Open the default Windows file explorer
        subprocess.Popen('explorer')

    def open_file_note(self):
        # Open Notepad
        subprocess.Popen('notepad')


    def open_file_chrome(self):
        # Open Chrome
        subprocess.Popen(os.path.join(os.getenv('PROGRAMFILES(X86)'), 'Google/Chrome/Application/chrome.exe'))

    def shutdown_system(self):
        # Confirm before shutdown
        reply = QMessageBox.question(self, 'Confirm Shutdown', 'Are you sure you want to shut down the system?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            subprocess.Popen('shutdown /s /t 0')

    def restart_system(self):
        # Confirm before restart
        reply = QMessageBox.question(self, 'Confirm Restart', 'Are you sure you want to restart the system?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            subprocess.Popen('shutdown /r /t 0')

    def closeEvent(self, event):
        # Prevent closing the window (even with Alt+F4)
        event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomExplorer()
    window.show()
    sys.exit(app.exec())
