# 🕵️‍♂️ StegHunter Pro: AI-Powered Steganalysis Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/Deep%20Learning-PyTorch-ee4c2c)](https://pytorch.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20%7C%20Streamlit-green)](https://pyside6.gs)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**StegHunter Pro** is a comprehensive digital forensics framework designed for the detection, analysis, and extraction of hidden data (steganography) within digital images. By integrating traditional statistical analysis with modern Deep Learning, StegHunter provides a multi-layered defense against common and advanced data-hiding techniques.

---

## 📖 Table of Contents
- [Problem Statement](#-problem-statement)
- [Technical Architecture](#-technical-architecture)
- [Detection Methodology](#-detection-methodology)
- [Feature Breakdown](#-feature-breakdown)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Performance & Accuracy](#-performance--accuracy)

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
- **Chi-Square Analysis ($\chi^2$):** Measures the distribution of "Pairs of Values" (PoVs). In natural images, the frequency of pixel value $2n$ and $2n+1$ is usually distinct. Steganography balances these, which the $\chi^2$ test detects.
- **LSB Entropy:** Calculates the Shannon Entropy of the least significant bits. Encrypted payloads increase the randomness (entropy) of the LSB plane.

### 2. Deep Learning (The "Heavy AI")
We implement a **Convolutional Neural Network (CNN)** using PyTorch. 
- **Input:** $128 \times 128$ RGB Image Tensors.
- **Layers:** 3 Convolutional layers with ReLU activation and Max-Pooling to extract spatial hierarchies.
- **Output:** A Sigmoid activation function providing a probability score $(0.0 \text{ to } 1.0)$.

### 3. Hybrid Heuristics (The "Safety Net")
To prevent False Negatives (missing small messages), the engine employs a **Text Density Check**. If the AI is uncertain but the extractor finds a high density of printable ASCII characters, the probability is automatically boosted to $\mathbf{85\%}$.

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
