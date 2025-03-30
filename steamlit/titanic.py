import streamlit as st
import pickle

# Load the Titanic prediction model
try:
    tit_model = pickle.load(open(r"C:/model/linear_regression_model.pkl", "rb"))
except FileNotFoundError:
    st.error("Model file not found. Please check the file path.")
    st.stop()

# Title for the app
st.title("Titanic Survival Prediction")

# Add input widgets (example)
st.subheader("Enter Passenger Details:")
age = st.number_input("Age", min_value=0, max_value=100, step=1)
fare = st.number_input("Fare Paid (in $)", min_value=0.0, step=1.0)
gender = st.selectbox("Gender", ["Male", "Female"])
pclass = st.selectbox("Passenger Class", [1, 2, 3])

# Transform inputs for the model (example logic)
gender_encoded = 1 if gender == "Male" else 0
input_data = [[pclass, age, fare, gender_encoded]]

# Prediction button
if st.button("Predict"):
    prediction = tit_model.predict(input_data)  # Assuming this method exists in your model
    if prediction[0] == 1:
        st.success("The passenger would have survived!")
    else:
        st.warning("The passenger would not have survived.")
