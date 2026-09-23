import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import os

# --- 1. THE NEURAL NETWORK ARCHITECTURE ---
class StegCNN(nn.Module):
    def __init__(self):
        super(StegCNN, self).__init__()
        # Convolutional layers to find pixel patterns
        self.conv_layer = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1), # Input: RGB, Output: 16 filters
            nn.ReLU(),
            nn.MaxPool2d(2), # Reduce size
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        # Fully connected layers to classify as Clean (0) or Stego (1)
        self.fc_layer = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 16 * 16, 128), # Adjust size based on input image
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid() # Output between 0 and 1
        )

    def forward(self, x):
        x = self.conv_layer(x)
        x = self.fc_layer(x)
        return x

# --- 2. DATASET LOADER ---
class StegoDataset(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.images = []
        self.labels = []
        
        for label, folder in [(0, "clean"), (1, "stego")]:
            folder_path = os.path.join(root_dir, folder)
            for img_name in os.listdir(folder_path):
                self.images.append(os.path.join(folder_path, img_name))
                self.labels.append(label)

        self.transform = transforms.Compose([
            transforms.Resize((128, 128)), # Standardize size for CNN
            transforms.ToTensor(),
        ])

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img = Image.open(self.images[idx]).convert('RGB')
        label = torch.tensor([self.labels[idx]], dtype=torch.float32)
        return self.transform(img), label

# --- 3. TRAINING LOOP ---
def train():
    print("[*] Initializing Heavy AI Training...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Using device: {device}")

    dataset = StegoDataset("dataset")
    train_loader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    model = StegCNN().to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 5
    for epoch in range(epochs):
        total_loss = 0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {total_loss/len(train_loader):.4f}")

    torch.save(model.state_dict(), "stego_cnn.pth")
    print("[+] CNN Model saved as 'stego_cnn.pth'!")

if __name__ == "__main__":
    train()
