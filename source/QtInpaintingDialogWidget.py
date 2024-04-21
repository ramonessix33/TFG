from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from io import BytesIO
from source.Inpainting import Inpainting
from source.QtImageSelectionDialog import QtImageSelectionDialog

class InpaintingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Inpainting Parameters")
        self.setGeometry(100, 100, 400, 300)

        self.prompt_label = QLabel("Prompt:")
        self.prompt_input = QLineEdit("catalan romanesque mural paintings, apses of the church of sant quirze de pedret")

        self.num_images_label = QLabel("Number of Images:")
        self.num_images_input = QLineEdit("3")

        self.advanced_button = QPushButton("Advanced Options")
        self.advanced_button.clicked.connect(self.toggleAdvancedOptions)

        self.advanced_options = QWidget()
        self.advanced_options.setVisible(False)

        self.negative_prompt_label = QLabel("Negative Prompt:")
        self.negative_prompt_input = QLineEdit("deformed face")

        self.inference_steps_label = QLabel("Number of Inference Steps:")
        self.inference_steps_input = QLineEdit("30")

        self.strength_label = QLabel("Strength:")
        self.strength_input = QLineEdit("0.99")

        self.guidance_scale_label = QLabel("Guidance Scale:")
        self.guidance_scale_input = QLineEdit("11")

        self.manual_seed_label = QLabel("Manual Seed:")
        self.manual_seed_input = QLineEdit("-1")

        # Set tooltips for parameter input fields
        self.setStyleSheet("""
            QToolTip {
                background-color: #000000;
                color: #FFFFFF;
                border: 1px solid #FFFFFF;
                padding: 5px;
            }
        """)
        self.prompt_input.setToolTip("Enter the prompt for the image generation.")
        self.num_images_input.setToolTip("Specify the number of images to generate.")
        self.negative_prompt_input.setToolTip("Enter the negative prompt to guide the image generation.")
        self.inference_steps_input.setToolTip("Specify the level of detail in the generated image. A value between 15 and 50 is recommended. Higher values generally produce more detailed images but also increase computation time.")
        self.strength_input.setToolTip("Control the intensity of the inpainting effect. A lower value (closer to 0) will apply subtle changes, while a higher value (closer to 1) will make more significant modifications.")
        self.guidance_scale_input.setToolTip("Determine how closely the generated image should follow the provided prompt. A value between 3 and 15 is suggested. Increasing the value prioritizes prompt adherence over image quality.")
        self.manual_seed_input.setToolTip("Specify a manual seed for reproducibility. Use -1 for random seed. Use positive integers.")

        advanced_layout = QVBoxLayout()
        advanced_layout.addWidget(self.negative_prompt_label)
        advanced_layout.addWidget(self.negative_prompt_input)
        advanced_layout.addWidget(self.inference_steps_label)
        advanced_layout.addWidget(self.inference_steps_input)
        advanced_layout.addWidget(self.strength_label)
        advanced_layout.addWidget(self.strength_input)
        advanced_layout.addWidget(self.guidance_scale_label)
        advanced_layout.addWidget(self.guidance_scale_input)
        advanced_layout.addWidget(self.manual_seed_label)
        advanced_layout.addWidget(self.manual_seed_input)
        self.advanced_options.setLayout(advanced_layout)

        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.createImages)
        self.back_button = QPushButton("Go Back")
        self.back_button.clicked.connect(self.reject)
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.back_button)

        layout = QVBoxLayout()
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(self.num_images_label)
        layout.addWidget(self.num_images_input)
        layout.addWidget(self.advanced_button)
        layout.addWidget(self.advanced_options)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.Inpainting = Inpainting(self)

    def toggleAdvancedOptions(self):
        self.advanced_options.setVisible(not self.advanced_options.isVisible())

    def createImages(self):
        prompt = self.prompt_input.text()
        num_images = int(self.num_images_input.text())
        negative_prompt = self.negative_prompt_input.text()
        image = self.parent.getImageDiff()
        mask_image = self.parent.getLabelBinaryImage()
        inference_steps = int(self.inference_steps_input.text())
        strength = float(self.strength_input.text())
        guidance_scale = float(self.guidance_scale_input.text())
        manual_seed = int(self.manual_seed_input.text())

        parameters = {
            "prompt": prompt,
            "num_images": num_images,
            "negative_prompt": negative_prompt,
            "image": image,
            "mask_image": mask_image,
            "inference_steps": inference_steps,
            "strength": strength,
            "guidance_scale": guidance_scale,
            "manual_seed": manual_seed
        }

        generated_images = self.Inpainting.paint(parameters = parameters)

        # Create a dictionary to store the image ID and corresponding QImage
        image_dict = {}

        # Display a new dialog and wait for user interaction
        dialog = QtImageSelectionDialog(self)
        for i, image in enumerate(generated_images, start=1):
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            qimage = QImage.fromData(buffer.getvalue())

            # Convert QImage to QPixmap
            qpixmap = QPixmap.fromImage(qimage)

            # Add the pixmap to the dialog
            dialog.addImage(qpixmap)

            # Store the QImage in the dictionary with the corresponding image ID
            image_dict[i] = qimage

        if dialog.exec_() == QDialog.Accepted:
            selected_image_ids = dialog.getSelectedImages()
            selected_images = [image_dict[image_id] for image_id in selected_image_ids]
            self.parent.addImagesToImagesWidget(selected_images)
        else:
            pass

        self.accept()
