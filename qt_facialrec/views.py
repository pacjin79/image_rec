import numpy as np
import cv2
from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QSlider, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage



class StartWindow(QMainWindow):
    def __init__(self, camera=None):
        super().__init__()
        self.camera = camera
        self.central_widget = QWidget()
        self.button_movie = QPushButton('Start Warren AR', self.central_widget)
        self.image_holder = QLabel(self)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_movie)
        self.layout.addWidget(self.image_holder)
        self.setCentralWidget(self.central_widget)

        # self.button_frame.clicked.connect(self.capture_frames)
        # self.button_movie.clicked.connect(self.start_movie)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.capture_frames)

        self.start_movie()

    def capture_frames(self):
        frame = self.camera.get_frame_with_face_rec()
        img = QImage(frame, frame.shape[1], frame.shape[0],
                     QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        pix = pix.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_holder.setPixmap(pix)

    def start_movie(self):
        self.movie_thread = MovieThread(self.camera)
        self.movie_thread.start()
        self.update_timer.start(60)

class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(200)