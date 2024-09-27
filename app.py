from flask import Flask, render_template, request, make_response ,redirect, url_for
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import pdfkit  # Import pdfkit for PDF generation
import json
import logging
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

# Specify the path to wkhtmltopdf.exe
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Load the pre-trained model using joblib
model = joblib.load('models/random_search_xgb_model.pkl')

# Define the correct feature names (for future reference)
feature_names = [
    "Age", "Gender", "Systolic Blood Pressure", "Diastolic Blood Pressure", "Smoking Status", "Alcohol Intake",
    "Physical Activity", "BMI", "Cholesterol Normal", "Cholesterol Above Normal",
    "Cholesterol Well Above Normal", "Glucose Normal", "Glucose Above Normal", "Glucose Well Above Normal"
]

# Function to preprocess data manually (including scaling and one-hot encoding)
def preprocess_data(age, gender, ap_hi, ap_lo, smoke, alco, active, bmi, chol, gluc):
    # Map gender (assuming 1 = female, 2 = male, convert to 0 for female, 1 for male)
    gender_encoded = 1 if gender == 2 else 0
    
    # One-hot encode cholesterol and glucose levels
    chol_encoded = [chol == 1, chol == 2, chol == 3]  # Cholesterol Normal, Above Normal, Well Above Normal
    gluc_encoded = [gluc == 1, gluc == 2, gluc == 3]  # Glucose Normal, Above Normal, Well Above Normal
    
    # Combine features into a single array
    features = np.array([[age, gender_encoded, ap_hi, ap_lo, smoke, alco, active, bmi] + chol_encoded + gluc_encoded])

    # Apply scaling to numerical features
    scaler = StandardScaler()  # Create a new scaler for scaling the input data
    scaled_features = scaler.fit_transform(features[:, :8])  # Scale the first 8 numerical features

    # Combine scaled numerical features with one-hot encoded categorical features
    processed_features = np.hstack([scaled_features, features[:, 8:]])  # Attach one-hot encoded chol and gluc features
    
    return processed_features

@app.route('/')
def home():
    return redirect(url_for('consent'))

@app.route('/consent', methods=['GET', 'POST'])
def consent():
    if request.method == 'POST':
        # User clicked "I Agree"
        return redirect(url_for('index'))  # Redirect to index.html
    return render_template('consent.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/predict', methods=['POST'])
def predict():
    logging.debug(request.form)
    try:
        # Get form data from the user
        age = request.form.get('age')
        gender = request.form.get('gender')
        height = request.form.get('height_cm')
        weight = request.form.get('weight')
        ap_hi = request.form.get('ap_hi')
        ap_lo = request.form.get('ap_lo')
        smoke = request.form.get('smoke')
        alco = request.form.get('alco')
        active = request.form.get('active')
        chol = request.form.get('chol')
        gluc = request.form.get('gluc')

         # Validate that none of the required fields are missing or empty (after stripping whitespace)
        if not all([age, gender, height, weight, ap_hi, ap_lo, smoke, alco, active, chol, gluc]) or \
           any([field.strip() == "" for field in [age, gender, height, weight, ap_hi, ap_lo, smoke, alco, active, chol, gluc]]):
            return "Error: Missing required input fields", 400

        # Convert fields to appropriate types and validate
        try:
            age = int(age)
            gender = int(gender)
            height = float(height)
            weight = float(weight)
            ap_hi = int(ap_hi)
            ap_lo = int(ap_lo)
            smoke = int(smoke)
            alco = int(alco)
            active = int(active)
            chol = int(chol)
            gluc = int(gluc)

            # Check for invalid values (e.g., negative or zero height/weight, unrealistic BP)
            if height <= 0 or weight <= 0 or ap_hi <= 0 or ap_lo <= 0:
                return "Error: Invalid input values", 400

        except ValueError:
            return "Error: Invalid data type for input fields", 400

        # Calculate BMI
        bmi = weight / ((height / 100) ** 2)

        # Preprocess the data manually
        processed_features = preprocess_data(age, gender, ap_hi, ap_lo, smoke, alco, active, bmi, chol, gluc)

        # Use the best model from RandomizedSearchCV for prediction
        best_model = model.best_estimator_ if hasattr(model, 'best_estimator_') else model

        # Get the predicted probability for the positive class
        prediction_prob = best_model.predict_proba(processed_features)[0][1]

        # Determine risk category
        if prediction_prob < 0.40:
            risk_category = "Low Risk"
            risk_color = "green"
        elif 0.40 <= prediction_prob <= 0.6:
            risk_category = "Moderate Risk"
            risk_color = "yellow"
        else:
            risk_category = "High Risk"
            risk_color = "red"

        # Pre-calculate the contributions of risk factors
        risk_factors = {
            'Cholesterol': chol / 3,
            'Glucose': gluc / 3,
            'Smoking': smoke,
            'Alcohol': alco,
            'Physical Activity': 1 - active,
            'BMI': min(bmi / 30, 1),
            'Blood Pressure': (ap_hi / 120 + ap_lo / 80) / 2
        }

        # Sort and calculate percentages for the top 5 risk factors
        sorted_risk_factors = dict(sorted(risk_factors.items(), key=lambda item: item[1], reverse=True)[:5])
        total_risk_contribution = sum(sorted_risk_factors.values())
        risk_factors_percentage = {k: (v / total_risk_contribution) * 100 for k, v in sorted_risk_factors.items()}

        # NHS recommendations mapping
        nhs_recommendations = {
            'Cholesterol': {
                'recommendation': 'Eat a healthy, balanced diet low in saturated fats. Increase physical activity, maintain a healthy weight, avoid smoking, and limit alcohol intake.',
                'link': 'https://www.nhs.uk/live-well/eat-well/food-types/fat-the-facts/'
            },
            'Blood Pressure': {
                'recommendation': 'Reduce salt intake, eat a balanced diet, exercise regularly, limit alcohol, lose weight if overweight, quit smoking, and manage stress.',
                'link': 'https://www.nhs.uk/conditions/high-blood-pressure/'
            },
            'Smoking': {
                'recommendation': 'Quitting smoking greatly improves your health. Consider nicotine replacement therapy or support groups to quit.',
                'link': 'https://www.nhs.uk/live-well/quit-smoking/nhs-stop-smoking-services-help-you-quit/'
            },
            'Alcohol': {
                'recommendation': 'Reduce alcohol consumption to improve overall health and reduce risk. Follow the recommended limit of 14 units of alcohol per week.',
                'link': 'https://www.nhs.uk/live-well/alcohol-advice/calculating-alcohol-units/'
            },
            'Physical Activity': {
                'recommendation': 'Increase your physical activity to at least 150 minutes of moderate exercise per week. This can greatly reduce cardiovascular risk.',
                'link': 'https://www.nhs.uk/live-well/exercise/'
            },
            'BMI': {
                'recommendation': 'Maintain a healthy weight through a balanced diet and regular exercise. Losing weight can significantly reduce your risk.',
                'link': 'https://www.nhs.uk/live-well/healthy-weight/'
            },
            'Glucose': {
                'recommendation': 'Maintain normal blood glucose levels through a balanced diet, regular exercise, and monitoring sugar intake.',
                'link': 'https://www.nhs.uk/conditions/type-2-diabetes/'
            }
        }

        # Inside the /predict route:
        recommendations = {factor: nhs_recommendations[factor] for factor in sorted_risk_factors.keys()}

        report_data = {
            'age': age,
            'gender': 'Male' if gender == 1 else 'Female',
            'height': height,
            'weight': weight,
            'bmi': round(bmi, 2),
            'ap_hi': ap_hi,
            'ap_lo': ap_lo,
            'smoke': 'Yes' if smoke == 1 else 'No',
            'alco': 'Yes' if alco == 1 else 'No',
            'active': 'Yes' if active == 1 else 'No',
            'cholesterol': 'Normal' if chol == 1 else 'Above Normal' if chol == 2 else 'Well Above Normal',
            'glucose': 'Normal' if gluc == 1 else 'Above Normal' if gluc == 2 else 'Well Above Normal',
            'prediction': risk_category,
            'probability': round(prediction_prob, 2),
            'risk_color': risk_color,
            'risk_factors_percentage': risk_factors_percentage,
            'recommendations': recommendations  # Include recommendations in the report_data
        }

        # Render the results page with the report data
        return render_template('results.html', report_data=report_data)

    except Exception as e:
        # Properly handle the exception and return an informative error message
        return "Error occurred during prediction: {}".format(e), 400


@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    try:
        # Retrieve form data
        prediction = request.form.get('prediction')
        probability = request.form.get('probability')
        risk_color = request.form.get('risk_color')
        ap_hi = request.form.get('ap_hi')
        ap_lo = request.form.get('ap_lo')
        bmi = request.form.get('bmi')
        age = request.form.get('age')
        gender = request.form.get('gender')
        risk_factors_percentage = request.form.get('risk_factors_percentage')
        recommendations = request.form.get('recommendations')

        # Check if any required fields are missing
        if not (prediction and probability and risk_color and ap_hi and ap_lo and bmi and age and gender and risk_factors_percentage and recommendations):
            return "Error: Missing required fields", 400  # Return 400 Bad Request if any field is missing

        # Ensure data can be parsed correctly
        try:
            risk_factors_percentage = json.loads(risk_factors_percentage)
            recommendations = json.loads(recommendations)
        except (ValueError, TypeError):
            return "Error: Invalid JSON format for risk factors or recommendations", 400  # Handle invalid JSON parsing

        # Render the HTML template for the PDF
        rendered_html = render_template('results_pdf.html', report_data={
            'prediction': prediction,
            'probability': probability,
            'risk_color': risk_color,
            'ap_hi': ap_hi,
            'ap_lo': ap_lo,
            'bmi': bmi,
            'age': age,
            'gender': gender,
            'risk_factors_percentage': risk_factors_percentage,
            'recommendations': recommendations
        })

        # Generate PDF using pdfkit
        pdf = pdfkit.from_string(rendered_html, False, configuration=config)

        # Create a response to download the PDF
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=prediction_report.pdf'

        return response

    except Exception as e:
        return f"Error occurred during PDF generation: {e}", 400



if __name__ == "__main__":
    app.run(debug=True)