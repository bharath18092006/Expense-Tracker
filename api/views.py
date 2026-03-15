from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ==========================
# TRAIN MODEL ONCE
# ==========================

data = pd.read_csv('dataset.csv')

def preprocess_text(text):
    return text.lower()

data['clean_description'] = data['description'].apply(preprocess_text)

tfidf_vectorizer = TfidfVectorizer(
    ngram_range=(1,2),
    max_features=3000,
    stop_words='english'
)

X = tfidf_vectorizer.fit_transform(data['clean_description'])
y = data['category']

model = LogisticRegression(max_iter=2000, class_weight='balanced')
model.fit(X, y)

print("API Model Loaded Successfully")


# ==========================
# PREDICT CATEGORY
# ==========================

class PredictCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_input = request.data.get('description')

        if not user_input:
            return Response({'error': 'No description provided'}, status=400)

        cleaned_input = preprocess_text(user_input)
        input_vector = tfidf_vectorizer.transform([cleaned_input])

        predicted_category = model.predict(input_vector)[0]

        return Response(
            {'predicted_category': predicted_category},
            status=status.HTTP_200_OK
        )


# ==========================
# UPDATE DATASET
# ==========================

class UpdateDataset(APIView):

    def post(self, request):
        new_data = request.data.get('new_data')

        if not new_data:
            return Response({'error': 'No data provided'}, status=400)

        description = new_data.get('description')
        category = new_data.get('category')

        if not description or not category:
            return Response({'error': 'Invalid data'}, status=400)

        data = pd.read_csv('dataset.csv')

        new_row = {
            'description': description,
            'category': category
        }

        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        data.to_csv('dataset.csv', index=False)

        return Response({'message': 'Dataset updated'}, status=200)
