import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QTextEdit, QLabel, QFileDialog
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap

# Apply a consistent button style
def button_style(button):
    button.setStyleSheet("background-color: #888888; color: white;")

class DefaultWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Default Window')
        self.setGeometry(100, 100, 400, 200)
        
        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Name input layout
        self.name_layout = QHBoxLayout()
        self.layout.addLayout(self.name_layout)
        
        # Name input field
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Name')
        self.name_layout.addWidget(self.name_input)
        
        # Save button
        self.save_button = QPushButton('Save', self)
        button_style(self.save_button)
        self.save_button.clicked.connect(self.save_contents)
        self.name_layout.addWidget(self.save_button)
        
        # Toggle button for notes and image section
        self.notes_toggle_button = QPushButton('Show Notes and Image', self)
        button_style(self.notes_toggle_button)
        self.notes_toggle_button.clicked.connect(self.toggle_notes)
        self.layout.addWidget(self.notes_toggle_button)
        
        # Layout for notes and image section
        self.notes_image_layout = QHBoxLayout()
        
        # Notes input field
        self.notes_input = QTextEdit(self)
        self.notes_input.setPlaceholderText('Notes')
        self.notes_input.setVisible(False)  # Initially hidden
        self.notes_image_layout.addWidget(self.notes_input)

        # Layout for image and button
        self.image_button_layout = QVBoxLayout()
        
        # Image label
        self.image_label = QLabel(self)
        self.image_label.setVisible(False)  # Initially hidden
        self.image_button_layout.addWidget(self.image_label)

        # Button to choose an image
        self.choose_image_button = QPushButton('Choose Image', self)
        button_style(self.choose_image_button)
        self.choose_image_button.clicked.connect(self.choose_image)
        self.choose_image_button.setVisible(False)  # Initially hidden
        self.image_button_layout.addWidget(self.choose_image_button)
        
        # Add image button layout to the notes and image layout
        self.notes_image_layout.addLayout(self.image_button_layout)
        self.layout.addLayout(self.notes_image_layout)

        # Path to the selected image
        self.image_path = ""

    # Toggle visibility of notes and image section
    def toggle_notes(self):
        visible = not self.notes_input.isVisible()
        self.notes_input.setVisible(visible)
        self.image_label.setVisible(visible)
        self.choose_image_button.setVisible(visible)
        self.notes_toggle_button.setText('Hide Notes and Image' if visible else 'Show Notes and Image')
        
    # Slot to choose an image
    @pyqtSlot()
    def choose_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "pictures", "Image Files (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
    
    # Slot to save contents to a file
    @pyqtSlot()
    def save_contents(self, suppress_message=False):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, 'Warning', 'Name cannot be empty!')
            return
        
        os.makedirs("saved", exist_ok=True)
        file_path = os.path.join("saved", f"{name}.txt")
        
        with open(file_path, 'w') as file:
            file.write(f"Name: {name}\n")
            file.write(f"Notes: {self.notes_input.toPlainText()}\n")
            file.write(f"ImagePath: {self.image_path}\n")
        
        if not suppress_message:
            QMessageBox.information(self, 'Info', f'Contents saved to {name}.txt')
    
    # Load contents from a file
    def load_contents(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.name_input.setText(lines[0].split(": ")[1].strip())
            self.notes_input.setPlainText(lines[1].split(": ", 1)[1].strip())
            self.image_path = lines[2].split(": ", 1)[1].strip()
            if self.image_path:
                pixmap = QPixmap(self.image_path)
                self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
