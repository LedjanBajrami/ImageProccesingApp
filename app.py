from flask import Flask, render_template, request, redirect, url_for, send_file
import cv2
import os
import numpy as np

app = Flask(__name__)

# Set up a folder for uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to apply a basic image processing operation (brightness adjustment)
def process_image(image_path, brightness_factor):
    image = cv2.imread(image_path)
    image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)
    return image

# Function to apply a contrast adjustment
def process_contrast(image_path, contrast_factor):
    image = cv2.imread(image_path)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Apply contrast adjustment to the L channel (luminance)
    l = cv2.convertScaleAbs(l, alpha=contrast_factor)

    lab = cv2.merge((l, a, b))
    adjusted_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    return adjusted_image

# Function to convert the image to grayscale
def process_grayscale(image_path):
    image = cv2.imread(image_path)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(grayscale_image, cv2.COLOR_GRAY2BGR)

# Function to apply Gaussian blur to the image
def process_blur(image_path, kernel_size):
    image = cv2.imread(image_path)
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return blurred_image

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return redirect(request.url)

    image_file = request.files['image']

    if image_file.filename == '':
        return redirect(request.url)

    if image_file:
        # Save the uploaded image
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(filename)

        # Determine which operation to perform based on the button clicked
        operation = request.form.get('operation')

        if operation == 'brightness':
            # Apply a basic image processing operation (brightness adjustment)
            brightness_factor = 1.5
            processed_image = process_image(filename, brightness_factor)
        elif operation == 'contrast':
            # Apply another image processing operation (contrast adjustment)
            contrast_factor = 1.5
            processed_image = process_contrast(filename, contrast_factor)
        elif operation == 'grayscale':
            # Apply the grayscale conversion operation
            processed_image = process_grayscale(filename)
        elif operation == 'blur':
            # Apply Gaussian blur with a kernel size of 5
            kernel_size = 9
            processed_image = process_blur(filename, kernel_size)
        else:
            # Default to brightness adjustment if no operation is specified
            brightness_factor = 0
            processed_image = process_image(filename, brightness_factor)

        # Save the processed image
        processed_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + image_file.filename)
        cv2.imwrite(processed_filename, processed_image)

        return send_file(processed_filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
