import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QTextEdit, QTabWidget, 
    QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QImage, QPixmap, QFont, QColor
from stego.engine import StegHunter
from PIL import Image

# --- WORKER THREAD FOR NON-BLOCKING ANALYSIS ---
class AnalysisWorker(QThread):
    """Worker thread to handle AI analysis without freezing the UI."""
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        try:
            hunter = StegHunter(self.image_path)
            results = hunter.run_full_analysis()
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

# --- MAIN WINDOW ---
class StegHunterPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StegHunter Pro - Advanced Forensics Suite")
        self.resize(1100, 700)
        self.image_path = None
        
        # Apply Modern Dark Theme
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QWidget { background-color: #1e1e2e; color: #cdd6f4; font-family: 'Segoe UI', Arial; }
            QTabWidget::pane { border: 1px solid #45475a; background: #1e1e2e; }
            QTabBar::tab { background: #313244; color: #cdd6f4; padding: 10px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: #45475a; border-bottom: 2px solid #b4befe; }
            QPushButton { background-color: #89b4fa; color: #11111b; font-weight: bold; border-radius: 5px; padding: 8px; }
            QPushButton:hover { background-color: #b4befe; }
            QTextEdit { background-color: #181825; border: 1px solid #45475a; color: #a6adc8; border-radius: 5px; }
            QLabel#ProbLabel { font-size: 32px; font-weight: bold; color: #f5c2e7; }
            QTableWidget { background-color: #181825; gridline-color: #45475a; color: #cdd6f4; }
            QHeaderView::section { background-color: #313244; color: #cdd6f4; padding: 5px; border: 1px solid #45475a; }
        """)

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Top Control Bar
        ctrl_layout = QHBoxLayout()
        self.btn_open = QPushButton("📂 Open Image")
        self.btn_open.clicked.connect(self.open_file)
        self.btn_batch = QPushButton("📂 Batch Scan Folder")
        self.btn_batch.clicked.connect(self.batch_scan)
        
        self.status_label = QLabel("Ready. Please upload an image.")
        ctrl_layout.addWidget(self.btn_open)
        ctrl_layout.addWidget(self.btn_batch)
        ctrl_layout.addStretch()
        ctrl_layout.addWidget(self.status_label)
        layout.addLayout(ctrl_layout)

        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: AI Analysis
        self.tab_ai = QWidget()
        self.setup_ai_tab()
        
        # Tab 2: Visual Proof
        self.tab_visual = QWidget()
        self.setup_visual_tab()
        
        # Tab 3: Forensics
        self.tab_forensics = QWidget()
        self.setup_forensics_tab()
        
        # Tab 4: Batch Results
        self.tab_batch = QWidget()
        self.setup_batch_tab()

        self.tabs.addTab(self.tab_ai, "🧠 AI Analysis")
        self.tabs.addTab(self.tab_visual, "🖼️ Visual Proof")
        self.tabs.addTab(self.tab_forensics, "🔍 Forensics")
        self.tabs.addTab(self.tab_batch, "📦 Batch Results")
        
        layout.addWidget(self.tabs)
        
        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 0) # Hide by default
        self.progress.hide()
        layout.addWidget(self.progress)

    def setup_ai_tab(self):
        layout = QVBoxLayout(self.tab_ai)
        
        self.prob_label = QLabel("0.00%")
        self.prob_label.setObjectName("ProbLabel")
        self.prob_label.setAlignment(Qt.AlignCenter)
        
        self.lsb_output = QTextEdit()
        self.lsb_output.setReadOnly(True)
        self.lsb_output.setPlaceholderText("LSB extracted data will appear here...")

        layout.addWidget(QLabel("Detection Probability:", alignment=Qt.AlignCenter))
        layout.addWidget(self.prob_label)
        layout.addWidget(QLabel("Extracted LSB Message:"))
        layout.addWidget(self.lsb_output)

    def setup_visual_tab(self):
        layout = QHBoxLayout(self.tab_visual)
        self.img_original = QLabel("No Image Loaded")
        self.img_original.setAlignment(Qt.AlignCenter)
        
        self.img_plane = QLabel("No Bit-Plane Loaded")
        self.img_plane.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.img_original)
        layout.addWidget(self.img_plane)

    def setup_forensics_tab(self):
        layout = QVBoxLayout(self.tab_forensics)
        self.metadata_box = QTextEdit()
        self.metadata_box.setReadOnly(True)
        self.eof_box = QTextEdit()
        self.eof_box.setReadOnly(True)
        
        layout.addWidget(QLabel("Metadata / EXIF Findings:"))
        layout.addWidget(self.metadata_box)
        layout.addWidget(QLabel("EOF / Trailing Data:"))
        layout.addWidget(self.eof_box)

    def setup_batch_tab(self):
        layout = QVBoxLayout(self.tab_batch)
        self.batch_table = QTableWidget(0, 3)
        self.batch_table.setHorizontalHeaderLabels(["File Name", "Probability", "Status"])
        self.batch_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.batch_table)

    # --- LOGIC ---
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            self.start_analysis()

    def start_analysis(self):
        self.status_label.setText(f"Analyzing {os.path.basename(self.image_path)}...")
        self.progress.show()
        
        self.worker = AnalysisWorker(self.image_path)
        self.worker.finished.connect(self.update_ui)
        self.worker.error.connect(lambda e: self.status_label.setText(f"Error: {e}"))
        self.worker.start()

    @Slot(dict)
    def update_ui(self, results):
        self.progress.hide()
        self.status_label.setText("Analysis Complete.")
        
        # Update AI Tab
        self.prob_label.setText(f"{results['probability']*100:.2f}%")
        self.lsb_output.setText(results['lsb_data'] or "No data found.")
        
        # Update Forensics Tab
        self.metadata_box.setText("\n".join(results['metadata']) or "No metadata found.")
        self.eof_box.setText(results['eof_data'].decode('utf-8', errors='ignore') if results['eof_data'] else "No EOF data found.")
        
        # Update Visual Tab
        hunter = StegHunter(self.image_path)
        
        # Original Image
        orig_img = Image.open(self.image_path)
        orig_img.thumbnail((400, 400))
        self.set_qlabel_image(self.img_original, orig_img)
        
        # Bit Plane 0
        plane_img = hunter.get_bit_plane_0()
        plane_img.thumbnail((400, 400))
        self.set_qlabel_image(self.img_plane, plane_img)

    def set_qlabel_image(self, label, pil_img):
        # Convert PIL image to QPixmap
        data = pil_img.tobytes("raw", "RGB") if pil_img.mode == 'RGB' else pil_img.tobytes("raw", "L")
        qimg = QImage(data, pil_img.size[0], pil_img.size[1], QImage.Format_RGB888 if pil_img.mode == 'RGB' else QImage.Format_Grayscale8)
        label.setPixmap(QPixmap.fromImage(qimg))

    def batch_scan(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if not folder: return
        
        self.batch_table.setRowCount(0)
        files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        for f in files:
            path = os.path.join(folder, f)
            hunter = StegHunter(path)
            res = hunter.run_full_analysis()
            
            row = self.batch_table.rowCount()
            self.batch_table.insertRow(row)
            self.batch_table.setItem(row, 0, QTableWidgetItem(f))
            self.batch_table.setItem(row, 1, QTableWidgetItem(f"{res['probability']*100:.2f}%"))
            
            status = "⚠️ Suspect" if res['probability'] > 0.5 else "✅ Clean"
            self.batch_table.setItem(row, 2, QTableWidgetItem(status))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StegHunterPro()
    window.show()
    sys.exit(app.exec())
