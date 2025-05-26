import streamlit as st
import numpy as np
import gdown
from joblib import load

# Google Drive file ID of your model
FILE_ID = '1PRnrcgJMi1zmHVK-aWgHjnWhzxIthaMJ'
MODEL_URL = f'https://drive.google.com/uc?id={FILE_ID}'
MODEL_PATH = 'random_forest_modell.pkl'

# Download the model (only if not already downloaded)
@st.cache_data(show_spinner=False)
def download_model():
    gdown.download(MODEL_URL, MODEL_PATH, quiet=True)
    return MODEL_PATH

model_path = download_model()
model = load(model_path)

st.title('Hypertension Prediction App')
st.markdown("""
This is a Hypertension Prediction Model built for the master's thesis project in Epidemiology  
by Tsegasilassie Gebremariam at Debre Berhan University.
""")

# Input fields for the 23 features
sex = st.selectbox('Sex (0=Female, 1=Male)', [0, 1])
education = st.selectbox('Education Level (0-4)', [0, 1, 2, 3, 4])
marital_status = st.selectbox('Marital Status (0-2)', [0, 1, 2])
occupation = st.selectbox('Occupation (0-4)', [0, 1, 2, 3, 4])
adult_18 = st.selectbox('Adult ≥ 18 (0=No, 1=Yes)', [0, 1])
current_smoking = st.selectbox('Current Smoking (0=No, 1=Yes)', [0, 1])
past_smoking = st.selectbox('Past Smoking (0=No, 1=Yes)', [0, 1])
days_fruit = st.number_input('Days Fruit Served (per week)', min_value=0, max_value=7, step=1)
servings_fruit = st.number_input('Servings Fruits per Day', min_value=0.0, step=0.1)
days_veg = st.number_input('Days Vegetables Served (per week)', min_value=0, max_value=7, step=1)
servings_veg = st.number_input('Servings Vegetables per Day', min_value=0.0, step=0.1)
add_salt = st.selectbox('Add Salt While Eating (0=No, 1=Yes)', [0, 1])
processed_food = st.selectbox('Eating Processed Food (0=No, 1=Yes)', [0, 1])
salt_amount = st.number_input('Salt Amount (grams/day)', min_value=0.0, step=0.1)
vigorous_work = st.selectbox('Vigorous Exercise at Work (0=No, 1=Yes)', [0, 1])
moderate_work = st.selectbox('Moderate Exercise at Work (0=No, 1=Yes)', [0, 1])
sedentary_hours = st.number_input('Sedentary Hours per Day', min_value=0.0, max_value=24.0, step=0.1)
told_high_bp = st.selectbox('Told Had High BP (0=No, 1=Yes)', [0, 1])
avg_pr = st.number_input('Average Pulse Rate', min_value=0, step=1)
bmi = st.number_input('BMI', min_value=0.0, step=0.1)
fbg = st.number_input('Fasting Blood Glucose (FBG)', min_value=0.0, step=0.1)
whr = st.number_input('Weight to Hip Ratio', min_value=0.0, step=0.01)
chol = st.number_input('Total Cholesterol Level', min_value=0.0, step=0.1)

# Gather inputs into array
input_data = np.array([[ 
    sex, education, marital_status, occupation, adult_18,
    current_smoking, past_smoking, days_fruit, servings_fruit,
    days_veg, servings_veg, add_salt, processed_food, salt_amount,
    vigorous_work, moderate_work, sedentary_hours, told_high_bp,
    avg_pr, bmi, fbg, whr, chol
]])

if st.button('Predict'):
    prediction = model.predict(input_data)
    st.write(f'Prediction: {prediction[0]}')
    st.success(f'Result: {"Hypertensive" if prediction[0] == 1 else "Not Hypertensive"}')
