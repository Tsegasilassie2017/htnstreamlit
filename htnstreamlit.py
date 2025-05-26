import streamlit as st
from joblib import load  # Explicit import to avoid circular issues
import numpy as np

# Load model
model = load('random_forest_model.pkl')

st.title('My Model Prediction App')

# Input fields
feature1 = st.number_input('Feature 1')
feature2 = st.number_input('Feature 2')
feature3 = st.number_input('Feature 3')

if st.button('Predict'):
    input_data = np.array([[feature1, feature2, feature3]])
    prediction = model.predict(input_data)
    st.write(f'Prediction: {prediction[0]}')