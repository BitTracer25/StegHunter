from PIL import Image

def hide_message(image_path, message, output_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    
    # Convert message to binary
    binary_msg = ''.join(format(ord(i), '08b') for i in message) + '00000000' # Add null terminator
    
    width, height = img.size
    msg_index = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Hide bits in R, G, and B channels
            channels = [r, g, b]
            for i in range(3):
                if msg_index < len(binary_msg):
                    # Replace the LSB with the message bit
                    channels[i] = (channels[i] & ~1) | int(binary_msg[msg_index])
                    msg_index += 1
            
            pixels[x, y] = tuple(channels)
            if msg_index >= len(binary_msg):
                img.save(output_path)
                print(f"[*] Message hidden successfully in {output_path}")
                return

# --- SETTINGS ---
input_img = "test.png"        # Your original image
secret_text = "Hello StegHunter! This is a secret message."
output_img = "stego_test.png"  # The new image with hidden data

hide_message(input_img, secret_text, output_img)
