import streamlit as st
from joblib import load
import numpy as np
import gdown
import os

# Download model from Google Drive
@st.cache_resource
def load_model():
    # Google Drive file ID from the URL
    file_id = "1UPGaTIFQgdNQuT4bcC6S0SVJhj5KqR4z"
    url = f"https://drive.google.com/uc?id={file_id}"
    
    # Local file name to save
    output = "random_forest_model.pkl"
    
    # Download if file doesn't exist
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    
    # Load the model
    return load(output)

# Load model
try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.title('Hypertension Prediction App')
st.markdown("""
This is a Hypertension Prediction Model built for the master's thesis project in Epidemiology  
by Tsegasilassie Gebremariam at Debre Berhan University.
""")

# Input fields for all 23 features
sex = st.selectbox('Sex', [0, 1])
education = st.selectbox('Education Level', [0, 1, 2, 3, 4])  # Adjust as needed
marital_status = st.selectbox('Marital Status', [0, 1, 2])    # Adjust as needed
occupation = st.selectbox('Occupation', [0, 1, 2, 3, 4])       # Adjust as needed
adult_18 = st.selectbox('Adult >= 18', [0, 1])
current_smoking = st.selectbox('Current Smoking', [0, 1])
past_smoking = st.selectbox('Past Smoking', [0, 1])
days_fruit = st.number_input('Days Fruit Served', min_value=0)
servings_fruit = st.number_input('Servings Fruits per Day', min_value=0.0)
days_veg = st.number_input('Days Vegetables Served', min_value=0)
servings_veg = st.number_input('Servings Vegetables per Day', min_value=0.0)
add_salt = st.selectbox('Add Salt While Eating', [0, 1])
processed_food = st.selectbox('Eating Processed Food', [0, 1])
salt_amount = st.number_input('Salt Amount (grams/day)', min_value=0.0)
vigorous_work = st.selectbox('Vigorous Exercise at Work', [0, 1])
moderate_work = st.selectbox('Moderate Exercise at Work', [0, 1])
sedentary_hours = st.number_input('Sedentary Hours per Day', min_value=0.0)
told_high_bp = st.selectbox('Told Had High BP', [0, 1])
avg_pr = st.number_input('Average Pulse Rate', min_value=0)
bmi = st.number_input('BMI', min_value=0.0)
fbg = st.number_input('FBG', min_value=0.0)
whr = st.number_input('Weight to Hip Ratio', min_value=0.0)
chol = st.number_input('Total Cholesterol Level', min_value=0.0)

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
    try:
        prediction = model.predict(input_data)
        st.success(f'Prediction: {"Hypertensive" if prediction[0] == 1 else "Not Hypertensive"}')
    except Exception as e:
        st.error(f"Error making prediction: {e}")
