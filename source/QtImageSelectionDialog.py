from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidgetItem, QLabel, QApplication, QCheckBox, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt

class QtImageSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Images")

        self.lblMessage = QLabel("Select your new generated images:")
        self.lstImages = QListWidget()
        self.lstImages.setIconSize(QSize(300, 300))  # Set the icon size for the list items
        self.lstImages.setSelectionMode(QListWidget.NoSelection)  # Disable item selection
        self.lstImages.setResizeMode(QListWidget.Adjust)  # Adjust the size of the items to fit the window
        self.lstImages.setViewMode(QListWidget.IconMode)  # Set the view mode to icon mode
        self.lstImages.setMovement(QListWidget.Static)  # Disable item movement
        self.lstImages.setSpacing(20)  # Set spacing between items
        self.btnOK = QPushButton("OK")
        self.btnCancel = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.addWidget(self.lblMessage)
        layout.addWidget(self.lstImages)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.btnOK)
        buttonLayout.addWidget(self.btnCancel)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        self.btnOK.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)

        screen_geometry = QApplication.desktop().availableGeometry()
        self.resize(screen_geometry.width() * 0.6, screen_geometry.height() * 0.6)

        self.image_id_counter = 1

    def addImage(self, image_path):
        item_widget = QWidget()
        layout = QHBoxLayout(item_widget)

        checkbox = QCheckBox()
        checkbox.setChecked(False)
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
            }
        """)  # Increase the size of the checkbox indicator

        image_label = QLabel()
        pixmap = QPixmap(image_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)

        image_id_label = QLabel(str(self.image_id_counter))
        image_id_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(checkbox)
        layout.addWidget(image_label)
        layout.addWidget(image_id_label)
        layout.setAlignment(checkbox, Qt.AlignCenter)  # Align the checkbox vertically centered
        layout.setContentsMargins(10, 0, 0, 0)  # Adjust the left margin to bring the checkbox closer to the image

        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        item.setData(Qt.UserRole, (self.image_id_counter, image_path))  # Store the image ID and path as user data

        self.lstImages.addItem(item)
        self.lstImages.setItemWidget(item, item_widget)

        self.image_id_counter += 1

    def getSelectedImages(self):
        selected_image_ids = []
        for i in range(self.lstImages.count()):
            item = self.lstImages.item(i)
            item_widget = self.lstImages.itemWidget(item)
            checkbox = item_widget.findChild(QCheckBox)
            if checkbox.isChecked():
                image_id, _ = item.data(Qt.UserRole)  # Retrieve only the image ID
                selected_image_ids.append(image_id)
        return selected_image_ids
