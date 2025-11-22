import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
import pickle

# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("D:\\Coding\\Datasets\\Fake jobs\\fake_job_postings.csv")


df.fillna("", inplace=True)

# Combine text fields
df["text"] = df["title"] + " " + df["company_profile"] + " " + df["description"] + " " + df["requirements"]


# ============================================================
# 2. PREPROCESSING FUNCTION
# ============================================================

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " url ", text)
    text = re.sub(r"\d+", " number ", text)
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df["clean_text"] = df["text"].apply(clean_text)


# ============================================================
# 3. SCAM KEYWORD INJECTION (boosting)
# ============================================================

scam_keywords = [
    "telegram", "whatsapp", "earn", "weekly", "income",
    "investment", "bitcoin", "crypto", "limited seats",
    "work from home", "urgent", "immediate", "per week"
]

def add_scam_weight(text):
    for w in scam_keywords:
        if w in text:
            text += (" " + w) * 3   # boosts weight 3x
    return text

df["boosted_text"] = df["clean_text"].apply(add_scam_weight)


# ============================================================
# 4. TRAIN-TEST SPLIT
# ============================================================

X = df["boosted_text"]
y = df["fraudulent"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# ============================================================
# 5. TF-IDF VECTORIZATION (Advanced)
# ============================================================

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),      # includes bi-grams
    min_df=3,                # remove rare noise
    max_df=0.95,             # remove too-common words
    sublinear_tf=True,       # log scaling
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


# ============================================================
# 6. BALANCING DATA (SMOTE)
# ============================================================

sm = SMOTE(random_state=42)
X_train_bal, y_train_bal = sm.fit_resample(X_train_vec, y_train)


# ============================================================
# 7. TRAIN MODEL: LINEAR SVM (best for text) + probability calibration
# ============================================================

# SVM does not output probability → wrap with calibrator
svm = LinearSVC()
model = CalibratedClassifierCV(svm, method="sigmoid")

model.fit(X_train_bal, y_train_bal)


# ============================================================
# 8. EVALUATION
# ============================================================

y_pred = model.predict(X_test_vec)
y_prob = model.predict_proba(X_test_vec)[:,1]

print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))


# ============================================================
# 9. EXPORT MODEL + VECTORIZER
# ============================================================

pickle.dump(model, open("improved_fake_job_model.pkl", "wb"))
pickle.dump(vectorizer, open("improved_vectorizer.pkl", "wb"))

print("\nSaved improved model + vectorizer successfully.")
