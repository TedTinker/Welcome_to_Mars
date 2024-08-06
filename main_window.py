import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QAction, QMdiArea, QMdiSubWindow, QWidget
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor
from default_window import DefaultWindow
from character_window import CharacterWindow
from obstacle_window import ObstacleWindow
from zone_window import ZoneWindow

# Overlay class to draw connections between windows
class ConnectionOverlay(QWidget):
    def __init__(self, mdi_area, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.mdi_area = mdi_area
        self.connections = {}

    # Update the connections to be drawn
    def update_connections(self, connections):
        self.connections = connections
        self.update()

    # Paint event to draw the connections
    def paintEvent(self, event):
        painter = QPainter(self)
        
        valid_windows = {sub_window.widget().name_input.text(): sub_window for sub_window in self.mdi_area.subWindowList() if self.is_valid_window(sub_window)}
        
        for zone_window, connected_window_names in self.connections.items():
            if zone_window in valid_windows.values():
                zone_center = self._get_center_point(zone_window)
                painter.setBrush(QColor(255, 0, 0, 127)) 
                painter.drawEllipse(zone_center, 5, 5) 
                for connected_window_name in connected_window_names:
                    if connected_window_name in valid_windows:
                        connected_window = valid_windows[connected_window_name]
                        connected_center = self._get_center_point(connected_window)
                        
                        # Set the pen color based on the type of connected window
                        if isinstance(connected_window.widget(), CharacterWindow):
                            pen = QPen(Qt.black, 2)
                        elif isinstance(connected_window.widget(), ObstacleWindow):
                            pen = QPen(Qt.white, 2)
                        else:
                            pen = QPen(Qt.black, 2)
                        
                        painter.setPen(pen)
                        painter.setBrush(QColor(0, 0, 255, 127))  
                        painter.drawEllipse(connected_center, 5, 5)  
                        painter.drawLine(zone_center, connected_center)
        
        painter.end()

    # Get the center point of a sub-window
    def _get_center_point(self, sub_window):
        if not self.is_valid_window(sub_window):
            return QPoint(0, 0)
        global_center = sub_window.mapToGlobal(sub_window.rect().center())
        local_center = self.mapFromGlobal(global_center)
        return local_center

    # Check if a sub-window is valid for drawing connections
    def is_valid_window(self, sub_window):
        try:
            return sub_window and sub_window.widget() and sub_window.isVisible() and not sub_window.isMinimized()
        except RuntimeError:
            return False

# Main application window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 800, 600)
        
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        
        self.overlay = ConnectionOverlay(self.mdi_area, self.mdi_area.viewport())
        self.overlay.setGeometry(self.mdi_area.viewport().geometry())
        self.overlay.show()
        
        self.create_menu()
        
        self.zone_connections = {}
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_connections)
        self.timer.start(100)  # Update every 100 ms

    # Update the overlay geometry on resize
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay.setGeometry(self.mdi_area.viewport().geometry())
        self.update_connections()

    # Create the menu bar and actions
    def create_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('File')
        
        new_character_action = QAction('New Character Window', self)
        new_character_action.triggered.connect(lambda: self.new_window(CharacterWindow))
        file_menu.addAction(new_character_action)
        
        new_obstacle_action = QAction('New Obstacle Window', self)
        new_obstacle_action.triggered.connect(lambda: self.new_window(ObstacleWindow))
        file_menu.addAction(new_obstacle_action)
        
        new_zone_action = QAction('New Zone Window', self)
        new_zone_action.triggered.connect(lambda: self.new_window(lambda: ZoneWindow(self.mdi_area)))
        file_menu.addAction(new_zone_action)
        
        load_action = QAction('Load', self)
        load_action.triggered.connect(self.load_windows)
        file_menu.addAction(load_action)

        save_all_action = QAction('Save All', self)
        save_all_action.triggered.connect(self.save_all_windows)
        file_menu.addAction(save_all_action)
        
        close_all_action = QAction('Close All', self)
        close_all_action.triggered.connect(self.close_all_windows)
        file_menu.addAction(close_all_action)
    
    # Create a new window of the specified class
    def new_window(self, window_class):
        sub_window = QMdiSubWindow()
        window_instance = window_class()
        sub_window.setWidget(window_instance)
        sub_window.setAttribute(Qt.WA_DeleteOnClose)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
        
        self.update_zone_window_dropdowns()
        self.update_connections()
        
        sub_window.moveEvent = self.update_connections_event
        sub_window.resizeEvent = self.update_connections_event
        sub_window.closeEvent = self.close_event

    # Load windows from saved files
    def load_windows(self):
        options = QFileDialog.Options()
        file_names, _ = QFileDialog.getOpenFileNames(self, "Load Files", "saved", "Text Files (*.txt);;All Files (*)", options=options)
        if file_names:
            for file_name in file_names:
                with open(file_name, 'r') as file:
                    first_line = file.readline()
                    window_type = first_line.split(": ")[1].strip()
                    
                    sub_window = QMdiSubWindow()
                    
                    if window_type == "ObstacleWindow":
                        window_instance = ObstacleWindow(add_default_rows=False)
                    elif window_type == "CharacterWindow":
                        window_instance = CharacterWindow()
                    elif window_type == "ZoneWindow":
                        window_instance = ZoneWindow(self.mdi_area)
                    else:
                        window_instance = DefaultWindow()

                    window_instance.load_contents(file_name)
                    sub_window.setWidget(window_instance)
                    sub_window.setAttribute(Qt.WA_DeleteOnClose)
                    self.mdi_area.addSubWindow(sub_window)
                    sub_window.show()
        
        self.update_zone_window_dropdowns()
        self.update_connections()

    # Save all open windows
    def save_all_windows(self):
        saved_files = []
        for sub_window in self.mdi_area.subWindowList():
            widget = sub_window.widget()
            if isinstance(widget, DefaultWindow):
                name = widget.name_input.text()
                if name:
                    widget.save_contents(suppress_message=True)
                    saved_files.append(f"{name}.txt")
        
        if saved_files:
            saved_files_str = ", ".join(saved_files)
            QMessageBox.information(self, 'Info', f'Contents saved to {saved_files_str}')
                
    # Close all open windows
    def close_all_windows(self):
        for sub_window in self.mdi_area.subWindowList():
            sub_window.close()
        
        self.update_zone_window_dropdowns()
        self.update_connections()

    # Update the dropdowns in all zone windows
    def update_zone_window_dropdowns(self):
        for sub_window in self.mdi_area.subWindowList():
            if isinstance(sub_window.widget(), ZoneWindow):
                sub_window.widget().update_dropdown()
        
    # Event handler to update connections on move/resize
    def update_connections_event(self, event):
        self.update_connections()
        super(QMdiSubWindow, self).moveEvent(event)

    # Event handler to update connections on close
    def close_event(self, event):
        sub_window = self.sender()
        if isinstance(sub_window, QMdiSubWindow):
            sub_window.deleteLater()
        self.update_connections()
        event.accept()

    # Update the connections for the overlay
    def update_connections(self):
        self.zone_connections.clear()
        for sub_window in self.mdi_area.subWindowList():
            if isinstance(sub_window.widget(), ZoneWindow):
                zone_window = sub_window.widget()
                connected_windows = zone_window.get_all_row_names()
                self.zone_connections[sub_window] = connected_windows
        self.overlay.update_connections(self.zone_connections)
        self.update()
