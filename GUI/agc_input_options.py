import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                               QComboBox, QGroupBox, QGridLayout, QSpinBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class AGCInputOptions(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("AGC Input Options")
        self.setFixedSize(550, 450)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top section layout (CPS2 Options and Smoothed ACE Options)
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        
        # CPS2 Options Group
        cps2_group = QGroupBox("CPS2 Options")
        cps2_layout = QVBoxLayout(cps2_group)
        cps2_layout.setSpacing(10)
        
        # Interval Length
        interval_layout = QHBoxLayout()
        interval_label = QLabel("Interval Length:")
        interval_label.setMinimumWidth(100)
        self.interval_input = QSpinBox()
        self.interval_input.setMinimum(1)
        self.interval_input.setMaximum(9999)
        self.interval_input.setValue(10)
        self.interval_input.setMinimumWidth(60)
        
        interval_layout.addWidget(interval_label)
        interval_layout.addStretch()
        interval_layout.addWidget(self.interval_input)
        
        # L10
        l10_layout = QHBoxLayout()
        l10_label = QLabel("L10:")
        l10_label.setMinimumWidth(100)
        self.l10_input = QSpinBox()
        self.l10_input.setMinimum(1)
        self.l10_input.setMaximum(9999)
        self.l10_input.setValue(50)
        self.l10_input.setMinimumWidth(60)
        
        l10_layout.addWidget(l10_label)
        l10_layout.addStretch()
        l10_layout.addWidget(self.l10_input)
        
        # Other L10 Values button
        other_l10_btn = QPushButton("Other L10 Values")
        other_l10_btn.setMinimumHeight(30)
        other_l10_btn.clicked.connect(self.other_l10_values)
        
        cps2_layout.addLayout(interval_layout)
        cps2_layout.addLayout(l10_layout)
        cps2_layout.addWidget(other_l10_btn)
        cps2_layout.addStretch()
        
        # Smoothed ACE Options Group
        ace_group = QGroupBox("Smoothed ACE Options")
        ace_layout = QVBoxLayout(ace_group)
        ace_layout.setSpacing(15)
        
        # Integral Length
        integral_layout = QHBoxLayout()
        integral_label = QLabel("Integral Length:")
        integral_label.setMinimumWidth(100)
        self.integral_input = QSpinBox()
        self.integral_input.setMinimum(1)
        self.integral_input.setMaximum(9999)
        self.integral_input.setValue(180)
        self.integral_input.setMinimumWidth(60)
        
        integral_layout.addWidget(integral_label)
        integral_layout.addStretch()
        integral_layout.addWidget(self.integral_input)
        
        # K1
        k1_layout = QHBoxLayout()
        k1_label = QLabel("K1:")
        k1_label.setMinimumWidth(100)
        self.k1_input = QSpinBox()
        self.k1_input.setMinimum(0)
        self.k1_input.setMaximum(9999)
        self.k1_input.setValue(1)
        self.k1_input.setMinimumWidth(60)
        
        k1_layout.addWidget(k1_label)
        k1_layout.addStretch()
        k1_layout.addWidget(self.k1_input)
        
        # K2
        k2_layout = QHBoxLayout()
        k2_label = QLabel("K2:")
        k2_label.setMinimumWidth(100)
        self.k2_input = QSpinBox()
        self.k2_input.setMinimum(0)
        self.k2_input.setMaximum(9999)
        self.k2_input.setValue(2)
        self.k2_input.setMinimumWidth(60)
        
        k2_layout.addWidget(k2_label)
        k2_layout.addStretch()
        k2_layout.addWidget(self.k2_input)
        
        ace_layout.addLayout(integral_layout)
        ace_layout.addLayout(k1_layout)
        ace_layout.addLayout(k2_layout)
        ace_layout.addStretch()
        
        top_layout.addWidget(cps2_group)
        top_layout.addWidget(ace_group)
        
        main_layout.addLayout(top_layout)
        
        # AGC Deadband Group
        deadband_group = QGroupBox("AGC Deadband")
        deadband_layout = QHBoxLayout(deadband_group)
        
        deadband_label = QLabel("Deadband [MW]:")
        deadband_label.setMinimumWidth(120)
        self.deadband_input = QSpinBox()
        self.deadband_input.setMinimum(0)
        self.deadband_input.setMaximum(9999)
        self.deadband_input.setValue(5)
        self.deadband_input.setMinimumWidth(60)
        
        deadband_layout.addWidget(deadband_label)
        deadband_layout.addStretch()
        deadband_layout.addWidget(self.deadband_input)
        
        main_layout.addWidget(deadband_group)
        
        # AGC Modes Group
        modes_group = QGroupBox("AGC Modes")
        modes_layout = QHBoxLayout(modes_group)
        
        mode_label = QLabel("AGC Mode:")
        mode_label.setMinimumWidth(120)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "3 - Smooth Mode",
            "1 - Normal Mode",
            "2 - Fast Mode",
            "4 - Custom Mode"
        ])
        self.mode_combo.setMinimumWidth(150)
        
        modes_layout.addWidget(mode_label)
        modes_layout.addStretch()
        modes_layout.addWidget(self.mode_combo)
        
        main_layout.addWidget(modes_group)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        done_button = QPushButton("Done")
        done_button.setMinimumSize(80, 35)
        done_button.clicked.connect(self.done_clicked)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumSize(80, 35)
        cancel_button.clicked.connect(self.cancel_clicked)
        
        bottom_layout.addWidget(done_button)
        bottom_layout.addWidget(cancel_button)
        
        main_layout.addLayout(bottom_layout)
        
        # Apply styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin: 3px 0px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #adadad;
                padding: 5px;
                border-radius: 3px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #d4edda;
            }
            QPushButton:pressed {
                background-color: #c3e6cb;
            }
            QSpinBox {
                border: 1px solid #ccc;
                padding: 3px;
                border-radius: 3px;
                background-color: white;
            }
            QComboBox {
                border: 1px solid #ccc;
                padding: 3px;
                border-radius: 3px;
                background-color: white;
                min-height: 20px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
            }
            QLabel {
                color: #333333;
            }
        """)
    
    def other_l10_values(self):
        # Placeholder for Other L10 Values dialog
        print("Other L10 Values clicked")
        # In a real application, this would open a dialog for additional L10 configuration
    
    def done_clicked(self):
        # Handle done button click
        print("Done clicked")
        print(f"Interval Length: {self.interval_input.value()}")
        print(f"L10: {self.l10_input.value()}")
        print(f"Integral Length: {self.integral_input.value()}")
        print(f"K1: {self.k1_input.value()}")
        print(f"K2: {self.k2_input.value()}")
        print(f"Deadband [MW]: {self.deadband_input.value()}")
        print(f"AGC Mode: {self.mode_combo.currentText()}")
        self.close()
    
    def cancel_clicked(self):
        # Handle cancel button click
        print("Cancel clicked")
        self.close()


def main():
    app = QApplication(sys.argv)
    window = AGCInputOptions()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()