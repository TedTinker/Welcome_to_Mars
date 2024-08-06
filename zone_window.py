import os
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QComboBox, QMessageBox, QMdiSubWindow, QFileDialog
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QPixmap
from default_window import DefaultWindow, button_style
from character_window import CharacterWindow
from obstacle_window import ObstacleWindow

class ZoneWindow(DefaultWindow):
    def __init__(self, mdi_area):
        super().__init__()
        self.setWindowTitle('Zone Window')

        self.mdi_area = mdi_area

        # Dropdown to select windows to add to the zone
        self.dropdown = QComboBox(self)
        self.dropdown.addItem("Select a window")
        self.dropdown.activated.connect(self.add_row_from_dropdown)
        self.layout.addWidget(self.dropdown)

        # Layout to hold rows of added windows
        self.rows_layout = QVBoxLayout()
        self.layout.addLayout(self.rows_layout)

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

        # Update the dropdown list and start the timer to refresh it
        self.update_dropdown()
        self.start_timer()

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

    # Start a timer to update the dropdown list periodically
    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dropdown)
        self.timer.start(2000)  # Update every 2 seconds

    # Update the dropdown list with the names of available windows
    def update_dropdown(self):
        current_names = set(self.get_all_row_names())
        all_window_names = [window.widget().name_input.text() for window in self.mdi_area.subWindowList() if window.widget().name_input.text() and window.widget() != self and not isinstance(window.widget(), ZoneWindow)]
        
        available_names = [name for name in all_window_names if name not in current_names]
        
        self.dropdown.blockSignals(True)
        self.dropdown.clear()
        self.dropdown.addItem("Select a window")
        self.dropdown.addItems(available_names)
        self.dropdown.blockSignals(False)

        self.cleanup_removed_windows(current_names)

    # Remove rows for windows that are no longer open
    def cleanup_removed_windows(self, current_names):
        all_window_names = {window.widget().name_input.text() for window in self.mdi_area.subWindowList() if window.widget().name_input.text()}
        for name in list(current_names):
            if name not in all_window_names:
                for i in range(self.rows_layout.count()):
                    row_widget = self.rows_layout.itemAt(i).widget()
                    if row_widget:
                        name_label = row_widget.layout().itemAt(0).widget()
                        if name_label.text() == name:
                            self.rows_layout.removeWidget(row_widget)
                            row_widget.deleteLater()

    # Add a row for a window selected from the dropdown
    def add_row_from_dropdown(self, index):
        if index == 0:  # Ignore the default index
            return
        
        window_name = self.dropdown.itemText(index)
        if window_name:
            self.add_row(window_name)
            self.dropdown.removeItem(index)

    # Add a row with the specified window name
    def add_row(self, window_name):
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_widget.setLayout(row_layout)

        name_label = QLineEdit(self)
        name_label.setText(window_name)
        name_label.setReadOnly(True)
        row_layout.addWidget(name_label)

        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_row(row_widget, window_name))
        row_layout.addWidget(remove_button)

        self.rows_layout.addWidget(row_widget)

    # Remove a row and update the dropdown
    def remove_row(self, row_widget, window_name):
        self.rows_layout.removeWidget(row_widget)
        row_widget.deleteLater()
        self.update_dropdown()

    # Get the names of all windows in the rows
    def get_all_row_names(self):
        names = []
        for i in range(self.rows_layout.count()):
            row_widget = self.rows_layout.itemAt(i).widget()
            if row_widget:
                name_label = row_widget.layout().itemAt(0).widget()
                names.append(name_label.text())
        return names

    # Save contents to a file
    def save_contents(self, suppress_message=False):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, 'Warning', 'Name cannot be empty!')
            return
        
        os.makedirs("saved", exist_ok=True)
        file_path = os.path.join("saved", f"{name}.txt")
        
        with open(file_path, 'w') as file:
            file.write(f"WindowType: ZoneWindow\n")
            file.write(f"Name: {name}\n")
            for i in range(self.rows_layout.count()):
                row_widget = self.rows_layout.itemAt(i).widget()
                if row_widget:
                    name_label = row_widget.layout().itemAt(0).widget()
                    file.write(f"{name_label.text()}\n")
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
                window_name = line.strip()
                if not self.is_window_open(window_name):
                    self.load_window(window_name)
                self.add_row(window_name)
            self.notes_input.setPlainText(lines[-2].split(": ", 1)[1].strip())
            self.image_path = lines[-1].split(": ", 1)[1].strip()
            if self.image_path:
                pixmap = QPixmap(self.image_path)
                self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

    # Check if a window with the specified name is open
    def is_window_open(self, window_name):
        return any(window.widget().name_input.text() == window_name for window in self.mdi_area.subWindowList())

    # Load a window from a file
    def load_window(self, window_name):
        file_path = os.path.join("saved", f"{window_name}.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                window_type = file.readline().split(": ")[1].strip()

                sub_window = QMdiSubWindow()
                if window_type == "ObstacleWindow":
                    window_instance = ObstacleWindow(add_default_rows=False)
                elif window_type == "CharacterWindow":
                    window_instance = CharacterWindow()
                elif window_type == "ZoneWindow":
                    window_instance = ZoneWindow(self.mdi_area)
                else:
                    window_instance = DefaultWindow()

                window_instance.load_contents(file_path)
                sub_window.setWidget(window_instance)
                sub_window.setAttribute(Qt.WA_DeleteOnClose)
                self.mdi_area.addSubWindow(sub_window)
                sub_window.show()
