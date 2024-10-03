from PIL import Image
import pytesseract

# Function to extract text from the uploaded image (OCR)
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text

# Mock user health data (this would come from a database eventually)
def get_user_health_data(user_id):
    return {
        "diabetes": True,
        "heart_disease": False,
        "high_blood_pressure": True,
    }

# Mock weekly consumption data (this would come from a database eventually)
def get_mock_weekly_summary(user_id):
    return {
        'calories': 2000,  # Example weekly total calories
        'fats': 600,       # Example weekly fat intake
        'sugars': 350,     # Example weekly sugar intake
        'fiber': 150,      # Example weekly fiber intake
        'oily_food': 3,    # Example oily food count for the week
    }

# Analyze ingredients considering health data and weekly consumption
def analyze_ingredients_with_health(extracted_text, weekly_data, health_data):
    toxic_ingredients = []
    healthy_ingredients = []
    warnings = []

    # Define toxic and healthy ingredients (you can expand these lists)
    toxic_list = {
        "sugar": "Sugar: High sugar is harmful for diabetic patients.",
        "hydrogenated vegetable oil": "Hydrogenated vegetable oil: Increases risk of heart disease.",
        "monosodium glutamate": "Monosodium glutamate: Can cause headaches in sensitive individuals."
    }

    healthy_list = {
        "carrot": "Carrot: Rich in vitamins, improves vision and skin health.",
        "peas": "Peas: High in fiber and protein, good for digestion and muscle repair.",
        "onion": "Onion: Contains antioxidants and helps reduce inflammation."
    }

    # Check for toxic ingredients in extracted text
    for ingredient, description in toxic_list.items():
        if ingredient in extracted_text.lower():
            toxic_ingredients.append(description)

    # Check for healthy ingredients in extracted text
    for ingredient, benefit in healthy_list.items():
        if ingredient in extracted_text.lower():
            healthy_ingredients.append(benefit)

    # Check user health conditions and issue warnings
    if 'sugar' in extracted_text.lower() and health_data["diabetes"]:
        warnings.append("Warning: This product contains sugar, which may be harmful for diabetic patients.")
    if 'hydrogenated vegetable oil' in extracted_text.lower() and health_data["heart_disease"]:
        warnings.append("Warning: This product contains hydrogenated vegetable oil, which is risky for heart patients.")

    # Check weekly consumption limits and provide warnings
    if weekly_data['sugars'] > 300:
        warnings.append("You have already consumed too much sugar this week.")
    if weekly_data['fats'] > 500:
        warnings.append("You have exceeded the recommended fat intake this week.")
    if weekly_data['oily_food'] > 2:
        warnings.append("You have eaten too many oily foods this week.")

    return toxic_ingredients, healthy_ingredients, warnings
