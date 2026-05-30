import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bramble Test')
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: white; color: black;")
        
        layout = QVBoxLayout()
        label = QLabel("If you see this, Bramble is alive!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn = QPushButton("Close Test")
        btn.clicked.connect(self.close)
        
        layout.addWidget(label)
        layout.addWidget(btn)
        self.setLayout(layout)

if __name__ == '__main__':
    # Force Wayland (COSMIC) environment
    os.environ["QT_QPA_PLATFORM"] = "wayland"
    
    app = QApplication(sys.argv)
    print("Starting Bramble Test Window...")
    
    gui = TestWindow()
    gui.show()
    
    print("Window should be visible now. Press Ctrl+C in terminal to kill if not.")
    sys.exit(app.exec())