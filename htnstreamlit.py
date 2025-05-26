import streamlit as st
from joblib import load  # Explicit import to avoid circular issues
import numpy as np
from joblib import load

# Load model
model = load('random_forest_model.pkl')

st.title('My Model Prediction App')
st.title('Hypertension Prediction App')

# Input fields
feature1 = st.number_input('Feature 1')
feature2 = st.number_input('Feature 2')
feature3 = st.number_input('Feature 3')
# Input fields for all 23 features
sex = st.selectbox('Sex', [0, 1])
education = st.selectbox('Education Level', [0, 1, 2, 3, 4])  # Adjust as needed
marital_status = st.selectbox('Marital Status', [0, 1, 2])    # Adjust as needed
occupation = st.selectbox('Occupation', [0, 1, 2, 3, 4])       # Adjust as needed
adult_18 = st.selectbox('Adult >= 18', [0, 1])
current_smoking = st.selectbox('Current Smoking', [0, 1])
past_smoking = st.selectbox('Past Smoking', [0, 1])
days_fruit = st.number_input('Days Fruit Served')
servings_fruit = st.number_input('Servings Fruits per Day')
days_veg = st.number_input('Days Vegetables Served')
servings_veg = st.number_input('Servings Vegetables per Day')
add_salt = st.selectbox('Add Salt While Eating', [0, 1])
processed_food = st.selectbox('Eating Processed Food', [0, 1])
salt_amount = st.number_input('Salt Amount (grams/day)')
vigorous_work = st.selectbox('Vigorous Exercise at Work', [0, 1])
moderate_work = st.selectbox('Moderate Exercise at Work', [0, 1])
sedentary_hours = st.number_input('Sedentary Hours per Day')
told_high_bp = st.selectbox('Told Had High BP', [0, 1])
avg_pr = st.number_input('Average Pulse Rate')
bmi = st.number_input('BMI')
fbg = st.number_input('FBG')
whr = st.number_input('Weight to Hip Ratio')
chol = st.number_input('Total Cholesterol Level')

# Collect all inputs in correct order
input_data = np.array([[
    sex, education, marital_status, occupation, adult_18,
    current_smoking, past_smoking, days_fruit, servings_fruit,
    days_veg, servings_veg, add_salt, processed_food, salt_amount,
    vigorous_work, moderate_work, sedentary_hours, told_high_bp,
    avg_pr, bmi, fbg, whr, chol
]])

# Prediction
if st.button('Predict'):
    input_data = np.array([[feature1, feature2, feature3]])
prediction = model.predict(input_data)
st.write(f'Prediction: {prediction[0]}')
st.success(f'Prediction: {"Hypertensive" if prediction[0]==1 else "Not Hypertensive"}')