# E-KYC Using Computer Vision

## Introduction

In this project, I’ve developed a web application using Streamlit that automates the Know Your Customer (KYC) process through computer vision techniques. Here’s how it works:

### User Interaction

When you visit our Streamlit web application, you’ll be prompted to upload two key pieces of information: a document and a photo. The document might include an ID card, passport, or any other form of identification. The photo should be a clear image of your face.

### Image Processing

Once you’ve uploaded both the document and the photo, the application begins by processing these images. The images are pre-processed to ensure they’re suitable for further analysis.

### Contour Detection

The next step involves detecting contours within the document image. This is done to identify and isolate the relevant sections of the document, such as text areas or identification numbers.

### Optical Character Recognition (OCR)

After contour detection, the application employs OCR technology to extract textual information from the document. This includes details like names, dates of birth, and document numbers.

### Face Validation

Concurrently, the face validation process begins. The application analyzes the uploaded photo and compares it with the face in the document. This step is crucial to ensure that the person in the photo matches the one on the document.

### Data Extraction and Storage

If the face validation is successful, the extracted data from the document and the photo are compiled and stored in a secure database. This data is used to verify the identity of the individual.

### Error Handling

If the face validation fails, the process is halted, and you will receive a message informing you of the mismatch. This ensures that only verified individuals proceed further.

This project showcases a comprehensive approach to automating the KYC process using advanced computer vision techniques, making it efficient and reliable.

Feel free to explore the application and see how it streamlines the verification process through cutting-edge technology!

## Techniques Used

- **Blurring**: GaussianBlur
- **Thresholding**: Adaptive Thresholding
- **Contour Detection**
- **Face Validation**: DeepFace
- **OCR**: EasyOCR
- **Face Detection**: CascadeClassifier

## Installation

Instructions for setting up the development environment and installing dependencies:

```bash
pip install -r requirements.txt


Usage
To use the web application, including uploading documents and photos:

streamlit run app.py

Technical Details
Libraries Installed: Streamlit, OpenCV, DeepFace, EasyOCR, scikit-learn, pandas, SQLAlchemy
Database Used: XAMPP with PHPMyAdmin for managing the MySQL database.
Error Handling and Configuration
Error Handling
For robust error management, the application employs Python’s built-in logging module. This ensures that all critical issues are logged systematically, allowing for easier debugging and monitoring of the application’s performance. The logging system captures detailed error messages and exceptions, which are essential for diagnosing issues and maintaining the reliability of the application.

Configuration Management
To bring standardization and flexibility to the application, we utilize a configuration.yaml file. This approach allows for parameterized configuration of various components of the system, including paths, thresholds, and other operational parameters. By externalizing configuration settings into a YAML file, we ensure that the codebase remains clean and adaptable. Users can easily modify configurations without altering the core application logic, promoting better maintainability and scalability.

The combination of detailed logging and a parameterized configuration file enhances the application’s resilience and adaptability, making it easier to manage and evolve over time.

License
This project is licensed under the [MIT License](LICENSE).


Contact Information
For any questions or suggestions, please contact:

Email: karanmakwana@gmail.com
GitHub: https://github.com/CodeCraftsmanML


