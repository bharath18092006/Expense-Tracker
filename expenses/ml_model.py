from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


DATASET_PATH = Path(__file__).resolve().parent.parent / "dataset.csv"

data = pd.read_csv(DATASET_PATH)
data["description"] = data["description"].fillna("").astype(str).str.lower()
data["category"] = data["category"].fillna("").astype(str)

X = data["description"]
y = data["category"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_vec, y)


def predict_category(text: str) -> str:
    clean_text = (text or "").strip().lower()
    if not clean_text:
        return ""
    text_vec = vectorizer.transform([clean_text])
    prediction = model.predict(text_vec)
    return prediction[0]
