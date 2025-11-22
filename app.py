from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

model = pickle.load(open("improved_fake_job_model.pkl", "rb"))
vectorizer = pickle.load(open("improved_vectorizer.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    text = (
        data["title"] + " " +
        data["company_profile"] + " " +
        data["description"] + " " +
        data["requirements"]
    ).strip()

    x = vectorizer.transform([text])

    prediction = model.predict(x)[0]
    probas = model.predict_proba(x)[0]

    return jsonify({
        "prediction": int(prediction),
        "prob_real": float(probas[0]),
        "prob_fake": float(probas[1])
    })

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)