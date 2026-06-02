import sys
import subprocess
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QProgressBar, QLabel, QPushButton, QStackedWidget)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

# --- BACKEND THREAD ---
class HardwareWorker(QThread):
    finished = pyqtSignal()
    def run(self):
        local_script = "./bramble-hw.sh"
        system_script = "/usr/local/bin/bramble-hw.sh"
        target = system_script if os.path.exists(system_script) else local_script
        if os.path.exists(target):
            subprocess.run(["bash", target])
        else:
            self.msleep(2000) 
        self.finished.emit()

# --- MAIN UI ---
class BrambleWelcome(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('BrambleOS Experience Selector')
        self.setFixedSize(1000, 650)
        self.setStyleSheet("background-color: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif;")

        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_init_screen())
        self.stack.addWidget(self.create_experience_screen())
        self.stack.addWidget(self.create_browser_screen())

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.worker = HardwareWorker()
        self.worker.finished.connect(lambda: self.stack.setCurrentIndex(1))
        self.worker.start()

    def create_init_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        lbl = QLabel("Optimizing BrambleOS for your hardware...")
        lbl.setStyleSheet("font-size: 22px; margin-top: 200px;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pbar = QProgressBar()
        self.pbar.setRange(0, 0)
        self.pbar.setStyleSheet("QProgressBar::chunk { background: #10b981; }")
        layout.addWidget(lbl)
        layout.addWidget(self.pbar)
        layout.addStretch()
        return screen

    def create_experience_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        
        title = QLabel("Choose Your Experience")
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-top: 30px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        cards_layout = QHBoxLayout()
        # Option 1: COSMIC
        cards_layout.addWidget(self.create_card("The Future", "COSMIC Desktop\n(Modern Rust)", "#a855f7", "cosmic"))
        # Option 2: Win (KDE)
        cards_layout.addWidget(self.create_card("The Classic", "Bramble-Win\n(Familiar KDE)", "#3b82f6", "windows"))
        # Option 3: Mac (KDE)
        cards_layout.addWidget(self.create_card("The Creative", "Bramble-Mac\n(Sleek KDE)", "#94a3b8", "mac"))
        
        layout.addLayout(cards_layout)
        layout.addStretch()
        return screen

    def create_browser_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        title = QLabel("Final Step: Essential Software")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin: 30px;")
        
        browser_layout = QHBoxLayout()
        browser_layout.addWidget(self.create_card("Zen", "Optimized", "#a855f7", "zen"))
        browser_layout.addWidget(self.create_card("Firefox", "Privacy", "#f97316", "firefox"))
        browser_layout.addWidget(self.create_card("Brave", "Secure", "#ef4444", "brave"))
        
        layout.addWidget(title)
        layout.addLayout(browser_layout)
        
        finish = QPushButton("Launch BrambleOS")
        finish.setStyleSheet("background: #10b981; padding: 20px; font-size: 20px; font-weight: bold; border-radius: 10px;")
        finish.clicked.connect(self.close)
        layout.addWidget(finish, alignment=Qt.AlignmentFlag.AlignCenter)
        return screen

    def create_card(self, title, desc, color, action_id):
        btn = QPushButton(f"{title}\n{desc}")
        btn.setFixedSize(280, 220)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #1e293b;
                border: 2px solid #334155;
                border-radius: 20px;
                font-size: 18px;
            }}
            QPushButton:hover {{
                border: 3px solid {color};
                background-color: #334155;
            }}
        """)
        btn.clicked.connect(lambda: self.handle_action(action_id))
        return btn

    def handle_action(self, action_id):
        if action_id == "cosmic":
            # Switch to COSMIC session
            print("Switching to COSMIC...")
            subprocess.Popen(["killall", "kwin_wayland"]) # Kill KDE
            subprocess.Popen(["cosmic-session"])         # Start COSMIC
        elif action_id == "windows":
            subprocess.run(["lookandfeeltool", "-a", "org.kde.breeze.desktop"])
            self.stack.setCurrentIndex(2)
        elif action_id == "mac":
            # For now using Dark Breeze as placeholder for Mac
            subprocess.run(["lookandfeeltool", "-a", "org.kde.breezedark.desktop"])
            self.stack.setCurrentIndex(2)
        else:
            # Browser installs
            print(f"Installing {action_id}...")
            self.stack.setCurrentIndex(2)

if __name__ == '__main__':
    os.environ["QT_QPA_PLATFORM"] = "wayland"
    app = QApplication(sys.argv)
    window = BrambleWelcome()
    window.show()
    sys.exit(app.exec())