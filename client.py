import sys
import requests
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QPushButton
import subprocess

def start_server():
    subprocess.Popen(['python', 'server.py'])

class ClientWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Client")
        self.setGeometry(100, 100, 400, 400)

        # Создаем элементы интерфейса
        self.line_edit = QLineEdit(self)
        self.list_view = QListWidget(self)
        self.post_button = QPushButton("POST", self)
        self.get_button = QPushButton("GET", self)

        # Создаем Layout
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        # Добавляем элементы на форму
        v_layout.addWidget(self.line_edit)
        v_layout.addWidget(self.list_view)

        h_layout.addWidget(self.post_button)
        h_layout.addWidget(self.get_button)

        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

        # Обработка нажатия кнопок
        self.post_button.clicked.connect(self.send_post_request)
        self.get_button.clicked.connect(self.send_get_request)

    def send_post_request(self):
        # Формируем json-файл для отправки на сервер
        data = {
            "text": self.line_edit.text(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "click_number": self.list_view.count() + 1
        }

        # Отправляем POST запрос на сервер
        response = requests.post("http://127.0.0.1:5000/data", json=data)

        # Обрабатываем ответ сервера
        if response.status_code == 200:
            print("Данные успешно отправлены на сервер")
        else:
            print("Ошибка отправки данных на сервер")

    def send_get_request(self):
        # Отправляем GET запрос на сервер
        response = requests.get("http://127.0.0.1:5000/data")

        # Обрабатываем ответ сервера
        if response.status_code == 200:
            # Очищаем список
            self.list_view.clear()

            # Добавляем полученные данные в список
            for item in response.json():
                self.list_view.addItem(f"Text: {item['text']}, Date: {item['date']}, Time: {item['time']}, Click number: {item['click_number']}")
        else:
            print("Ошибка получения данных с сервера")


if __name__ == '__main__':
    start_server()
    app = QApplication(sys.argv)
    client_widget = ClientWidget()
    client_widget.show()
    sys.exit(app.exec())

