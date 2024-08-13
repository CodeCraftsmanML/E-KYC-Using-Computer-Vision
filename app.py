import os
import logging
import streamlit as st
from preprocessor import read_image, extract_image_from_id, save_image
from OCR import extract_text
from aadhar_postprocessor import extract_aadhaar_information
from pan_postprocessor import extract_pan_information
from validation import detect_and_extract_face, face_comparison, get_face_embeddings
from dbms_operations import insert_records, fetch_records, check_duplicacy

# Configure logging
logging_str = "[%(levelname)s]: %(message)s"

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "ekyc_logs.log"),
    level=logging.INFO,
    format=logging_str,
    filemode="a"
)

def sidebar_section():
    """
    Create a sidebar in the Streamlit app that allows users to select the type of ID card they are uploading.
    The selected option is then returned for further processing.
    """
    st.sidebar.title("Select ID Card Type")
    option = st.sidebar.selectbox("", ("PAN", "Aadhar", "Driving License"))
    logging.info(f"ID card type selected: {option}")
    return option

def header_section(option):
    """
    Set the header of the Streamlit app based on the selected ID card type.
    This helps in guiding the user through the appropriate registration process.
    """
    if option == "Aadhar":
        st.title("Registration Using Aadhar Card")
        logging.info("Header set for Aadhar Card registration.")
    elif option == "PAN":
        st.title("Registration Using PAN Card")
        logging.info("Header set for PAN Card registration.")
    elif option == 'Driving License':
        st.title("Registration using Driving License")
        logging.info("Header set for Driving License")

def main_content(image_file, face_image_file, option):
    if image_file is not None and face_image_file is not None:
        face_image = read_image(face_image_file, is_uploaded=True)  
        # Read face image
        logging.info("Face image loaded.")

        if face_image is not None:
            image = read_image(image_file, is_uploaded=True)  
            # Read ID card image
            logging.info("ID card image loaded.")
            
            image_roi, _ = extract_image_from_id(image)  
            # Extract ID card region of interest
            logging.info("ID card ROI extracted.")
            
            face_image_path2 = detect_and_extract_face(img=image_roi)  
            # Detect and extract face from ID card
            face_image_path1 = save_image(face_image, "face_image.jpg", path="S:\\Machine Learning\\Siddharthan Playlist\\KYC Final\\Data\\faces")  # Save face image
            logging.info("Faces extracted and saved.")
            
            is_face_verified = face_comparison(image1_path=face_image_path1, image2_path=face_image_path2)  
            # Compare faces
            logging.info(f"Face verification status: {'successful' if is_face_verified else 'failed'}.")

            if is_face_verified:
                extracted_text = extract_text(image_roi)  
                
                if option == "PAN":
                    # Extract Aadhar information
                    text_info = extract_pan_information(extracted_text)  
                # elif option == "Aadhar":
                #     # Extract PAN information
                #     text_info = extract_pan_information(extracted_text)  
                # else:
                #     st.error("Unsupported ID card type.")
                #     return

                logging.info("Text extracted and information parsed from ID card.")
                
                # Fetch records from the database
                records = fetch_records(text_info)  
                
                if not records.empty and 'Name' in records.columns:
                    st.write(f"{records['Name'].iloc[0]} Verified")
                else:
                    # st.error("Name not found in records.")
                    pass 
                    
                # Check for duplicate records    
                is_duplicate = check_duplicacy(text_info)  
                if is_duplicate:
                    st.write(f"User already present with ID {text_info['ID']}")
                else:
                    st.write(text_info)
                    
                    # Get face embeddings
                    text_info['Embedding'] = get_face_embeddings(face_image_path1)  
                    
                    # Insert new record into the database
                    insert_records(text_info)  
                    logging.info(f"New user record inserted: {text_info['ID']}")
                    
            else:
                st.error("Face verification failed. Please try again.")
                
        else:
            st.error("Face image not uploaded. Please upload a face image.")
            logging.error("No face image uploaded.")
            
    elif image_file is None:
        st.warning("Please upload an ID card image.")
        logging.warning("No ID card image uploaded.")
    elif face_image_file is None:
        st.warning("Please upload a face image.")
        logging.warning("No face image uploaded.")

def main():
    """
    Set up the Streamlit app, handle user inputs, and process the uploaded files.
    """
    # Get the selected ID card type
    option = sidebar_section()  
    header_section(option)
    
    image_file = st.file_uploader("Upload ID Card")
    
    if image_file is not None:
        face_image_file = st.file_uploader("Upload Face Image")
        
        if face_image_file is not None:
            # Process images and handle content
            main_content(image_file, face_image_file, option)  
        else:
            st.warning("Please upload a face image.")
    else:
        st.warning("Please upload an ID card image.")

if __name__ == "__main__":
    main()
