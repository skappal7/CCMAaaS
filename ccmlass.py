# -*- coding: utf-8 -*-
"""ccmlass.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tofDK9dGGpz1TOBJ4esCMDpRkgbfud3o
"""

import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Sample Data (Replace 'MLData.csv' with your actual data file)
data = pd.read_csv('MLData.csv')

# Train a simple RandomForestClassifier
X = data[['AHT (min)', 'NTT (min)', 'Cross Talk (%)', 'CSAT (%)', 'Sentiment Score', 'NPS Score', 'FCR (%)', 'Avg Speed of Answer (sec)', 'Abandonment Rate (%)', 'Medallia Survey Result', 'Industry']]
y = data['Maturity Level']

# Define preprocessing steps
numeric_features = ['AHT (min)', 'NTT (min)', 'Cross Talk (%)', 'CSAT (%)', 'Sentiment Score', 'NPS Score', 'FCR (%)', 'Avg Speed of Answer (sec)', 'Abandonment Rate (%)']
categorical_features = ['Medallia Survey Result', 'Industry']

numeric_transformer = Pipeline(steps=[('num', 'passthrough')])  # No transformation needed for numeric features

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Append classifier to preprocessing pipeline
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', RandomForestClassifier())])

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the model
clf.fit(X_train, y_train)

# Save the model
joblib.dump(clf, 'model.pkl')

# Load the model
loaded_model = joblib.load('model.pkl')

# Predict Maturity Level
y_pred = loaded_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Streamlit App
st.title("Analytics Maturity Level Prediction")

# Model Accuracy in percentage with bold and large size
st.sidebar.text(f'Model Accuracy: **{accuracy*100:.0f}%**')
st.title("Select Variables")

# Sliders for user input
aht = st.slider("Average Handling Time (AHT)", min_value=0, max_value=int(data['AHT (min)'].max()), value=0)
ntt = st.slider("Non-Talk Time (NTT)", min_value=0, max_value=int(data['NTT (min)'].max()), value=0)
cross_talk = st.slider("Cross Talk (%)", min_value=0, max_value=int(data['Cross Talk (%)'].max()), value=0)
csat = st.slider("CSAT (%)", min_value=0, max_value=int(data['CSAT (%)'].max()), value=0)
sentiment = st.slider("Sentiment Score", min_value=1, max_value=10, value=5)
nps = st.slider("NPS Score", min_value=0, max_value=int(data['NPS Score'].max()), value=0)
fcr = st.slider("FCR (%)", min_value=0, max_value=int(data['FCR (%)'].max()), value=0)
asa = st.slider("Avg Speed of Answer (sec)", min_value=0, max_value=int(data['Avg Speed of Answer (sec)'].max()), value=0)
abandonment_rate = st.slider("Abandonment Rate (%)", min_value=0, max_value=int(data['Abandonment Rate (%)'].max()), value=0)

# Dropdown for Medallia Survey Result and Industry
with st.sidebar:
    st.title("Select Dropdowns")
    medallia_survey_result = st.selectbox("Medallia Survey Result", ['Satisfied', 'Neutral', 'Dissatisfied'], help="Satisfied: 0, Neutral: 1, Dissatisfied: 2")
    industry = st.selectbox("Industry", ['Healthcare', 'Banking', 'Utilities', 'Sales', 'Tech Support'], help="Healthcare: 0, Banking: 1, Utilities: 2, Sales: 3, Tech Support: 4")

# Convert user input to DataFrame
input_data = pd.DataFrame({
    'AHT (min)': [aht],
    'NTT (min)': [ntt],
    'Cross Talk (%)': [cross_talk],
    'CSAT (%)': [csat],
    'Sentiment Score': [sentiment],
    'NPS Score': [nps],
    'FCR (%)': [fcr],
    'Avg Speed of Answer (sec)': [asa],
    'Abandonment Rate (%)': [abandonment_rate],
    'Medallia Survey Result': [medallia_survey_result],
    'Industry': [industry]
})

# Predict Maturity Level
predicted_maturity_level = loaded_model.predict(input_data)[0]
st.write(f"**Predicted Maturity Level:** {predicted_maturity_level}")

# Display Probability Distribution with Maturity Levels
st.title("Probability Distribution of Maturity Levels")
probabilities = loaded_model.predict_proba(input_data)[0]
maturity_levels = loaded_model.classes_
fig, ax = plt.subplots()
sns.barplot(x=maturity_levels, y=probabilities, ax=ax)
ax.set(title='Maturity Level Probabilities', xlabel='Maturity Level', ylabel='Probability')
ax.tick_params(axis='x', rotation=45)
ax.tick_params(axis='y', labelsize=8)
for i, value in enumerate(probabilities):
    ax.text(i, value + 0.01, f'{value:.2%}', ha='center', va='bottom')
st.pyplot(fig)

# Define Survey Result Labels
medallia_labels = {
    0: "Satisfied",
    1: "Neutral",
    2: "Dissatisfied"
}

# Define Industry Labels
industry_labels = {
    0: "Healthcare",
    1: "Banking",
    2: "Utilities",
    3: "Sales",
    4: "Tech Support"
}

# Display Survey Result Labels
st.sidebar.title("Medallia Survey Result Labels:")
for key, value in medallia_labels.items():
    st.sidebar.text(f"{key}: {value}")

# Display Industry Labels
st.sidebar.title("Industry Labels:")
for key, value in industry_labels.items():
    st.sidebar.text(f"{key}: {value}")



