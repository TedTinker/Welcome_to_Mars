import os 
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSlot
from default_window import DefaultWindow, button_style

class CharacterWindow(DefaultWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Character Window')

        # Layout for Fate Points and Refresh
        fate_refresh_layout = QHBoxLayout()
        self.layout.addLayout(fate_refresh_layout)
        
        # Fate Points input
        fate_refresh_layout.addWidget(QLabel('Fate Points'))
        self.fate_points_input = QLineEdit(self)
        self.fate_points_input.setText('3')
        fate_refresh_layout.addWidget(self.fate_points_input)
        
        # Refresh input
        fate_refresh_layout.addWidget(QLabel('Refresh'))
        self.refresh_input = QLineEdit(self)
        self.refresh_input.setText('3')
        fate_refresh_layout.addWidget(self.refresh_input)
        
        # Layout for Approaches
        skills_layout = QVBoxLayout()
        self.layout.addLayout(skills_layout)
        
        # Header for Approaches
        skills_header_layout = QHBoxLayout()
        skills_layout.addLayout(skills_header_layout)
        
        skills_header_layout.addWidget(QLabel('Careful'))
        skills_header_layout.addWidget(QLabel('Clever'))
        skills_header_layout.addWidget(QLabel('Flashy'))
        skills_header_layout.addWidget(QLabel('Forceful'))
        skills_header_layout.addWidget(QLabel('Quick'))
        skills_header_layout.addWidget(QLabel('Sneaky'))
        
        # Input fields for Approaches
        skills_inputs_layout = QHBoxLayout()
        skills_layout.addLayout(skills_inputs_layout)
        
        self.careful_input = QLineEdit(self)
        self.careful_input.setText('0')
        skills_inputs_layout.addWidget(self.careful_input)
        
        self.clever_input = QLineEdit(self)
        self.clever_input.setText('0')
        skills_inputs_layout.addWidget(self.clever_input)
        
        self.flashy_input = QLineEdit(self)
        self.flashy_input.setText('0')
        skills_inputs_layout.addWidget(self.flashy_input)
        
        self.forceful_input = QLineEdit(self)
        self.forceful_input.setText('0')
        skills_inputs_layout.addWidget(self.forceful_input)
        
        self.quick_input = QLineEdit(self)
        self.quick_input.setText('0')
        skills_inputs_layout.addWidget(self.quick_input)
        
        self.sneaky_input = QLineEdit(self)
        self.sneaky_input.setText('0')
        skills_inputs_layout.addWidget(self.sneaky_input)
        
        # Layout for Aspects
        aspects_layout = QVBoxLayout()
        self.layout.addLayout(aspects_layout)
        
        aspects_layout.addWidget(QLabel('Aspects:'))
        
        # High Concept input
        high_concept_layout = QHBoxLayout()
        aspects_layout.addLayout(high_concept_layout)
        high_concept_layout.addWidget(QLabel('High Concept'))
        self.high_concept_input = QLineEdit(self)
        high_concept_layout.addWidget(self.high_concept_input)
        
        # Trouble input
        trouble_layout = QHBoxLayout()
        aspects_layout.addLayout(trouble_layout)
        trouble_layout.addWidget(QLabel('Trouble'))
        self.trouble_input = QLineEdit(self)
        trouble_layout.addWidget(self.trouble_input)

        # Additional Aspects
        self.aspects_list_layout = QVBoxLayout()
        aspects_layout.addLayout(self.aspects_list_layout)
        
        # Button to add a new aspect
        self.add_aspect_button = QPushButton('New Aspect', self)
        button_style(self.add_aspect_button)
        self.add_aspect_button.clicked.connect(self.add_aspect)
        aspects_layout.addWidget(self.add_aspect_button)
        
        # Layout for Stunts
        stunts_layout = QVBoxLayout()
        self.layout.addLayout(stunts_layout)
        
        stunts_layout.addWidget(QLabel('Stunts:'))
        
        # List of Stunts
        self.stunts_list_layout = QVBoxLayout()
        stunts_layout.addLayout(self.stunts_list_layout)
        
        # Button to add a new stunt
        self.add_stunt_button = QPushButton('New Stunt', self)
        button_style(self.add_stunt_button)
        self.add_stunt_button.clicked.connect(self.add_stunt)
        stunts_layout.addWidget(self.add_stunt_button)
        
        # Re-add the toggle button and notes/image layout
        self.notes_toggle_button.setParent(None)
        self.notes_image_layout.setParent(None)

        self.layout.addWidget(self.notes_toggle_button)
        self.layout.addLayout(self.notes_image_layout)

        # Show the notes and image by default
        self.notes_input.setVisible(True)
        self.image_label.setVisible(True)
        self.choose_image_button.setVisible(True)
        self.notes_toggle_button.setText('Hide Notes and Image')

    # Add a new aspect
    def add_aspect(self):
        aspect_layout = QHBoxLayout()
        
        aspect_input = QLineEdit(self)
        aspect_layout.addWidget(aspect_input)
        
        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_aspect(aspect_layout))
        aspect_layout.addWidget(remove_button)
        
        self.aspects_list_layout.addLayout(aspect_layout)
    
    # Remove an aspect
    def remove_aspect(self, aspect_layout):
        for i in reversed(range(aspect_layout.count())):
            widget = aspect_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.aspects_list_layout.removeItem(aspect_layout)
    
    # Add a new stunt
    def add_stunt(self):
        stunt_layout = QHBoxLayout()
        
        stunt_input = QLineEdit(self)
        stunt_layout.addWidget(stunt_input)
        
        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_stunt(stunt_layout))
        stunt_layout.addWidget(remove_button)
        
        self.stunts_list_layout.addLayout(stunt_layout)
    
    # Remove a stunt
    def remove_stunt(self, stunt_layout):
        for i in reversed(range(stunt_layout.count())):
            widget = stunt_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.stunts_list_layout.removeItem(stunt_layout)

    # Toggle visibility of notes and image section
    def toggle_notes(self):
        visible = not self.notes_input.isVisible()
        self.notes_input.setVisible(visible)
        self.image_label.setVisible(visible)
        self.choose_image_button.setVisible(visible)
        self.notes_toggle_button.setText('Hide Notes and Image' if visible else 'Show Notes and Image')

    # Choose an image
    @pyqtSlot()
    def choose_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "pictures", "Image Files (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

    # Save contents to a file
    def save_contents(self, suppress_message=False):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, 'Warning', 'Name cannot be empty!')
            return
        
        os.makedirs("saved", exist_ok=True)
        file_path = os.path.join("saved", f"{name}.txt")
        
        with open(file_path, 'w') as file:
            file.write(f"WindowType: CharacterWindow\n")
            file.write(f"Name: {name}\n")
            file.write(f"Fate Points: {self.fate_points_input.text()}\n")
            file.write(f"Refresh: {self.refresh_input.text()}\n")
            file.write(f"Careful: {self.careful_input.text()}\n")
            file.write(f"Clever: {self.clever_input.text()}\n")
            file.write(f"Flashy: {self.flashy_input.text()}\n")
            file.write(f"Forceful: {self.forceful_input.text()}\n")
            file.write(f"Quick: {self.quick_input.text()}\n")
            file.write(f"Sneaky: {self.sneaky_input.text()}\n")
            
            file.write(f"High Concept: {self.high_concept_input.text()}\n")
            file.write(f"Trouble: {self.trouble_input.text()}\n")
            
            for i in range(self.aspects_list_layout.count()):
                aspect_layout = self.aspects_list_layout.itemAt(i).layout()
                if aspect_layout:
                    aspect_input = aspect_layout.itemAt(0).widget()
                    file.write(f"Aspect: {aspect_input.text()}\n")
            
            for i in range(self.stunts_list_layout.count()):
                stunt_layout = self.stunts_list_layout.itemAt(i).layout()
                if stunt_layout:
                    stunt_input = stunt_layout.itemAt(0).widget()
                    file.write(f"Stunt: {stunt_input.text()}\n")

            file.write(f"Notes: {self.notes_input.toPlainText()}\n")
            file.write(f"ImagePath: {self.image_path}\n")
        
        if not suppress_message:
            QMessageBox.information(self, 'Info', f'Contents saved to {name}.txt')

    # Load contents from a file
    def load_contents(self, file_path):
        self.clear_layout(self.aspects_list_layout)
        self.clear_layout(self.stunts_list_layout)
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.name_input.setText(lines[1].split(": ")[1].strip())
            self.fate_points_input.setText(lines[2].split(": ")[1].strip())
            self.refresh_input.setText(lines[3].split(": ")[1].strip())
            self.careful_input.setText(lines[4].split(": ")[1].strip())
            self.clever_input.setText(lines[5].split(": ")[1].strip())
            self.flashy_input.setText(lines[6].split(": ")[1].strip())
            self.forceful_input.setText(lines[7].split(": ")[1].strip())
            self.quick_input.setText(lines[8].split(": ")[1].strip())
            self.sneaky_input.setText(lines[9].split(": ")[1].strip())
            self.high_concept_input.setText(lines[10].split(": ")[1].strip())
            self.trouble_input.setText(lines[11].split(": ")[1].strip())
            
            for line in lines[12:-2]:
                if line.startswith("Aspect:"):
                    aspect_text = line.split(": ")[1].strip()
                    self.add_aspect_with_text(aspect_text)
                elif line.startswith("Stunt:"):
                    stunt_text = line.split(": ")[1].strip()
                    self.add_stunt_with_text(stunt_text)

            self.notes_input.setPlainText(lines[-2].split(": ", 1)[1].strip())
            self.image_path = lines[-1].split(": ", 1)[1].strip()
            if self.image_path:
                pixmap = QPixmap(self.image_path)
                self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

    # Clear a layout
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    # Add an aspect with text
    def add_aspect_with_text(self, text):
        aspect_layout = QHBoxLayout()
        
        aspect_input = QLineEdit(self)
        aspect_input.setText(text)
        aspect_layout.addWidget(aspect_input)
        
        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_aspect(aspect_layout))
        aspect_layout.addWidget(remove_button)
        
        self.aspects_list_layout.addLayout(aspect_layout)

    # Add a stunt with text
    def add_stunt_with_text(self, text):
        stunt_layout = QHBoxLayout()
        
        stunt_input = QLineEdit(self)
        stunt_input.setText(text)
        stunt_layout.addWidget(stunt_input)
        
        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_stunt(stunt_layout))
        stunt_layout.addWidget(remove_button)
        
        self.stunts_list_layout.addLayout(stunt_layout)
