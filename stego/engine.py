import os
import math
import numpy as np
import joblib
import pandas as pd
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
from PIL.ExifTags import TAGS

# --- CNN ARCHITECTURE (Must be outside the StegHunter class) ---
class StegCNN(nn.Module):
    def __init__(self):
        super(StegCNN, self).__init__()
        self.conv_layer = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(), 
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(), 
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(), 
            nn.MaxPool2d(2)
        )
        self.fc_layer = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 16 * 16, 128), # Corrected shape for 128x128 input
            nn.ReLU(), 
            nn.Linear(128, 1), 
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.conv_layer(x)
        x = self.fc_layer(x)
        return x

# --- CORE ENGINE ---
class StegHunter:
    def __init__(self, image_path=None):
        self.image_path = image_path
        self.image = self._load_image() if image_path else None
        self.extracted_data = ""
        
        # Load the CNN Model
        try:
            self.cnn_model = StegCNN()
            # map_location ensures it works on both CPU and GPU
            self.cnn_model.load_state_dict(torch.load("stego_cnn.pth", map_location=torch.device('cpu')))
            self.cnn_model.eval()
        except Exception as e:
            print(f"[!] Model Load Error: {e}")
            self.cnn_model = None

    def _load_image(self):
        try:
            if not self.image_path: return None
            img = Image.open(self.image_path)
            return img.convert('RGB')
        except Exception as e:
            print(f"[!] Load Error: {e}")
            return None

    # --- FORENSIC TOOLS ---
    def scan_metadata(self):
        findings = []
        try:
            img = Image.open(self.image_path)
            info = img._getexif()
            if info:
                for tag, value in info.items():
                    findings.append(f"{TAGS.get(tag, tag)}: {value}")
            for key, value in img.info.items():
                findings.append(f"{key}: {value}")
        except: pass
        return findings

    def scan_eof(self):
        try:
            with open(self.image_path, 'rb') as f:
                content = f.read()
                marker = b'\xff\xd9' if self.image_path.lower().endswith(('.jpg', '.jpeg')) else b'\x49\x45\x4e\x44\xae\x42\x60\x82'
                pos = content.rfind(marker)
                if pos != -1: return content[pos + len(marker):]
        except: pass
        return None

    def get_bit_plane_0(self):
        if self.image is None: return None
        pixels = np.array(self.image)
        lsb_plane = (pixels[:, :, 0] & 1) * 255 
        return Image.fromarray(lsb_plane.astype('uint8'), 'L')

    # --- AI & LSB LOGIC ---
    def analyze_ai(self):
        """Deep Learning Prediction using the CNN."""
        if self.image is None or self.cnn_model is None: return 0.0
        
        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
        ])
        img_tensor = transform(self.image).unsqueeze(0)
        
        with torch.no_grad():
            prediction = self.cnn_model(img_tensor)
            prob = prediction.item()
            
        return round(prob, 4)

    def extract_lsb(self):
        if self.image is None: return None
        binary = "".join([str(val & 1) for pixel in self.image.getdata() for val in pixel])
        all_bytes = [binary[i:i+8] for i in range(0, len(binary), 8)]
        decoded = ""
        for b in all_bytes:
            try: decoded += chr(int(b, 2))
            except: continue
        self.extracted_data = decoded
        return decoded

    def run_full_analysis(self):
        if self.image is None: return None
        
        ai_prob = self.analyze_ai()
        lsb_res = self.extract_lsb()
        
        final_prob = ai_prob
        if lsb_res:
            # Analyze the first 200 characters for a better sample size
            sample = lsb_res[:200]
            if len(sample) > 0:
                # 1. Count printable characters (ASCII 32 to 126)
                printable_count = sum(1 for c in sample if 32 <= ord(c) <= 126)
                printable_ratio = printable_count / len(sample)
                
                # 2. Count alphabetical characters
                alpha_count = sum(1 for c in sample if c.isalpha())
                alpha_density = alpha_count / len(sample)
                
                # STRICT HYBRID LOGIC:
                # Real text is usually > 90% printable AND > 30% alphabetical.
                # Random noise is usually < 40% printable.
                if printable_ratio > 0.90 and alpha_density > 0.30:
                    final_prob = max(ai_prob, 0.85) # High confidence hit
                elif printable_ratio > 0.70 and alpha_density > 0.15:
                    final_prob = max(ai_prob, 0.40) # Potential hit
        
        return {
            "probability": round(final_prob, 4),
            "lsb_data": lsb_res,
            "metadata": self.scan_metadata(),
            "eof_data": self.scan_eof()
        }
