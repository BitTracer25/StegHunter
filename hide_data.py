from stego.lsb import embed_text

def hide_message(image_path, message, output_path):
    """Hide a UTF-8 message in an image and save it as lossless PNG."""
    embed_text(image_path, message, output_path)
    print(f"[*] Message hidden successfully in {output_path}")

# --- SETTINGS ---
input_img = "test.png"        # Your original image
secret_text = "Hello StegHunter! This is a secret message."
output_img = "stego_test.png"  # The new image with hidden data

hide_message(input_img, secret_text, output_img)
