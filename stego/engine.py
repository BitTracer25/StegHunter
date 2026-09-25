import os
import sys
import numpy as np
import joblib
import sklearn.ensemble  # Ensure PyInstaller collects the classes used by the saved model.
from PIL import Image, ExifTags

class StegHunter:
    """
    Image steganalysis helpers using a Random Forest and basic LSB inspection.
    """
    def __init__(self, image_path=None):
        self.image_path = image_path
        self.image = self._load_image() if image_path else None
        self.extracted_data = ""
        self.model = None
        self.cnn_model = None
        self.model_errors = {}
        bundle_root = getattr(sys, "_MEIPASS", None)
        project_root = os.path.dirname(os.path.dirname(__file__))
        search_roots = [root for root in (bundle_root, project_root, sys.prefix) if root]

        for root in search_roots:
            model_path = os.path.join(root, "stego_model.pkl")
            if os.path.isfile(model_path):
                try:
                    self.model = joblib.load(model_path)
                    break
                except Exception as error:
                    self.model_errors["random_forest"] = str(error)
        if self.model is None and "random_forest" not in self.model_errors:
            self.model_errors["random_forest"] = "stego_model.pkl was not found"

        cnn_path = next(
            (os.path.join(root, "stego_cnn.pth") for root in search_roots
             if os.path.isfile(os.path.join(root, "stego_cnn.pth"))),
            None,
        )
        if cnn_path:
            try:
                import torch
                from train_cnn import StegCNN

                cnn = StegCNN()
                cnn.load_state_dict(torch.load(cnn_path, map_location="cpu", weights_only=True))
                cnn.eval()
                self.cnn_model = cnn
            except Exception as error:
                self.model_errors["cnn"] = str(error)
        else:
            self.model_errors["cnn"] = "stego_cnn.pth was not found"

    def _load_image(self):
        # (Function body remains the same)
        try:
            if not self.image_path: return None
            img = Image.open(self.image_path)
            return img.convert('RGB')
        except Exception as e:
            print(f"[!] Error loading image: {e}")
            return None

    # --- FORENSIC TOOLS ---
    def scan_metadata(self):
        findings = []
        try:
            img = Image.open(self.image_path)
            info = img._getexif()
            if info:
                for tag, value in info.items():
                    findings.append(f"{ExifTags.TAGS.get(tag, tag)}: {value}")
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
        """Returns an image of the 0th bit plane (LSB)."""
        if self.image is None: return None
        
        pixels = np.array(self.image)
        lsb_plane = (pixels[:, :, 0] & 1) * 255
        return Image.fromarray(lsb_plane.astype('uint8'), 'L')

    # --- AI & LSB LOGIC ---
    def _get_chi_square(self):
        if self.image is None: return 0.0
        counts = np.bincount(np.asarray(self.image).reshape(-1), minlength=256)
        chi_sq, pairs = 0, 0
        for i in range(0, 256, 2):
            even, odd = counts[i], counts[i+1]
            exp = (even + odd) / 2
            if exp > 0:
                chi_sq += ((even - exp)**2 / exp) + ((odd - exp)**2 / exp)
                pairs += 1
        return chi_sq / pairs if pairs > 0 else 0

    def _get_entropy(self):
        if self.image is None: return 0.0
        lsbs = np.asarray(self.image, dtype=np.uint8).reshape(-1) & 1
        c0, c1, total = int(np.count_nonzero(lsbs == 0)), int(np.count_nonzero(lsbs == 1)), lsbs.size
        if total == 0: return 0
        p0, p1 = c0 / total, c1 / total
        entropy = 0
        if p0 > 0: entropy -= p0 * np.log2(p0)
        if p1 > 0: entropy -= p1 * np.log2(p1)
        return entropy

    def analyze_models(self):
        scores = {}
        if self.image is None:
            return scores

        if self.model is not None:
            try:
                features = np.array([[self._get_chi_square(), self._get_entropy()]])
                if hasattr(self.model, "predict_proba"):
                    probabilities = self.model.predict_proba(features)[0]
                    classes = list(self.model.classes_)
                    scores["random_forest"] = (
                        float(probabilities[classes.index(1)]) if 1 in classes else 0.0
                    )
                else:
                    scores["random_forest"] = float(self.model.predict(features)[0] == 1)
            except Exception as error:
                self.model_errors["random_forest"] = str(error)

        if self.cnn_model is not None:
            try:
                import torch

                pixels = np.asarray(self.image.resize((128, 128)), dtype=np.float32) / 255.0
                tensor = torch.from_numpy(pixels).permute(2, 0, 1).unsqueeze(0)
                with torch.no_grad():
                    scores["cnn"] = float(self.cnn_model(tensor).item())
            except Exception as error:
                self.model_errors["cnn"] = str(error)
        return scores

    def analyze_ai(self):
        """Return the mean score from the available models for legacy callers."""
        scores = self.analyze_models()
        return float(np.mean(list(scores.values()))) if scores else 0.0

    def extract_lsb(self):
        # (Function body remains the same)
        if self.image is None: return None
        pixel_bits = (np.asarray(self.image, dtype=np.uint8).reshape(-1) & 1).tolist()
        all_bytes = bytes(
            sum(bit << (7 - j) for j, bit in enumerate(pixel_bits[i:i + 8]))
            for i in range(0, len(pixel_bits) - 7, 8)
        )
        magic = b"STGH"
        decoded = ""
        if all_bytes.startswith(magic) and len(all_bytes) >= 8:
            payload_length = int.from_bytes(all_bytes[4:8], "big")
            payload = all_bytes[8:8 + payload_length]
            if len(payload) == payload_length:
                decoded = payload.decode("utf-8", errors="replace")
        else:
            # Legacy payloads were null-terminated byte strings.
            payload = all_bytes.split(b"\x00", 1)[0]
            decoded = payload.decode("utf-8", errors="replace")
        self.extracted_data = decoded
        return decoded

    def run_full_analysis(self):
        if self.image is None: return None
        
        # --- Hybrid Logic ---
        model_scores = self.analyze_models()
        ai_prob = float(np.mean(list(model_scores.values()))) if model_scores else 0.0
        lsb_res = self.extract_lsb()
        
        final_prob = ai_prob
        if lsb_res:
            # 1. Analyze the first 200 characters for a better sample size
            sample = lsb_res[:200]
            if len(sample) > 0:
                # 2. Count printable and alphabetical characters
                printable_count = sum(1 for c in sample if 32 <= ord(c) <= 126)
                printable_ratio = printable_count / len(sample) if len(sample) > 0 else 0
                alpha_count = sum(1 for c in sample if c.isalpha())
                alpha_density = alpha_count / len(sample) if len(sample) > 0 else 0

                # 3. The Logic: Requires high printability AND sufficient alphabetical content
                if printable_ratio > 0.90 and alpha_density > 0.30:
                    final_prob = max(ai_prob, 0.85) 
                elif printable_ratio > 0.70 and alpha_density > 0.15:
                    final_prob = max(ai_prob, 0.40)

        return {
            "probability": round(final_prob, 4),
            "combined_score": round(ai_prob, 4),
            "model_available": bool(model_scores),
            "models_available": {
                "random_forest": self.model is not None,
                "cnn": self.cnn_model is not None,
            },
            "model_scores": model_scores,
            "model_errors": dict(self.model_errors),
            "lsb_data": lsb_res,
            "metadata": self.scan_metadata(),
            "eof_data": self.scan_eof()
        }
