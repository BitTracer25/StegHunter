"""Helpers for a small, length-prefixed UTF-8 LSB payload format."""

from PIL import Image

MAGIC = b"STGH"


def embed_text(input_path, text, output_path):
    if not output_path.lower().endswith(".png"):
        raise ValueError("LSB payloads must be saved as PNG to preserve their bits")

    image = Image.open(input_path).convert("RGB")
    payload = text.encode("utf-8")
    framed = MAGIC + len(payload).to_bytes(4, "big") + payload
    bits = [(byte >> shift) & 1 for byte in framed for shift in range(7, -1, -1)]
    capacity = image.width * image.height * 3
    if len(bits) > capacity:
        raise ValueError(f"Payload needs {len(bits)} bits; image holds {capacity} bits")

    pixels = image.load()
    bit_index = 0
    for y in range(image.height):
        for x in range(image.width):
            channels = list(pixels[x, y])
            for channel in range(3):
                if bit_index >= len(bits):
                    break
                channels[channel] = (channels[channel] & 0xFE) | bits[bit_index]
                bit_index += 1
            pixels[x, y] = tuple(channels)
            if bit_index >= len(bits):
                image.save(output_path, format="PNG")
                return
    image.save(output_path, format="PNG")
