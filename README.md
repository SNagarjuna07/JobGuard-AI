# 🔐 JobGuard AI — Fake Job Posting Detection System

JobGuard AI is an intelligent system that detects fraudulent job postings using a blend of machine learning, probability scoring, and keyword-based scam detection.  
It includes a modern UI, a Flask backend, and a fully customizable SVM training pipeline.

---

## 🚀 Features

- 🧠 ML Model: Linear SVM + TF-IDF + SMOTE
- 📊 Probability Score for predictions
- ⚠ Scam Keyword Override System
- 🌐 Flask REST API
- 💻 Clean Web UI (HTML, CSS, JS)

---

## 📁 Project Structure

```
JobGuard-AI/
│
├── app.py
├── requirements.txt
│
├── improved_fake_job_model.pkl
├── improved_vectorizer.pkl
│
├── train_model.py           
│
└── templates/
    ├── index.html
    ├── style.css
    └── script.js
```

---

# ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```
git clone https://github.com/SNagarjuna07/JobGuard-AI.git
cd JobGuard-AI
```

### 2️⃣ Create virtual environment
```
python -m venv venv
venv/Scripts/activate     # Windows
source venv/bin/activate  # Linux/Mac
```

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

---

# 🧪 Train the Model (Before Running the App)

This project includes a full training pipeline that:

- Cleans and preprocesses text  
- Merges job fields  
- Applies TF-IDF vectorization  
- Balances dataset with SMOTE  
- Trains a Linear SVM  
- Calibrates probabilities  
- Saves updated `.pkl` model files  

### ▶️ Run the training script
```
python train_model.py
```

After training completes, these two files will be generated/updated:

```
improved_fake_job_model.pkl
improved_vectorizer.pkl
```

These are automatically loaded by `app.py`.

---

# ▶️ Run the Web App

After training, run:

```
python app.py
```

Open in browser:

👉 http://127.0.0.1:5000/

---

# 📊 Dataset & Model Performance

## 📁 Dataset Overview

JobGuard AI was trained using a publicly available **Real vs Fake Job Posting Dataset**, widely used in research for fraud detection.

### Dataset Statistics

| Attribute | Value |
|----------|--------|
| Total Samples | ~17,880 |
| Real Jobs | ~90% |
| Fake Jobs | ~10% |
| Problem Type | Binary Classification |
| Text Features | title, company_profile, description, requirements |
| Balancing Method | SMOTE |

### Common Fake Job Patterns
- Unrealistic salaries (“Earn ₹50,000 weekly”)
- Contact via Telegram/WhatsApp  
- Investment/deposit requests  
- Suspicious repetitive wording  
- Vague or empty descriptions  

This inspired the **scam keyword override system**.

---

# 🤖 Model Architecture

Your model is built with:

- **TF-IDF Vectorizer** (1–2 grams)
- **SMOTE Oversampling**
- **Linear SVM (LinearSVC)**
- **CalibratedClassifierCV** for probability scores
- **Custom Keyword Boosting Logic**

---

# 🧪 Model Performance

### Classification Report

```
               precision    recall  f1-score   support

           0       0.99      1.00      0.99      3403
           1       1.00      0.90      0.94       373

    accuracy                           0.99      3776
   macro avg       0.99      0.95      0.97      3776
weighted avg       0.99      0.99      0.99      3776
```

### Interpretation

- **Accuracy:** 99%
- **Fake Job Precision:** 100% (no false positives)
- **Fake Job Recall:** 90%
- **Macro F1:** 0.97  
- **Weighted F1:** 0.99  

---

# 📡 API Documentation

### POST /predict

#### Request Body:
```json
{
  "title": "Senior Developer",
  "company_profile": "Global IT Pvt Ltd",
  "description": "We are hiring...",
  "requirements": "Python, SQL"
}
```

#### Response:
```json
{
  "prediction": 1,
  "probability": 0.92
}
```

---

# 👤 Author

**S Nagarjuna**  

---

# ⭐ Support the Project

If you found JobGuard AI helpful, please ⭐ the repository — it helps a lot!

