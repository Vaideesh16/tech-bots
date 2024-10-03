from flask import Flask, render_template, request, jsonify
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

# Function to analyze the ingredients
def analyze_ingredients(ingredients):
    unhealthy = {
        "Sugar": "Excess sugar can lead to weight gain and diabetes",
        "Hydrogenated Vegetable Oil": "Increases bad cholesterol, risk of heart disease",
        "Monosodium Glutamate": "Can cause headaches and other reactions in sensitive individuals",
    }
    healthy = {
        "Rice": "Good source of energy and essential nutrients.",
        "Onion": "Rich in antioxidants and has anti-inflammatory properties.",
        "Tomato": "Rich in vitamins and antioxidants.",
    }

    found_unhealthy = {ingredient: unhealthy[ingredient] for ingredient in unhealthy if ingredient in ingredients}
    found_healthy = {ingredient: healthy[ingredient] for ingredient in healthy if ingredient in ingredients}

    return found_unhealthy, found_healthy

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        # Save the uploaded file
        image_path = os.path.join('upload', file.filename)
        file.save(image_path)

        # Perform OCR to extract text from the image
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img)

        # Analyze the ingredients
        ingredients = extracted_text.split(',')
        unhealthy, healthy = analyze_ingredients([ingredient.strip() for ingredient in ingredients])

        # Prepare the response
        response = {
            "unhealthy": unhealthy,
            "healthy": healthy
        }

        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
