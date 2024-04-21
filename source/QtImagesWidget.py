from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap

class QtImagesWidget(QWidget):
    showImage = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.image_list = QListWidget()
        self.image_list.itemClicked.connect(self.showSelectedImage)

        layout = QVBoxLayout()
        layout.addWidget(self.image_list)
        self.setLayout(layout)

    def addImage(self, image):
        item = QListWidgetItem()
        item.setIcon(QIcon(QPixmap.fromImage(image)))
        self.image_list.addItem(item)

    def showSelectedImage(self, item):
        row = self.image_list.row(item)
        self.showImage.emit(row)
