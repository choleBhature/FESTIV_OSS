import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                               QComboBox, QGroupBox, QGridLayout, QSpinBox,
                               QRadioButton, QButtonGroup, QCheckBox, QTableWidget,
                               QTableWidgetItem, QTextEdit, QListWidget, QTabWidget,
                               QFileDialog, QSplitter, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class ReservePickUpDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reserve Pick Up Parameters Input Dialog")
        self.setFixedSize(500, 380)
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Main Setting
        main_group = QGroupBox("Main Setting")
        main_layout = QHBoxLayout(main_group)
        main_layout.addWidget(QLabel("Should a Reserve Pick Up be allowed?"))
        main_layout.addStretch()
        
        self.main_bg = QButtonGroup()
        yes_radio = QRadioButton("Yes")
        no_radio = QRadioButton("No")
        no_radio.setChecked(True)
        self.main_bg.addButton(yes_radio, 1)
        self.main_bg.addButton(no_radio, 0)
        main_layout.addWidget(yes_radio)
        main_layout.addWidget(no_radio)
        
        # RPU Timing Parameters
        timing_group = QGroupBox("RPU Timing Parameters")
        timing_layout = QHBoxLayout(timing_group)
        
        timing_layout.addWidget(QLabel("HRPU:"))
        self.hrpu_spin = QSpinBox()
        self.hrpu_spin.setValue(6)
        timing_layout.addWidget(self.hrpu_spin)
        
        timing_layout.addWidget(QLabel("IRPU:"))
        self.irpu_spin = QSpinBox()
        self.irpu_spin.setValue(10)
        timing_layout.addWidget(self.irpu_spin)
        
        timing_layout.addWidget(QLabel("PRPU:"))
        self.prpu_spin = QSpinBox()
        self.prpu_spin.setValue(1)
        timing_layout.addWidget(self.prpu_spin)
        
        # RPU Operating Parameters
        operating_group = QGroupBox("RPU Operating Parameters")
        operating_layout = QVBoxLayout(operating_group)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("ACE Threshold in MW:"))
        self.ace_threshold = QSpinBox()
        self.ace_threshold.setMaximum(9999)
        self.ace_threshold.setValue(1000)
        row1.addWidget(self.ace_threshold)
        
        row1.addWidget(QLabel("Time Restriction [min]:"))
        self.time_restriction = QSpinBox()
        self.time_restriction.setValue(10)
        row1.addWidget(self.time_restriction)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("ACE Threshold in AGC intervals:"))
        self.ace_agc_intervals = QSpinBox()
        self.ace_agc_intervals.setValue(2)
        row2.addWidget(self.ace_agc_intervals)
        row2.addStretch()
        
        operating_layout.addLayout(row1)
        operating_layout.addLayout(row2)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        rpu_mods_btn = QPushButton("RPU Mods")
        bottom_layout.addWidget(rpu_mods_btn)
        bottom_layout.addStretch()
        
        done_btn = QPushButton("Done")
        cancel_btn = QPushButton("Cancel")
        done_btn.clicked.connect(self.close)
        cancel_btn.clicked.connect(self.close)
        bottom_layout.addWidget(done_btn)
        bottom_layout.addWidget(cancel_btn)
        
        layout.addWidget(main_group)
        layout.addWidget(timing_group)
        layout.addWidget(operating_group)
        layout.addLayout(bottom_layout)
        
        self.apply_styles()
    
    def apply_styles(self):
        self.setStyleSheet("""
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
                padding: 5px 10px;
                border-radius: 3px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #d4edda;
            }
        """)


class MultipleRunsDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiple Runs Input Dialog")
        self.setFixedSize(900, 650)
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Multiple Runs checkbox
        self.multiple_runs_cb = QCheckBox("Multiple Runs")
        layout.addWidget(self.multiple_runs_cb)
        
        # Input/Output file section
        file_layout = QVBoxLayout()
        
        input_row = QHBoxLayout()
        input_row.addWidget(QLabel("Input File Name:"))
        self.input_file = QLineEdit("PJM_5_BUS.h5")
        input_row.addWidget(self.input_file)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_input_file)
        input_row.addWidget(browse_btn)
        
        output_row = QHBoxLayout()
        output_row.addWidget(QLabel("Output File Name:"))
        self.output_file = QLineEdit()
        output_row.addWidget(self.output_file)
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_run)
        output_row.addWidget(add_btn)
        
        file_layout.addLayout(input_row)
        file_layout.addLayout(output_row)
        
        # Table for runs
        self.runs_table = QTableWidget(0, 2)
        self.runs_table.setHorizontalHeaderLabels(["Input File Name", "Output File Name"])
        self.runs_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addLayout(file_layout)
        layout.addWidget(self.runs_table)
        
        self.apply_styles()
    
    def browse_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", "HDF5 Files (*.h5)")
        if file_path:
            self.input_file.setText(file_path)
    
    def add_run(self):
        if self.input_file.text() and self.output_file.text():
            row = self.runs_table.rowCount()
            self.runs_table.insertRow(row)
            self.runs_table.setItem(row, 0, QTableWidgetItem(self.input_file.text()))
            self.runs_table.setItem(row, 1, QTableWidgetItem(self.output_file.text()))
            self.output_file.clear()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #adadad;
                padding: 5px 10px;
                border-radius: 3px;
                min-height: 20px;
            }
        """)


class ContingencyParametersDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contingency Parameters Input Dialog")
        self.setFixedSize(500, 480)
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # How will contingencies be simulated
        sim_group = QGroupBox("How will contingencies be simulated?")
        sim_layout = QHBoxLayout(sim_group)
        
        self.sim_bg = QButtonGroup()
        none_radio = QRadioButton("None at all")
        none_radio.setChecked(True)
        prespec_radio = QRadioButton("Prespecified by the user")
        random_radio = QRadioButton("Randomly")
        
        self.sim_bg.addButton(none_radio, 0)
        self.sim_bg.addButton(prespec_radio, 1)
        self.sim_bg.addButton(random_radio, 2)
        
        sim_layout.addWidget(none_radio)
        sim_layout.addWidget(prespec_radio)
        sim_layout.addWidget(random_radio)
        
        # Contingency Parameters
        params_group = QGroupBox("Contingency Parameters")
        params_layout = QGridLayout(params_group)
        
        params_layout.addWidget(QLabel("Unit to Outage:"), 0, 0)
        self.unit_combo = QComboBox()
        self.unit_combo.addItem("ALTA")
        params_layout.addWidget(self.unit_combo, 0, 1)
        
        params_layout.addWidget(QLabel("Time of Outage:"), 0, 2)
        time_layout = QHBoxLayout()
        self.day_spin = QSpinBox()
        self.hour_spin = QSpinBox()
        self.min_spin = QSpinBox()
        self.sec_spin = QSpinBox()
        
        time_layout.addWidget(self.day_spin)
        time_layout.addWidget(QLabel("D"))
        time_layout.addWidget(self.hour_spin)
        time_layout.addWidget(QLabel("H"))
        time_layout.addWidget(self.min_spin)
        time_layout.addWidget(QLabel("M"))
        time_layout.addWidget(self.sec_spin)
        time_layout.addWidget(QLabel("S"))
        
        time_widget = QWidget()
        time_widget.setLayout(time_layout)
        params_layout.addWidget(time_widget, 0, 3)
        
        # Generator table
        self.gen_table = QTableWidget(0, 2)
        self.gen_table.setHorizontalHeaderLabels(["Generator Name", "Time of Outage [hr]"])
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        remove_btn = QPushButton("Remove")
        add_btn.clicked.connect(self.add_generator)
        remove_btn.clicked.connect(self.remove_generator)
        
        bottom_layout.addWidget(add_btn)
        bottom_layout.addWidget(remove_btn)
        bottom_layout.addStretch()
        
        done_btn = QPushButton("Done")
        cancel_btn = QPushButton("Cancel")
        done_btn.clicked.connect(self.close)
        cancel_btn.clicked.connect(self.close)
        bottom_layout.addWidget(done_btn)
        bottom_layout.addWidget(cancel_btn)
        
        layout.addWidget(sim_group)
        layout.addWidget(params_group)
        layout.addWidget(self.gen_table)
        layout.addLayout(bottom_layout)
        
        self.apply_styles()
    
    def add_generator(self):
        row = self.gen_table.rowCount()
        self.gen_table.insertRow(row)
        self.gen_table.setItem(row, 0, QTableWidgetItem("Generator"))
        self.gen_table.setItem(row, 1, QTableWidgetItem("0"))
    
    def remove_generator(self):
        current_row = self.gen_table.currentRow()
        if current_row >= 0:
            self.gen_table.removeRow(current_row)
    
    def apply_styles(self):
        self.setStyleSheet("""
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
                padding: 5px 10px;
                border-radius: 3px;
                min-height: 20px;
            }
        """)


class DebuggingParametersDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Debugging Parameters Input Dialog")
        self.setFixedSize(500, 450)
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Suppress Outputs
        suppress_group = QGroupBox("Suppress Outputs")
        suppress_layout = QHBoxLayout(suppress_group)
        suppress_layout.addWidget(QLabel("Suppress output plots?"))
        suppress_layout.addStretch()
        
        self.suppress_bg = QButtonGroup()
        yes_radio1 = QRadioButton("Yes")
        no_radio1 = QRadioButton("No")
        no_radio1.setChecked(True)
        self.suppress_bg.addButton(yes_radio1, 1)
        self.suppress_bg.addButton(no_radio1, 0)
        suppress_layout.addWidget(yes_radio1)
        suppress_layout.addWidget(no_radio1)
        
        # Solver Options - Which solver
        solver_group = QGroupBox("Solver Options")
        solver_layout = QHBoxLayout(solver_group)
        solver_layout.addWidget(QLabel("Which solver?"))
        solver_layout.addStretch()
        
        self.solver_bg = QButtonGroup()
        cplex_radio = QRadioButton("Cplex")
        cplex_radio.setChecked(True)
        gurobi_radio = QRadioButton("Gurobi")
        self.solver_bg.addButton(cplex_radio, 0)
        self.solver_bg.addButton(gurobi_radio, 1)
        solver_layout.addWidget(cplex_radio)
        solver_layout.addWidget(gurobi_radio)
        
        # Solver Options - Integers
        integers_group = QGroupBox("Solver Options")
        integers_layout = QHBoxLayout(integers_group)
        integers_layout.addWidget(QLabel("Should integers be used?"))
        integers_layout.addStretch()
        
        self.integers_bg = QButtonGroup()
        yes_radio2 = QRadioButton("Yes")
        yes_radio2.setChecked(True)
        no_radio2 = QRadioButton("No")
        self.integers_bg.addButton(yes_radio2, 1)
        self.integers_bg.addButton(no_radio2, 0)
        integers_layout.addWidget(yes_radio2)
        integers_layout.addWidget(no_radio2)
        
        # Execution Options
        exec_group = QGroupBox("Execution Options")
        exec_layout = QVBoxLayout(exec_group)
        
        stop_layout = QHBoxLayout()
        stop_layout.addWidget(QLabel("Stop execution at a certain time?"))
        stop_layout.addStretch()
        
        self.stop_bg = QButtonGroup()
        yes_radio3 = QRadioButton("Yes")
        no_radio3 = QRadioButton("No")
        no_radio3.setChecked(True)
        self.stop_bg.addButton(yes_radio3, 1)
        self.stop_bg.addButton(no_radio3, 0)
        stop_layout.addWidget(yes_radio3)
        stop_layout.addWidget(no_radio3)
        
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Time to stop [hr] :"))
        time_layout.addStretch()
        self.time_stop = QSpinBox()
        self.time_stop.setMaximum(9999)
        self.time_stop.setValue(999)
        time_layout.addWidget(self.time_stop)
        
        exec_layout.addLayout(stop_layout)
        exec_layout.addLayout(time_layout)
        
        # Done button
        done_btn = QPushButton("Done")
        done_btn.clicked.connect(self.close)
        done_layout = QHBoxLayout()
        done_layout.addStretch()
        done_layout.addWidget(done_btn)
        
        layout.addWidget(suppress_group)
        layout.addWidget(solver_group)
        layout.addWidget(integers_group)
        layout.addWidget(exec_group)
        layout.addLayout(done_layout)
        
        self.apply_styles()
    
    def apply_styles(self):
        self.setStyleSheet("""
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
                padding: 5px 10px;
                border-radius: 3px;
                min-height: 20px;
            }
        """)


class OtherFunctionalModsDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Other Functional Mods")
        self.setFixedSize(600, 500)
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Dropdown
        self.rules_combo = QComboBox()
        self.rules_combo.addItem("Choose where to add additional rules")
        layout.addWidget(self.rules_combo)
        
        # Model Input File
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Model Input File:"))
        self.model_file = QLineEdit()
        file_layout.addWidget(self.model_file)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        # Two columns layout
        columns_layout = QHBoxLayout()
        
        # Left column
        left_layout = QVBoxLayout()
        left_buttons = QHBoxLayout()
        add_btn1 = QPushButton("Add")
        remove_btn1 = QPushButton("Remove")
        add_btn1.clicked.connect(self.add_left_item)
        remove_btn1.clicked.connect(self.remove_left_item)
        left_buttons.addWidget(add_btn1)
        left_buttons.addWidget(remove_btn1)
        
        self.left_list = QListWidget()
        self.left_list.addItem("---")
        
        left_layout.addLayout(left_buttons)
        left_layout.addWidget(self.left_list)
        
        # Right column
        right_layout = QVBoxLayout()
        right_buttons = QHBoxLayout()
        add_btn2 = QPushButton("Add")
        remove_btn2 = QPushButton("Remove")
        add_btn2.clicked.connect(self.add_right_item)
        remove_btn2.clicked.connect(self.remove_right_item)
        right_buttons.addWidget(add_btn2)
        right_buttons.addWidget(remove_btn2)
        
        self.right_list = QListWidget()
        self.right_list.addItem("---")
        
        right_layout.addLayout(right_buttons)
        right_layout.addWidget(self.right_list)
        
        columns_layout.addLayout(left_layout)
        columns_layout.addLayout(right_layout)
        
        layout.addLayout(columns_layout)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        done_btn = QPushButton("Done")
        cancel_btn = QPushButton("Cancel")
        done_btn.clicked.connect(self.close)
        cancel_btn.clicked.connect(self.close)
        bottom_layout.addWidget(done_btn)
        bottom_layout.addWidget(cancel_btn)
        
        layout.addLayout(bottom_layout)
        
        self.apply_styles()
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Model Input File", "", "All Files (*)")
        if file_path:
            self.model_file.setText(file_path)
    
    def add_left_item(self):
        self.left_list.addItem("New Item")
    
    def remove_left_item(self):
        current_row = self.left_list.currentRow()
        if current_row >= 0:
            self.left_list.takeItem(current_row)
    
    def add_right_item(self):
        self.right_list.addItem("New Item")
    
    def remove_right_item(self):
        current_row = self.right_list.currentRow()
        if current_row >= 0:
            self.right_list.takeItem(current_row)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #adadad;
                padding: 5px 10px;
                border-radius: 3px;
                min-height: 20px;
            }
            QListWidget {
                border: 1px solid #ccc;
            }
        """)


class ModifyOptimizationDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modify Optimization Formulation")
        self.setFixedSize(850, 700)
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # DASCUC Tab
        dascuc_tab = QWidget()
        dascuc_layout = QVBoxLayout(dascuc_tab)
        
        # Folder selection
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Select Folder:"))
        self.folder_line = QLineEdit()
        folder_layout.addWidget(self.folder_line)
        browse_folder_btn = QPushButton("Browse")
        browse_folder_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(browse_folder_btn)
        
        # Location selection
        location_layout = QHBoxLayout()
        location_layout.addWidget(QLabel("Select Location:"))
        self.location_combo = QComboBox()
        self.location_combo.addItem("Header")
        location_layout.addWidget(self.location_combo)
        location_layout.addStretch()
        
        dascuc_layout.addLayout(folder_layout)
        dascuc_layout.addLayout(location_layout)
        
        # Main content area
        content_layout = QHBoxLayout()
        
        # Left side
        left_layout = QVBoxLayout()
        default_btn = QPushButton("Default\nDASCUC")
        clear_btn = QPushButton("Clear\nDASCUC")
        default_btn.clicked.connect(self.load_default)
        clear_btn.clicked.connect(self.clear_content)
        left_layout.addWidget(default_btn)
        left_layout.addWidget(clear_btn)
        
        # Warning text
        warning_label = QLabel("Warning:\nChanging\nthe GAMS\ncode may\nresult in an\ninfeasible\nmodel.")
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: red; font-weight: bold;")
        left_layout.addWidget(warning_label)
        left_layout.addStretch()
        
        # Center area
        center_layout = QVBoxLayout()
        self.left_text = QTextEdit()
        center_layout.addWidget(self.left_text)
        
        # Move buttons
        move_layout = QVBoxLayout()
        move_layout.addStretch()
        move_right_btn = QPushButton(">")
        move_left_btn = QPushButton("<")
        move_right_btn.clicked.connect(self.move_right)
        move_left_btn.clicked.connect(self.move_left)
        move_layout.addWidget(move_right_btn)
        move_layout.addWidget(move_left_btn)
        move_layout.addStretch()
        
        # Right area
        right_layout = QVBoxLayout()
        self.right_text = QTextEdit()
        self.right_text.setStyleSheet("background-color: lightblue;")
        self.right_text.append("Base_DAC_Header.txt")
        right_layout.addWidget(self.right_text)
        
        content_layout.addLayout(left_layout)
        content_layout.addLayout(center_layout)
        content_layout.addLayout(move_layout)
        content_layout.addLayout(right_layout)
        
        dascuc_layout.addLayout(content_layout)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        load_all_btn = QPushButton("Load All")
        save_all_btn = QPushButton("Save All")
        summary_btn = QPushButton("Summary")
        load_all_btn.clicked.connect(self.load_all)
        save_all_btn.clicked.connect(self.save_all)
        summary_btn.clicked.connect(self.show_summary)
        bottom_layout.addWidget(load_all_btn)
        bottom_layout.addWidget(save_all_btn)
        bottom_layout.addWidget(summary_btn)
        bottom_layout.addStretch()
        
        done_btn = QPushButton("Done")
        cancel_btn = QPushButton("Cancel")
        done_btn.clicked.connect(self.close)
        cancel_btn.clicked.connect(self.close)
        bottom_layout.addWidget(done_btn)
        bottom_layout.addWidget(cancel_btn)
        
        dascuc_layout.addLayout(bottom_layout)
        
        self.tabs.addTab(dascuc_tab, "DASCUC")
        
        # Add placeholder tabs
        rtscuc_tab = QWidget()
        rtscuc_layout = QVBoxLayout(rtscuc_tab)
        rtscuc_label = QLabel("RTSCUC content will be implemented here")
        rtscuc_label.setAlignment(Qt.AlignCenter)
        rtscuc_layout.addWidget(rtscuc_label)
        self.tabs.addTab(rtscuc_tab, "RTSCUC")
        
        rtsced_tab = QWidget()
        rtsced_layout = QVBoxLayout(rtsced_tab)
        rtsced_label = QLabel("RTSCED content will be implemented here")
        rtsced_label.setAlignment(Qt.AlignCenter)
        rtsced_layout.addWidget(rtsced_label)
        self.tabs.addTab(rtsced_tab, "RTSCED")
        
        layout.addWidget(self.tabs)
        
        self.apply_styles()
    
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_line.setText(folder_path)
    
    def load_default(self):
        self.left_text.setText("Default DASCUC content loaded")
    
    def clear_content(self):
        self.left_text.clear()
    
    def move_right(self):
        selected_text = self.left_text.textCursor().selectedText()
        if selected_text:
            self.right_text.append(selected_text)
    
    def move_left(self):
        selected_text = self.right_text.textCursor().selectedText()
        if selected_text:
            self.left_text.append(selected_text)
    
    def load_all(self):
        print("Load All functionality")
    
    def save_all(self):
        print("Save All functionality")
    
    def show_summary(self):
        print("Summary functionality")
    
    def apply_styles(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #adadad;
                padding: 5px 10px;
                border-radius: 3px;
                min-height: 20px;
        }
            QTextEdit {
                border: 1px solid #ccc;
                background-color: white;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
            }
            QTabBar::tab {
                background: #e1e1e1;
                border: 1px solid #c0c0c0;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Test all dialogs
    dialog1 = ReservePickUpDialog()
    dialog1.show()
    
    dialog2 = MultipleRunsDialog()
    dialog2.move(520, 50)
    dialog2.show()
    
    dialog3 = ContingencyParametersDialog()
    dialog3.move(50, 450)
    dialog3.show()
    
    dialog4 = DebuggingParametersDialog()
    dialog4.move(570, 450)
    dialog4.show()
    
    dialog5 = OtherFunctionalModsDialog()
    dialog5.move(1050, 50)
    dialog5.show()
    
    dialog6 = ModifyOptimizationDialog()
    dialog6.move(1050, 600)
    dialog6.show()
    
    sys.exit(app.exec())