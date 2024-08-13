import logging
import re

def extract_driving_license_information(data_string):
    """
    Extracts information from a formatted string into a dictionary specifically for Driving Licenses.

    :param data_string: Raw data string.
    :return: Dictionary with extracted information.
    """
    # Clean the input string by removing special characters except spaces
    updated_data_string = re.sub(r'[^\w\s]', '', data_string)
    words = updated_data_string.split()

    extracted_info = {
        "ID": "",
        "Name": "",
        "ID Type": "Driving License"
    }

    logging.info(f"Cleaned Data String: {updated_data_string}")
    logging.info(f"Words List: {words}")

    try:
        # Regex pattern for Driving License Number (format like "MH47 20220017016")
        dl_pattern = r'\b[A-Z]{2}[0-9]{2}\s*[0-9]{11}\b'

        # Extract Driving License Number and Name using the provided logic
        for item in data_string.splitlines():
            word = item.split()

            # Check for DL Number pattern in the line
            matches = re.findall(dl_pattern, item)
            if matches:
                extracted_info["DL No"] = matches[0].replace(' ', '')

            # Extract name assuming it appears after the word 'Name' in the string
            if "Name" in item:
                extracted_info["Name"] = item.split('Name')[-1].strip()

    except Exception as e:
        logging.exception(f"Unexpected error during Driving License information extraction: {e}")

    # Logging if fields are missing
    if extracted_info["DL No"] == "":
        logging.warning("Driving License number could not be extracted.")
    if extracted_info["Name"] == "":
        logging.warning("Name could not be extracted.")
    
    logging.info(f"Extracted information: {extracted_info}")

    return extracted_info
