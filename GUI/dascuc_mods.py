import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                               QListWidget, QGridLayout, QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


class DASCUCFunctionalMods(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("DASCUC Functional Mods")
        self.setFixedSize(750, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Model Input File section
        file_layout = QHBoxLayout()
        file_label = QLabel("Model Input File:")
        file_label.setMinimumWidth(120)
        
        self.file_input = QLineEdit()
        self.file_input.setMinimumHeight(30)
        
        browse_button = QPushButton("Browse")
        browse_button.setMinimumSize(80, 30)
        browse_button.clicked.connect(self.browse_file)
        
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_button)
        
        main_layout.addLayout(file_layout)
        
        # Button sections layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        # Left side buttons (Mods Before DASCUC)
        left_buttons_layout = QVBoxLayout()
        left_buttons_layout.setSpacing(10)
        
        left_button_row = QHBoxLayout()
        add_before_btn = QPushButton("Add")
        add_before_btn.setMinimumSize(80, 35)
        add_before_btn.clicked.connect(self.add_before_mod)
        
        remove_before_btn = QPushButton("Remove")
        remove_before_btn.setMinimumSize(80, 35)
        remove_before_btn.clicked.connect(self.remove_before_mod)
        
        left_button_row.addWidget(add_before_btn)
        left_button_row.addWidget(remove_before_btn)
        left_button_row.addStretch()
        
        left_buttons_layout.addLayout(left_button_row)
        
        # Right side buttons (Mods After DASCUC)
        right_buttons_layout = QVBoxLayout()
        right_buttons_layout.setSpacing(10)
        
        right_button_row = QHBoxLayout()
        add_after_btn = QPushButton("Add")
        add_after_btn.setMinimumSize(80, 35)
        add_after_btn.clicked.connect(self.add_after_mod)
        
        remove_after_btn = QPushButton("Remove")
        remove_after_btn.setMinimumSize(80, 35)
        remove_after_btn.clicked.connect(self.remove_after_mod)
        
        right_button_row.addWidget(add_after_btn)
        right_button_row.addWidget(remove_after_btn)
        right_button_row.addStretch()
        
        right_buttons_layout.addLayout(right_button_row)
        
        buttons_layout.addLayout(left_buttons_layout)
        buttons_layout.addLayout(right_buttons_layout)
        
        main_layout.addLayout(buttons_layout)
        
        # List widgets section
        lists_layout = QHBoxLayout()
        lists_layout.setSpacing(20)
        
        # Mods Before DASCUC
        before_layout = QVBoxLayout()
        before_label = QLabel("Mods Before DASCUC")
        before_label.setAlignment(Qt.AlignCenter)
        before_label.setStyleSheet("font-weight: bold; padding: 5px; background-color: #f0f0f0; border: 1px solid #ccc;")
        
        self.before_list = QListWidget()
        self.before_list.setMinimumHeight(300)
        self.before_list.setStyleSheet("border: 1px solid #ccc;")
        
        before_layout.addWidget(before_label)
        before_layout.addWidget(self.before_list)
        
        # Mods After DASCUC
        after_layout = QVBoxLayout()
        after_label = QLabel("Mods After DASCUC")
        after_label.setAlignment(Qt.AlignCenter)
        after_label.setStyleSheet("font-weight: bold; padding: 5px; background-color: #f0f0f0; border: 1px solid #ccc;")
        
        self.after_list = QListWidget()
        self.after_list.setMinimumHeight(300)
        self.after_list.setStyleSheet("border: 1px solid #ccc;")
        
        after_layout.addWidget(after_label)
        after_layout.addWidget(self.after_list)
        
        lists_layout.addLayout(before_layout)
        lists_layout.addLayout(after_layout)
        
        main_layout.addLayout(lists_layout)
        
        # Bottom buttons
        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.addStretch()
        
        done_button = QPushButton("Done")
        done_button.setMinimumSize(80, 35)
        done_button.clicked.connect(self.done_clicked)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumSize(80, 35)
        cancel_button.clicked.connect(self.cancel_clicked)
        
        bottom_buttons_layout.addWidget(done_button)
        bottom_buttons_layout.addWidget(cancel_button)
        
        main_layout.addLayout(bottom_buttons_layout)
        
        # Set window properties
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #adadad;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d4edda;
            }
            QPushButton:pressed {
                background-color: #c3e6cb;
            }
            QLineEdit {
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 3px;
            }
        """)
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Model Input File", 
            "", 
            "All Files (*)"
        )
        if file_path:
            self.file_input.setText(file_path)
    
    def add_before_mod(self):
        # Placeholder for adding mods before DASCUC
        # In a real application, this would open a dialog to select/add mods
        self.before_list.addItem("Sample Mod Before")
    
    def remove_before_mod(self):
        current_row = self.before_list.currentRow()
        if current_row >= 0:
            self.before_list.takeItem(current_row)
    
    def add_after_mod(self):
        # Placeholder for adding mods after DASCUC
        # In a real application, this would open a dialog to select/add mods
        self.after_list.addItem("Sample Mod After")
    
    def remove_after_mod(self):
        current_row = self.after_list.currentRow()
        if current_row >= 0:
            self.after_list.takeItem(current_row)
    
    def done_clicked(self):
        # Handle done button click
        print("Done clicked")
        print(f"Model Input File: {self.file_input.text()}")
        print(f"Mods Before DASCUC: {[self.before_list.item(i).text() for i in range(self.before_list.count())]}")
        print(f"Mods After DASCUC: {[self.after_list.item(i).text() for i in range(self.after_list.count())]}")
        self.close()
    
    def cancel_clicked(self):
        # Handle cancel button click
        print("Cancel clicked")
        self.close()


def main():
    app = QApplication(sys.argv)
    window = DASCUCFunctionalMods()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()