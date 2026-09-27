# StegHunter Pro

<<<<<<< HEAD
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red)
![GUI](https://img.shields.io/badge/GUI-PySide6%20%7C%20Streamlit-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
=======
StegHunter Pro is a desktop application for examining images for signs of hidden data. It combines two model scores with image checks and forensic details to help guide further investigation.

## Download and install
>>>>>>> 07fac01 (Changes in README)

Download the installer for your operating system from the [latest GitHub release](https://github.com/BitTracer25/StegHunter/releases/latest).

- **Windows:** Download and run `StegHunter-Pro-Setup-2.0.0.exe`, then open StegHunter Pro from the Start Menu.
- **Linux:** On Debian-based 64-bit distributions, including Kali, Ubuntu, and Debian, download and open `steg-hunter-pro_2.0.0_amd64.deb` with your software installer. After installation, open StegHunter Pro from the applications menu.

## What it does

- Analyzes PNG and JPEG images and displays Random Forest and CNN scores, along with their arithmetic mean.
- Looks for simple least significant bit (LSB) text payloads.
- Shows the image's least significant bit plane for visual inspection.
- Displays available image metadata and checks for data appended after the file’s end marker.
- Scans a folder of images and presents the results together.
- Includes a tool for hiding UTF-8 text in PNG images.

## Using the app

Open an image to view its analysis, extracted LSB text, bit-plane preview, metadata, and trailing-data findings. Use **Batch Scan Folder** to analyze multiple images.

When hiding text, save the resulting image as PNG. JPEG compression can alter pixel values and damage LSB payloads.

## Understanding results

Scores are indicators for investigation. They are not calibrated probabilities and do not prove that an image does or does not contain hidden data. Steganography methods vary, and this tool will not detect every method. Review the other findings and the original image as part of your assessment.

## License

StegHunter Pro is distributed under the MIT License.
