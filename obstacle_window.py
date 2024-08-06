import os
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QMessageBox, QFileDialog, QLabel
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from default_window import DefaultWindow, button_style

class ObstacleWindow(DefaultWindow):
    def __init__(self, add_default_rows=True):
        super().__init__()
        self.setWindowTitle('Obstacle Window')

        # Header layout for columns: Agent, Score, and Remove button
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Agent"))
        header_layout.addWidget(QLabel("Score"))
        header_layout.addWidget(QLabel(""))
        self.layout.addLayout(header_layout)

        # Layout for rows of obstacles
        self.rows_layout = QVBoxLayout()
        self.layout.addLayout(self.rows_layout)

        # Add default rows if specified
        if add_default_rows:
            self.add_row("Obstacle", "0")
            self.add_row("", "0")
        
        # Button to add a new row
        self.new_row_button = QPushButton('New Row', self)
        button_style(self.new_row_button)
        self.new_row_button.clicked.connect(lambda: self.add_row("", "0"))
        self.layout.addWidget(self.new_row_button)

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

    # Add a new row with agent and score
    def add_row(self, agent="Obstacle", score="0"):
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_widget.setLayout(row_layout)

        # Agent input
        agent_input = QLineEdit(self)
        agent_input.setText(agent)
        row_layout.addWidget(agent_input)

        # Score input
        score_input = QLineEdit(self)
        score_input.setText(score)
        row_layout.addWidget(score_input)

        # Remove button for the row
        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_row(row_widget))
        row_layout.addWidget(remove_button)

        self.rows_layout.addWidget(row_widget)

    # Remove a row
    def remove_row(self, row_widget):
        self.rows_layout.removeWidget(row_widget)
        row_widget.deleteLater()

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
            file.write(f"WindowType: ObstacleWindow\n")
            file.write(f"Name: {name}\n")
            for i in range(self.rows_layout.count()):
                row_widget = self.rows_layout.itemAt(i).widget()
                if row_widget:
                    agent_input = row_widget.layout().itemAt(0).widget()
                    score_input = row_widget.layout().itemAt(1).widget()
                    file.write(f"{agent_input.text()}:{score_input.text()}\n")
            file.write(f"Notes: {self.notes_input.toPlainText()}\n")
            file.write(f"ImagePath: {self.image_path}\n")
        
        if not suppress_message:
            QMessageBox.information(self, 'Info', f'Contents saved to {name}.txt')

    # Load contents from a file
    def load_contents(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.name_input.setText(lines[1].split(": ")[1].strip())
            for line in lines[2:-2]:
                agent, score = line.strip().split(':')
                self.add_row(agent, score)
            self.notes_input.setPlainText(lines[-2].split(": ", 1)[1].strip())
            self.image_path = lines[-1].split(": ", 1)[1].strip()
            if self.image_path:
                pixmap = QPixmap(self.image_path)
                self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
