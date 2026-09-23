import os
import random
import string
from PIL import Image

def hide_random_data(image_path, output_path):
    """Hides a random string of data in an image to create a stego sample."""
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    
    # Generate a random string of random length
    length = random.randint(10, 500)
    random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    binary_msg = ''.join(format(ord(i), '08b') for i in random_text)
    
    width, height = img.size
    msg_index = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            channels = [r, g, b]
            for i in range(3):
                if msg_index < len(binary_msg):
                    channels[i] = (channels[i] & ~1) | int(binary_msg[msg_index])
                    msg_index += 1
            pixels[x, y] = tuple(channels)
            if msg_index >= len(binary_msg):
                img.save(output_path)
                return

def build_dataset(seed_folder, samples_per_image=10):
    """Creates a dataset of clean and stego images."""
    # Create folders
    os.makedirs("dataset/clean", exist_ok=True)
    os.makedirs("dataset/stego", exist_ok=True)
    
    seed_images = [f for f in os.listdir(seed_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not seed_images:
        print(f"[!] No images found in {seed_folder}")
        return

    print(f"[*] Found {len(seed_images)} seed images. Generating {len(seed_images) * samples_per_image * 2} samples...")

    for img_name in seed_images:
        img_path = os.path.join(seed_folder, img_name)
        
        for i in range(samples_per_image):
            # 1. Create a Clean Sample
            clean_path = f"dataset/clean/{img_name}_{i}.png"
            Image.open(img_path).convert('RGB').save(clean_path)
            
            # 2. Create a Stego Sample
            stego_path = f"dataset/stego/{img_name}_{i}.png"
            hide_random_data(img_path, stego_path)

    print("[+] Dataset created successfully in /dataset folder!")

if __name__ == "__main__":
    # 1. Create a folder called 'seeds' and put 5-10 random images in it first!
    seed_dir = "seeds" 
    if not os.path.exists(seed_dir):
        os.makedirs(seed_dir)
        print(f"[!] Please put some images in the '{seed_dir}' folder and run this again.")
    else:
        build_dataset(seed_dir)
