import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import joblib

# Initialize the Flask application
app = Flask(__name__)

# --- Load the Trained Model ---
# Load the pre-trained machine learning pipeline
try:
    model = joblib.load("salary_prediction_pipeline_enhanced.joblib")
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ Error: Model file 'salary_prediction_pipeline_enhanced.joblib' not found.")
    print("Please make sure the model file is in the same directory as this script.")
    model = None
except Exception as e:
    print(f"❌ An error occurred while loading the model: {e}")
    model = None


# --- Define Routes ---

@app.route('/')
def home():
    """Renders the main page of the web application."""
    # The 'index.html' file should be in a folder named 'templates'
    # in the same directory as this script.
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives employee data from the web form, makes a prediction,
    and returns the result as JSON.
    """
    if model is None:
        return jsonify({'error': 'Model is not loaded. Cannot make predictions.'}), 500

    try:
        # Get the data from the POST request's form
        form_data = request.form.to_dict()
        
        # Convert numerical fields from string to float/int
        years_experience = float(form_data['YearsExperience'])
        age = int(form_data['Age'])
        
        # The other features are categorical and remain as strings
        job_title = form_data['JobTitle']
        education_level = form_data['EducationLevel']
        department = form_data['Department']

        # Create a pandas DataFrame from the input data, matching the model's expected format
        input_data = pd.DataFrame({
            'YearsExperience': [years_experience],
            'Age': [age],
            'JobTitle': [job_title],
            'EducationLevel': [education_level],
            'Department': [department]
        })
        
        print(f"Received data for prediction: \n{input_data}")

        # Use the loaded model to make a prediction
        prediction = model.predict(input_data)
        
        # Get the single predicted value
        output = prediction[0]
        
        # Format the output as a currency string
        formatted_salary = f"${output:,.2f}"

        # Return the prediction as a JSON object
        return jsonify({'predicted_salary': formatted_salary})

    except Exception as e:
        print(f"❌ An error occurred during prediction: {e}")
        return jsonify({'error': f'An error occurred on the server: {e}'}), 500

# --- Run the Application ---
if __name__ == "__main__":
    # To run this app:
    # 1. Make sure you have Flask installed: pip install Flask
    # 2. Save this code as 'app.py'.
    # 3. Create a folder named 'templates' in the same directory.
    # 4. Save the HTML file (which I will provide next) as 'index.html' inside the 'templates' folder.
    # 5. Make sure the 'salary_prediction_pipeline_enhanced.joblib' file is in the same directory.
    # 6. Run the script from your terminal: python app.py
    # 7. Open your web browser and go to http://127.0.0.1:5000
    app.run(debug=True)
