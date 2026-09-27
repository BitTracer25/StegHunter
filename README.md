<div align="center">

# 🔎 StegHunter Pro

### See what's hidden in plain sight.

Inspect images for clues. Compare model scores. Explore pixel patterns and file details in one desktop app.

[![Latest Release](https://img.shields.io/badge/release-v2.0.0-7357d5?style=for-the-badge)](https://github.com/BitTracer25/StegHunter/releases/latest)
![Windows](https://img.shields.io/badge/Windows-x64-0078D4?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Debian%20based-FCC624?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-2ea44f?style=for-the-badge)

[Download StegHunter Pro](https://github.com/BitTracer25/StegHunter/releases/latest)

</div>

---

## 🧭 Explore

[Download & Install](#-download--install) · [What You Can Do](#-what-you-can-do) · [A Typical Review](#-a-typical-review) · [Understanding Scores](#-understanding-the-scores)

## 📦 Download & install

Get the installer for your system from the [latest release](https://github.com/BitTracer25/StegHunter/releases/latest).

| Your system | Release file | Install it |
| --- | --- | --- |
| 🪟 **Windows 64-bit** | `StegHunter-Pro-Setup-2.0.0.exe` | Run the installer, then open StegHunter Pro from the Start Menu. |
| 🐧 **Linux 64-bit** | `steg-hunter-pro_2.0.0_amd64.deb` | Open the package with your software installer, then launch the app from the applications menu. |

The Linux `.deb` package is for Debian-based distributions, including Kali, Debian, and Ubuntu.

## 🕵️ What you can do

<table>
<tr>
<td width="50%">

### 🧠 Compare model scores
Review the Random Forest and CNN scores, with their arithmetic mean shown as a summary.

</td>
<td width="50%">

### 🧩 Inspect LSB data
Look for text hidden in supported RGB least significant bit (LSB) formats.

</td>
</tr>
<tr>
<td width="50%">

### 🎨 Explore the bit plane
View the image's least significant bit plane for visual patterns that may merit a closer look.

</td>
<td width="50%">

### 🔬 Review file details
Inspect available metadata and check for data appended after the image's end marker.

</td>
</tr>
<tr>
<td colspan="2">

### 📂 Scan a folder
Analyze multiple PNG and JPEG images and review their results together.

</td>
</tr>
</table>

## 🚀 A typical review

1. **Open** a PNG or JPEG image.
2. **Review** the model scores and any extracted LSB text.
3. **Compare** the original image with its bit-plane view.
4. **Check** metadata and trailing-data findings.
5. **Batch scan** a folder to review a collection of images.

## 🖼️ Image formats

StegHunter can inspect PNG and JPEG images. PNG preserves pixel values; JPEG compression can change them and corrupt LSB data.

## 📊 Understanding the scores

Scores are clues for further investigation, not calibrated forensic probabilities. The displayed mean is the arithmetic average of the two model scores. Results depend on the image and the hiding method; a low score does not guarantee an image is clean.

> **Keep context in view:** Steganography has many forms. StegHunter can help surface clues, but it cannot detect every method or prove that an image does or does not contain hidden data.

## 📜 License

StegHunter Pro is distributed under the MIT License.
