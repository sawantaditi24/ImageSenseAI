from PIL import Image
import pytesseract
import io

def extract_text_from_image(image_bytes: bytes) -> str:
    try:
        # Try to open and verify the image
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()  # Raises exception if image is not valid
        # Reopen after verify (verify() leaves the file in an unusable state)
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise ValueError(f"Invalid image data: {e}")
