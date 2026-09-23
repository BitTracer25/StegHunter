# 🕵️‍♂️ StegHunter Pro: AI-Powered Steganalysis Suite

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/Deep Learning-PyTorch-ee4c2c)](https://pytorch.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20%7C%20Streamlit-green)](https://pyside6.gs)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**StegHunter Pro** is a professional-grade digital forensics framework designed for the detection, analysis, and extraction of hidden data (steganography) within digital images. By integrating traditional statistical analysis with modern Deep Learning, StegHunter provides a multi-layered defense against common and advanced data-hiding techniques.

---

## 📖 Table of Contents

- [Problem Statement](#-problem-statement)
- [Technical Architecture](#-technical-architecture)
- [Detection Methodology](#-detection-methodology)
- [Feature Breakdown](#-feature-breakdown)
- [Installation & Setup](#-installation--setup)
- [🚀 Detailed Usage Guide](#-detailed-usage-guide)
- [Project Structure](#-project-structure)
- [Performance & Accuracy](#-performance--accuracy)
- [License](#-license)

---

## 🎯 Problem Statement

Steganography allows users to hide secret information within an innocuous cover image. Traditional detection methods (like simple LSB extraction) fail when:

1. The payload is very small (low signal-to-noise ratio).
2. The data is encrypted, making it look like random noise.
3. Data is hidden in metadata or appended to the file end rather than the pixels.

**StegHunter Pro** solves this by implementing a **Hybrid Detection Pipeline** that analyzes the image from three different perspectives: Global Statistics, Spatial Patterns, and File Structure.

---

## ⚙️ Technical Architecture

StegHunter is built on a **Modular Engine Architecture**. The core logic is decoupled from the user interfaces, allowing the same "Brain" to power three different front-ends:

1. **The Core Engine (`stego/engine.py`):** Handles all mathematical computations, AI inference, and file parsing.
2. **Pro Desktop App:** A high-performance PySide6 application for deep-dive forensics.
3. **Lite Web App:** A Streamlit-based dashboard for rapid triage.
4. **CLI Tool:** A lightweight interface for automation and scripting.

---

## 🔬 Detection Methodology

### 1. Statistical Analysis (The "First Pass")

The tool calculates two primary metrics to identify anomalies:

- **Chi-Square Analysis (χ²):** Measures the distribution of "Pairs of Values" (PoVs). In natural images, the frequency of pixel value 2n and 2n+1 is usually distinct. Steganography balances these, which the χ² test detects.
- **LSB Entropy:** Calculates the Shannon Entropy of the least significant bits. Encrypted payloads increase the randomness (entropy) of the LSB plane.

### 2. Deep Learning (The "Heavy AI")

We implement a **Convolutional Neural Network (CNN)** using PyTorch.

- **Input:** 128 × 128 RGB Image Tensors.
- **Layers:** 3 Convolutional layers with ReLU activation and Max-Pooling to extract spatial hierarchies.
- **Output:** A Sigmoid activation function providing a probability score (0.0 to 1.0).

### 3. Hybrid Heuristics (The "Safety Net")

To prevent False Negatives (missing small messages), the engine employs a **Text Density Check**. If the AI is uncertain but the extractor finds a high density of printable ASCII characters, the probability is automatically boosted to 85%.

---

## ✨ Feature Breakdown

| Feature | Description | Technology |
| :--- | :--- | :--- |
| **AI Probability** | Predicts the likelihood of hidden data via CNN and Random Forest. | PyTorch / Scikit-Learn |
| **LSB Extraction** | Recovers binary data hidden in the 0th bit of RGB channels. | NumPy / Pillow |
| **Bit-Plane Slicing** | Visualizes the 0th bit plane to reveal artificial patterns. | NumPy / Pillow |
| **Metadata Scan** | Extracts hidden strings from EXIF, XMP, and Image Info. | PIL.ExifTags |
| **EOF Analysis** | Scans for trailing data after the binary end-marker. | Binary File I/O |
| **Batch Processing** | Scans entire directories and flags suspect files. | PySide6 |

---

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.10+**
- **WSL2 (Windows Subsystem for Linux)** is highly recommended for the Desktop App.
- **GUI Server:** Windows 11 (WSLg) or VcXsrv (Windows 10).

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/BitTracer25/StegHunter.git
cd StegHunter

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Detailed Usage Guide

StegHunter provides three ways to interact with the engine depending on your needs:

### 🖥️ 1. Pro Desktop Application (Full Forensic Suite)

Designed for professional investigators who need visual proof and batch capabilities.

- **Launch:** `python3 desktop_app.py`
- **Workflow:**
  1. Click **"Open Image"** to select a target file.
  2. **AI Analysis Tab:** View the probability percentage and the extracted LSB text.
  3. **Visual Proof Tab:** Compare the original image with the **0th Bit-Plane Slice**. Patterns or blocks of noise here indicate steganography.
  4. **Forensics Tab:** Review the detailed Metadata and EOF analysis for hidden strings.
  5. **Batch Scan:** Click **"Batch Scan Folder"** to analyze a whole directory. The tool will generate a table flagging all "Suspect" images.

### 🌐 2. Lite Web Dashboard (Rapid Triage)

Designed for quick checks and ease of use via a browser.

- **Launch:** `streamlit run app.py`
- **Workflow:**
  1. Open the provided localhost URL in your browser.
  2. **Drag and Drop** an image into the uploader.
  3. Instantly view the **Stego Probability** and the **LSB Extraction** preview.

### ⌨️ 3. Command Line Interface (Automation)

Designed for power users, developers, and automated pipelines.

- **Usage:** `python3 main.py <image_path>`
- **Workflow:**
  1. Provide the path to the image as an argument.
  2. The tool outputs the AI probability and a preview of any extracted LSB data directly to the terminal.

---

## 📂 Project Structure

```text
StegHunter/
├── stego/                   # Core Logic
│   └── engine.py            # AI & Forensic Engine
├── desktop_app.py           # PySide6 Professional GUI
├── app.py                   # Streamlit Web App
├── main.py                  # Command Line Interface
├── train_cnn.py             # CNN Training Pipeline
├── train_model.py           # Random Forest Training Pipeline
├── generate_dataset.py      # Dataset Generator
├── stego_model.pkl          # Pre-trained RF Model
├── stego_cnn.pth            # Pre-trained CNN Model
└── requirements.txt         # Project Dependencies
```

---

## 📈 Performance & Accuracy

The tool was trained on a custom dataset of clean and stego-images.

- **Random Forest Accuracy:** ≈ 98% (on high-payload images).
- **CNN Detection:** Capable of detecting structured noise patterns that bypass basic χ² tests.
- **Extraction Rate:** 100% for standard LSB-encoded printable text.

---

## 📜 License

This project is licensed under the **MIT License**.

Copyright (c) 2024 BitTracer.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
