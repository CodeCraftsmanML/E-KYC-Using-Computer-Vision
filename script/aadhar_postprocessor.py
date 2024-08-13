import logging
import re

def extract_aadhaar_information(data_string):
    """
    Extracts information from a formatted string into a dictionary specifically for Aadhaar cards.

    :param data_string: Raw data string.
    :return: Dictionary with extracted information.
    """
    # Clean the input string by removing special characters except spaces
    updated_data_string = re.sub(r'[^\w\s]', '', data_string)
    words = updated_data_string.split()

    extracted_info = {
        "ID": "",
        "Name": "",
        "ID Type": "Aadhaar"
    }

    logging.info(f"Cleaned Data String: {updated_data_string}")
    logging.info(f"Words List: {words}")

    try:
        # Regex pattern for Aadhaar Number (12 digits with optional spaces or hyphens)
        aadhaar_pattern = r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'

        # Initialize Name and Aadhaar ID variables
        Name = None
        Aadhar_id = None

        # Extract Aadhaar Number and Name using the provided logic
        for item in data_string.splitlines():
            word = item.split()

            # Check for Aadhaar ID (12 digits) in the line
            matches = re.findall(aadhaar_pattern, item)
            if matches:
                extracted_info["ID"] = matches[0].replace(' ', '').replace('-', '')

            # Extract name assuming it does not contain 'Government' and starts with a letter
            if len(word) > 1 and (word[0] != 'Government' and word[0].isalpha()):
                extracted_info["Name"] = item

    except Exception as e:
        logging.exception(f"Unexpected error during Aadhaar information extraction: {e}")

    # Logging if fields are missing
    if extracted_info["ID"] == "":
        logging.warning("Aadhaar number could not be extracted.")
    if extracted_info["Name"] == "":
        logging.warning("Name could not be extracted.")
    
    logging.info(f"Extracted information: {extracted_info}")

    return extracted_info
