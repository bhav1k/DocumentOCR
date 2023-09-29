import cv2
import pytesseract
from pdf2image import convert_from_path
import tempfile
import os
import argparse

# Function to extract text from an image using Tesseract
def extract_text_from_image(image_path):

    image = cv2.imread(image_path) # Read the image using OpenCV

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert image to greyscale

    denoised_image = cv2.medianBlur(gray, 3) # Using a median filter to remove pepper noise

    preprocessed_image = cv2.adaptiveThreshold(denoised_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 4) # Using thresholding to improve text visibility

    text = pytesseract.image_to_string(preprocessed_image) # Tesseract does its job

    text = text.strip() # Removing whitespace
    return text

# Function to extract text from a PDF using Tesseract
def extract_text_from_pdf(pdf_path):

    images = convert_from_path(pdf_path) # Converts PDF to a list of images

    temp_dir = tempfile.mkdtemp() # Create a tmp dir for storing the images

    image_paths = [] # Save the temp files for further processing
    for i, image in enumerate(images):
        image_path = os.path.join(temp_dir, f"page_{i}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)

    extracted_text = [] # Extract text from all images one by one and store in a single variable
    for image_path in image_paths:
        text = extract_text_from_image(image_path)
        if text:
            extracted_text.append(text)

    separator = "\n" # Removing the newline separator
    text = separator.join(extracted_text)
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from an image or PDF.") # Adding a cmd line argument parser
    parser.add_argument("input_file", help="Path to the input image or PDF file") # The requied argument which will provide input file path

    args = parser.parse_args()
    input_file = args.input_file

    if input_file.lower().endswith(".pdf"): # Check file type and call the appropriate function
        extracted_text = extract_text_from_pdf(input_file)
    elif input_file.lower().endswith((".jpg", ".jpeg", ".png")):
        extracted_text = extract_text_from_image(input_file)
    else:
        print("Unsupported file type") # Report unsupported file if not an image or PDF
        quit()
    if extracted_text: # Print output if successful else report failure
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("Text extraction failed.")