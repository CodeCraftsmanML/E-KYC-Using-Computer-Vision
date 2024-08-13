import cv2
import os
import numpy as np
import logging
from utilities import read_yaml, file_exists

# Setup logging configuration
logging_str = "[%(levelname)s]: %(message)s"

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"),
                    level=logging.INFO, format=logging_str, filemode="a")

# Read configuration from YAML file
config_path = "configuration.yaml"
config = read_yaml(config_path)

artifacts = config["artifacts"]
intermediate_dir_path = artifacts["intermediate_directory_path"]
contour_file_name = artifacts["contour_image_file_name"]

def read_image(image_path, is_uploaded=False):
    """
    I read an image from a file path or an uploaded file.

    If the image is uploaded, I decode the image bytes; otherwise, I read the image from the local file system.

    :param image_path: Path to the image file or uploaded file. If uploaded, this should be a file-like object.
    :param is_uploaded: Boolean indicating if the image is uploaded. Default is False.
    :return: Image as a numpy array if successful, or None if an error occurs.
    """
    try:
        if is_uploaded:
            image_bytes = image_path.read()
            img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        else:
            img = cv2.imread(image_path)

        if img is None:
            raise ValueError(f"Failed to read image from {image_path}")

        return img
    
    except Exception as e:
        logging.exception(f"Error loading image: {e}")
        print(f"Error loading image: {e}")
        return None

def extract_image_from_id(img):
    """
    I extract the largest contour from the input image (assumed to be an ID card) and save it.

    I process the image to detect contours, identify the largest contour based on area, and then extract this contour 
    from the image. Finally, I save the extracted contour to the specified path.

    :param img: Input image as a numpy array.
    :return: A tuple (contour_image, filename) where contour_image is the extracted contour image, 
             and filename is the name of the saved image file. Returns (None, None) if an error occurs.
    """
    try:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
        threshold_img = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        
        contours, _ = cv2.findContours(threshold_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        largest_contour = None
        largest_area = 0
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > largest_area:
                largest_contour = cnt
                largest_area = area
        
        if largest_contour is None or largest_area == 0:
            logging.warning("No contours found, or the largest contour has zero area.")
            return None, None
        
        x, y, w, h = cv2.boundingRect(largest_contour)
        logging.info(f"Contours are found at {(x, y, w, h)}")
        
        contour_id = img[y:y+h, x:x+w]
        filename = save_image(contour_id, contour_file_name, intermediate_dir_path)
        
        return contour_id, filename
    
    except Exception as e:
        logging.exception(f"Error extracting image from ID: {e}")
        print(f"Error extracting image from ID: {e}")
        return None, None

def save_image(image, filename, path):
    """
    I save an image to the specified directory path.

    I ensure that the directory exists, check if a file with the same name already exists, remove it if necessary, 
    and then save the new image.

    :param image: Image to save as a numpy array.
    :param filename: Filename for the saved image.
    :param path: Directory path where the image will be saved.
    :return: Full path of the saved image if successful, or None if an error occurs.
    """
    try:
        os.makedirs(path, exist_ok=True)  # Ensure the directory exists
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):  # Check if file already exists
            os.remove(full_path)  # Remove the existing file
        
        cv2.imwrite(full_path, image)  # Save the new image
        logging.info(f"Image saved successfully: {full_path}")  # Log success
        return full_path
    
    except Exception as e:
        logging.exception(f"Error saving image: {e}")  # Log error
        print(f"Error saving image: {e}")  # Print error message
        return None
