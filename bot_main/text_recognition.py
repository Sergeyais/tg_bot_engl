import pytesseract
from PIL import Image

def recognition_eng_and_rus(path_image: str) -> str:
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image = Image.open(path_image)
    text = pytesseract.image_to_string(image, lang='eng+rus')
    return text


