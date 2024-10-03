from flask import Flask, render_template, request
from analysis import extract_text_from_image, analyze_ingredients_with_health, get_user_health_data, get_mock_weekly_summary
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the uploaded file
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            # Save the file to the upload folder
            filepath = os.path.join("upload", uploaded_file.filename)
            uploaded_file.save(filepath)

            # Perform OCR on the uploaded image
            extracted_text = extract_text_from_image(filepath)

            # Get mock data (replace with actual database queries when available)
            user_health_data = get_user_health_data(user_id=1)  # Mock user ID 1
            weekly_summary = get_mock_weekly_summary(user_id=1)

            # Analyze the ingredients with health and weekly data
            toxic_ingredients, healthy_ingredients, warnings = analyze_ingredients_with_health(extracted_text, weekly_summary, user_health_data)

            # Render the result to the user
            return render_template("index.html", toxic_ingredients=toxic_ingredients, healthy_ingredients=healthy_ingredients, warnings=warnings)

    return render_template("index.html", toxic_ingredients=None, healthy_ingredients=None, warnings=None)

if __name__ == "__main__":
    app.run(debug=True)
