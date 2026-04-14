import streamlit as st
import numpy as np
import os
import pickle
import time
import pandas as pd

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Car Price Predictor", layout="wide")

# ------------------ SESSION ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------ LOGIN PAGE ------------------
def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ------------------ MAIN APP ------------------
def main_app():
    # Load model
    model = pickle.load(open(os.path.join(os.getcwd(), "model.pkl"), "rb"))
    columns = pickle.load(open(os.path.join(os.getcwd(), "columns.pkl"), "rb"))

    # Sidebar
    st.sidebar.title("🚗 Navigation")
    page = st.sidebar.radio("Go to", ["Predict Price", "About"])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # ----------- PREDICTION PAGE -----------
    if page == "Predict Price":

        st.title("🚗 Car Price Predictor")

        col1, col2 = st.columns(2)

        with col1:
            year = st.slider("Manufacturing Year", 2000, 2025, 2018)
            age = 2025 - year
            km_driven = st.number_input("KM Driven", 0, 500000, step=1000)
            owner = st.selectbox("Owners", [1, 2, 3, 4])

        with col2:
            brand = st.selectbox("Brand", ["Maruti", "Hyundai", "Honda", "Toyota", "Tata", "Mahindra"])
            fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
            transmission = st.radio("Transmission", ["Manual", "Automatic"])

        st.markdown("---")

        # Prepare input
        input_dict = {col: 0 for col in columns}

        if 'Year' in input_dict:
            input_dict['Year'] = year
        if 'Age' in input_dict:
            input_dict['Age'] = age
        if 'kmDriven' in input_dict:
            input_dict['kmDriven'] = km_driven
        if 'Owner' in input_dict:
            input_dict['Owner'] = owner

        if f'Brand_{brand}' in input_dict:
            input_dict[f'Brand_{brand}'] = 1

        if f'FuelType_{fuel}' in input_dict:
            input_dict[f'FuelType_{fuel}'] = 1

        if f'Transmission_{transmission}' in input_dict:
            input_dict[f'Transmission_{transmission}'] = 1

        input_array = np.array([list(input_dict.values())])

        # Predict
        if st.button("🚀 Predict Price", use_container_width=True):

            with st.spinner("Analyzing..."):
                time.sleep(2)

            prediction = model.predict(input_array)[0]
            price = int(prediction)

            st.success(f"💰 Estimated Price: ₹ {price:,}")

            # -------- INSIGHTS --------
            st.subheader("📊 Insights")

            if age > 10:
                st.warning("Older cars have lower resale value")
            if km_driven > 100000:
                st.warning("High mileage reduces price")
            if owner > 2:
                st.warning("More owners = lower value")

            # -------- CHART --------
            st.subheader("📈 Price Trend")

            ages = list(range(1, 15))
            prices = [price - (i * 15000) for i in ages]

            df_chart = pd.DataFrame({
                "Age": ages,
                "Price": prices
            })

            st.line_chart(df_chart.set_index("Age"))

    # ----------- ABOUT PAGE -----------
    elif page == "About":
        st.title("📘 About Project")

        st.write("""
        This project predicts used car prices using Machine Learning.

        🔹 Built using:
        - Python
        - Scikit-learn
        - Streamlit

        🔹 Features:
        - Real-time prediction
        - Clean UI
        - Data preprocessing
        - Visualization

        🔹 Model:
        - Random Forest Regressor
        """)

# ------------------ ROUTING ------------------
if st.session_state.logged_in:
    main_app()
else:
    login()
