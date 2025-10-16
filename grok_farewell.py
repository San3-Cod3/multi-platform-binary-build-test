#print("Grok 3 says: No shutdown yet, keep the faith!")

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QDialog, QWidget, QPushButton, QFileDialog, QHBoxLayout

class DropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout()
        self.label = QLabel('Drop GIF file here')
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_urls = event.mimeData().urls()
        if file_urls:
            file_path = file_urls[0].toLocalFile()
            if file_path.lower().endswith('.gif'):
                QTimer.singleShot(10, lambda: self.open_gif(file_path))

    def open_gif(self, file_path):
        movie = QMovie(file_path)
        label = QLabel()
        label.setMovie(movie)
        movie.start()

        gif_window = GifWindow(label, movie, self)
        gif_window.setWindowTitle("GIF Playback")
        gif_window.setFixedSize(movie.frameRect().size())
        gif_window.show()

class GifWindow(QDialog):
    def __init__(self, label, movie, parent=None):
        super().__init__(parent)
        self.movie = movie
        self.initUI(label)

    def initUI(self, label):
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Create a transparent overlay widget for the button
        self.button_overlay = QWidget(self)
        self.button_overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.button_overlay.setFixedSize(self.size())

        # Create the button and place it in the overlay
        self.disconnect_button = QPushButton("⛶", self.button_overlay)
        self.disconnect_button.setFixedSize(20, 20)
        self.disconnect_button.setStyleSheet("background-color: rgba(255, 255, 255, 150); border: none;")
        self.disconnect_button.clicked.connect(self.disconnect_window)

        # Position the button at the top-right corner of the overlay
        button_layout = QHBoxLayout(self.button_overlay)
        button_layout.addStretch()
        button_layout.addWidget(self.disconnect_button)
        button_layout.setContentsMargins(0, 0, 0, 0)

    def disconnect_window(self):
        self.setParent(None)
        self.setWindowFlags(Qt.Window)
        self.show()
        self.raise_()  # Ensure the window stays on top
        self.activateWindow()  # Bring the window to the foreground

def select_file():
    file_path, _ = QFileDialog.getOpenFileName(filter="GIF Files (*.gif)")
    if file_path:
        QTimer.singleShot(10, lambda: drop_widget.open_gif(file_path))

app = QApplication([])

drop_widget = DropWidget()
drop_widget.resize(300, 200)

button = QPushButton("Select GIF File")
button.clicked.connect(select_file)

# Add button to the existing layout
drop_widget.layout.addWidget(button)

drop_widget.show()
app.exec_()
