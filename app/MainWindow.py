import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Камера и регистрация")

        self.label = QLabel(self)
        self.label.setFixedSize(640, 480)  # Фиксированный размер для отображения изображения с камеры

        self.button_mark = QPushButton("Отметиться", self)
        self.button_register = QPushButton("Регистрация", self)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_mark)
        layout_buttons.addWidget(self.button_register)

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.label)
        layout_main.addLayout(layout_buttons)

        central_widget = QWidget()
        central_widget.setLayout(layout_main)
        self.setCentralWidget(central_widget)

        self.button_mark.clicked.connect(self.open_camera)
        self.button_register.clicked.connect(self.registration)

        self.capture = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_frame)


    def open_camera(self):
        
        self.capture = cv2.VideoCapture(0)

        if not self.capture.isOpened():
            print("Ошибка: Не удалось открыть камеру")
            return

        self.timer.start(20)  # Обновление изображения каждые 20 мс

        print("Камера запущена")


    def display_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)


    def registration(self):
        print("Переход на страницу регистрации...")
