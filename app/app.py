import os
import streamlit as st
import pandas as pd
import joblib
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "..", "notebooks", "churn_model.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "..", "notebooks", "features.pkl"))
st.title("Customer Churn Prediction")

st.write(
    "Predict whether a telecom customer is likely to churn."
)
gender = st.selectbox(
    "Gender",
    ["Female", "Male"]
)

senior_citizen = st.selectbox(
    "Senior Citizen",
    [0, 1]
)

partner = st.selectbox(
    "Partner",
    ["No", "Yes"]
)

dependents = st.selectbox(
    "Dependents",
    ["No", "Yes"]
)

tenure = st.slider(
    "Tenure (Months)",
    0,
    72,
    12
)

monthly_charges = st.number_input(
    "Monthly Charges",
    min_value=0.0,
    value=70.0
)

total_charges = st.number_input(
    "Total Charges",
    min_value=0.0,
    value=1000.0
)
phone_service = st.selectbox(
    "Phone Service",
    ["No", "Yes"]
)

multiple_lines = st.selectbox(
    "Multiple Lines",
    ["No", "Yes", "No phone service"]
)

internet_service = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)

online_security = st.selectbox(
    "Online Security",
    ["No", "Yes", "No internet service"]
)

online_backup = st.selectbox(
    "Online Backup",
    ["No", "Yes", "No internet service"]
)

device_protection = st.selectbox(
    "Device Protection",
    ["No", "Yes", "No internet service"]
)

tech_support = st.selectbox(
    "Tech Support",
    ["No", "Yes", "No internet service"]
)

streaming_tv = st.selectbox(
    "Streaming TV",
    ["No", "Yes", "No internet service"]
)

streaming_movies = st.selectbox(
    "Streaming Movies",
    ["No", "Yes", "No internet service"]
)

contract = st.selectbox(
    "Contract",
    ["Month-to-month", "One year", "Two year"]
)

paperless_billing = st.selectbox(
    "Paperless Billing",
    ["No", "Yes"]
)

payment_method = st.selectbox(
    "Payment Method",
    [
        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check"
    ]
)

if st.button("Predict Churn"):

    data = {col: 0 for col in features}

    data["SeniorCitizen"] = senior_citizen
    data["tenure"] = tenure
    data["MonthlyCharges"] = monthly_charges
    data["TotalCharges"] = total_charges

    if gender == "Male":
        data["gender_Male"] = 1

    if partner == "Yes":
        data["Partner_Yes"] = 1

    if dependents == "Yes":
        data["Dependents_Yes"] = 1

    if phone_service == "Yes":
        data["PhoneService_Yes"] = 1

    if multiple_lines == "No phone service":
        data["MultipleLines_No phone service"] = 1
    elif multiple_lines == "Yes":
        data["MultipleLines_Yes"] = 1

    if internet_service == "Fiber optic":
        data["InternetService_Fiber optic"] = 1
    elif internet_service == "No":
        data["InternetService_No"] = 1

    if online_security == "No internet service":
        data["OnlineSecurity_No internet service"] = 1
    elif online_security == "Yes":
        data["OnlineSecurity_Yes"] = 1

    if online_backup == "No internet service":
        data["OnlineBackup_No internet service"] = 1
    elif online_backup == "Yes":
        data["OnlineBackup_Yes"] = 1

    if device_protection == "No internet service":
        data["DeviceProtection_No internet service"] = 1
    elif device_protection == "Yes":
        data["DeviceProtection_Yes"] = 1

    if tech_support == "No internet service":
        data["TechSupport_No internet service"] = 1
    elif tech_support == "Yes":
        data["TechSupport_Yes"] = 1

    if streaming_tv == "No internet service":
        data["StreamingTV_No internet service"] = 1
    elif streaming_tv == "Yes":
        data["StreamingTV_Yes"] = 1

    if streaming_movies == "No internet service":
        data["StreamingMovies_No internet service"] = 1
    elif streaming_movies == "Yes":
        data["StreamingMovies_Yes"] = 1

    if contract == "One year":
        data["Contract_One year"] = 1
    elif contract == "Two year":
        data["Contract_Two year"] = 1

    if paperless_billing == "Yes":
        data["PaperlessBilling_Yes"] = 1

    if payment_method == "Credit card (automatic)":
        data["PaymentMethod_Credit card (automatic)"] = 1
    elif payment_method == "Electronic check":
        data["PaymentMethod_Electronic check"] = 1
    elif payment_method == "Mailed check":
        data["PaymentMethod_Mailed check"] = 1

    input_df = pd.DataFrame([data])

    # 🔥 PREDICTION (MISSING BEFORE)
    prediction = model.predict(input_df)[0]
    
    probability = model.predict_proba(input_df)[0][1]
    st.subheader("Churn Probability Visualization")

    st.progress(float(probability))

    # Risk Level
    if probability < 0.3:
        risk = "🟢 Low Risk"
    elif probability < 0.7:
        risk = "🟡 Medium Risk"
    else:
        risk = "🔴 High Risk"

    st.subheader("Risk Level")
    st.write(risk)

    st.subheader("Prediction Result")

    if prediction == 1:
        st.error("⚠️ High Churn Risk")
    else:
        st.success("✅ Customer Likely To Stay")

    st.write(f"Churn Probability: {probability:.2%}")

    # SHAP (MOVE INSIDE BUTTON, AFTER PREDICTION)
    # ---------------- SHAP EXPLANATION ---------------- #
    st.subheader("Why this prediction? (Explainable AI)")

    reasons = []

    if contract == "Month-to-month":
        reasons.append("Month-to-month contract increases churn risk")

    if tenure < 12:
        reasons.append("Low tenure increases churn risk")

    if monthly_charges > 70:
        reasons.append("High monthly charges increase churn risk")

    if internet_service == "Fiber optic":
        reasons.append("Fiber optic users show higher churn tendency")

    for r in reasons[:3]:
        st.write("•", r)
    # Quick Insight
    st.subheader("Quick Insight")

    if prediction == 1:
        st.write("Customer shows patterns similar to high churn users.")
        st.write("Possible reasons: Month-to-month contract, high charges, lack of support.")
    else:
        st.write("Customer has strong retention indicators like longer tenure or stable contract.")

    # Model Info
    st.subheader("Model Info")
    st.write("Model used: Logistic Regression (Best Accuracy: 80.31%)")

    st.subheader("Project Summary")
    st.write("""
    This model predicts customer churn using telecom data.
    It helps businesses identify at-risk customers early and improve retention strategies.
    Model: Logistic Regression
    """)