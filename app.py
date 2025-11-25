from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle

# -------------------------------------------------------------
# Initialize Flask App
# -------------------------------------------------------------
app = Flask(__name__)
CORS(app)   # Enable Cross-Origin Resource Sharing for frontend requests

# -------------------------------------------------------------
# Load Trained ML Model and TF-IDF Vectorizer
# -------------------------------------------------------------
model = pickle.load(open("improved_fake_job_model.pkl", "rb"))
vectorizer = pickle.load(open("improved_vectorizer.pkl", "rb"))

# -------------------------------------------------------------
# Route: Homepage
# Serves the main HTML UI for the application
# -------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------------------------------------------
# Route: /predict
# Handles POST requests from the frontend and returns prediction
# -------------------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    # Read JSON payload sent by frontend
    data = request.json

    # Combine all text fields into one string for model processing
    text = (
        data["title"] + " " +
        data["company_profile"] + " " +
        data["description"] + " " +
        data["requirements"]
    ).strip()

    # Transform input text using the pre-trained TF-IDF vectorizer
    x = vectorizer.transform([text])

    # Predict class (0 = Real Job, 1 = Fake Job)
    prediction = model.predict(x)[0]

    # Get prediction probabilities for both classes
    # probas[0] → Probability of Real
    # probas[1] → Probability of Fake
    probas = model.predict_proba(x)[0]

    # Return output in JSON format
    return jsonify({
        "prediction": int(prediction),
        "prob_real": float(probas[0]),
        "prob_fake": float(probas[1])
    })

# -------------------------------------------------------------
# Application Entry Point
# -------------------------------------------------------------
if __name__ == "__main__":
    # Run Flask app on all network interfaces (useful for testing)
    app.run("0.0.0.0", debug=True)