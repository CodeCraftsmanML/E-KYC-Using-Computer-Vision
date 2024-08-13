import os
import logging
import easyocr

# Setup logging configuration
logging_str = "[%(levelname)s]: %(message)s"

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"),
                    level=logging.INFO, format=logging_str, filemode="a")

def extract_text(image_path, confidence_threshold=0.10, language=['en']):
    """
    I extract text from an image using EasyOCR.

    :param image_path: Path to the image file.
    :param confidence_threshold: Minimum confidence level to include text.
    :param language: List of languages for OCR.
    :return: Extracted text as a string.
    """
    
    logging.info('Text extraction started') 
    
    reader = easyocr.Reader(language) 
    
    try:
        result = reader.readtext(image_path) 
        filtered_text = "" 
        for bounding_box, recognized_text, confidence in result:
            if confidence > confidence_threshold:
                filtered_text += recognized_text + "|"
                
        if filtered_text:
            logging.info('Text extraction completed successfully')
        else:
            logging.info('No text found above the confidence threshold')
            
        return filtered_text
    
    except Exception as e:
        logging.exception(f"An error occurred during text extraction: {e}")
        return ""
