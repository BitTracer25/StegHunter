import os
import re
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score
import joblib

def calculate_entropy(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.getdata()
    lsbs = [val & 1 for pixel in pixels for val in pixel]
    count_0, count_1 = lsbs.count(0), lsbs.count(1)
    total = len(lsbs)
    if total == 0: return 0
    p0, p1 = count_0 / total, count_1 / total
    entropy = 0
    if p0 > 0: entropy -= p0 * np.log2(p0)
    if p1 > 0: entropy -= p1 * np.log2(p1)
    return entropy

def get_chi_square(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.getdata()
    flat_pixels = [val for pixel in pixels for val in pixel]
    counts = [0] * 256
    for val in flat_pixels: counts[val] += 1
    chi_sq_stat, observed_pairs = 0, 0
    for i in range(0, 256, 2):
        val_even, val_odd = counts[i], counts[i+1]
        expected = (val_even + val_odd) / 2
        if expected > 0:
            chi_sq_stat += ((val_even - expected)**2 / expected) + ((val_odd - expected)**2 / expected)
            observed_pairs += 1
    return chi_sq_stat / observed_pairs if observed_pairs > 0 else 0

def prepare_dataset():
    data = []
    groups = []
    for label, folder in [(0, "dataset/clean"), (1, "dataset/stego")]:
        if not os.path.isdir(folder):
            raise FileNotFoundError(f"Training folder not found: {folder}")
        for img_name in os.listdir(folder):
            path = os.path.join(folder, img_name)
            if not os.path.isfile(path):
                continue
            data.append([get_chi_square(path), calculate_entropy(path), label])
            # Generated variants from the same seed image share a group, avoiding
            # near-duplicate images leaking into both train and validation sets.
            groups.append(re.sub(r"_\d+$", "", os.path.splitext(img_name)[0]))
    if not data:
        raise ValueError("No training images found in dataset/clean and dataset/stego")
    return pd.DataFrame(data, columns=['chi_square', 'entropy', 'label']), np.asarray(groups)

if __name__ == "__main__":
    df, groups = prepare_dataset()
    X = df[['chi_square', 'entropy']]
    y = df['label']
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(splitter.split(X, y, groups))
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    print(f"[+] Accuracy: {accuracy_score(y_test, model.predict(X_test)) * 100:.2f}%")
    joblib.dump(model, "stego_model.pkl")
    print("[+] Model saved as 'stego_model.pkl'")
