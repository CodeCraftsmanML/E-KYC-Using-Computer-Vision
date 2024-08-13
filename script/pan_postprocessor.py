import logging

def extract_pan_information(data_string):
    """
    I extract information from a formatted string and organize it into a dictionary.

    I first remove any periods from the data string and split it into words based on the "|" delimiter. 
    I then clean up each word by stripping extra spaces and discard any word with less than three characters. 

    I initialize a dictionary to hold the extracted information with default values.

    I then check if "Permanent Account Number Card" is mentioned in the data string. 
    If it is, I locate this term in the list of words and retrieve the ID immediately following it. 
    I also search for "name" and get the corresponding name from the string.

    If "Permanent Account Number Card" is not found, I look for "GOVT OF INDIA" and "Permanent Account Number". 
    If "GOVT OF INDIA" is present, I extract the name from the word following it. 
    Similarly, if "Permanent Account Number" is present, I extract the ID from the subsequent word.

    :param data_string: Raw data string containing the information.
    :return: A dictionary with extracted information including ID and Name.
    """
    updated_data_string = data_string.replace(".", "")
    words = [word.strip() for word in updated_data_string.split("|") if len(word.strip()) > 2]

    extracted_info = {
        "ID": "",
        "Name": "",
        "ID Type": "PAN"
    }

    try:
        if "Permanent Account Number Card" in updated_data_string:
            for i, word in enumerate(words):
                if "Permanent Account Number Card" in word:
                    extracted_info["ID"] = words[i + 1].strip()
                    break
            
            for i, word in enumerate(words):
                if "name" in word.lower():
                    extracted_info["Name"] = words[i + 1].strip()
                    break

        else:
            if "GOVT OF INDIA" in words:
                name_index = words.index("GOVT OF INDIA") + 1
                extracted_info["Name"] = words[name_index]
            
            if "Permanent Account Number" in words:
                id_index = words.index("Permanent Account Number") + 1
                extracted_info["ID"] = words[id_index]

    except Exception as e:
        logging.exception(f"Unexpected error during information extraction: {e}")

    return extracted_info
