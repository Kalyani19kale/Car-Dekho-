import streamlit as st
import pickle

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Car Dekho Price Predictor", layout="centered")

st.title("🚗 Car Dekho - Price Prediction App")
st.subheader("Enter Car Details")

# ---------------- NUMERICAL INPUTS ----------------
km_driven = st.number_input("Kilometers Driven", min_value=0)
seats = st.number_input("Seats", min_value=2, max_value=10)
yeard_old = st.number_input("Car Age (Years)", min_value=0)
mileage_value = st.number_input("Mileage (km/l)", min_value=0.0)
engine_value = st.number_input("Engine (CC)", min_value=0.0)
max_power_value = st.number_input("Max Power (bhp)", min_value=0.0)

# ---------------- CATEGORICAL INPUTS ----------------
fuel = st.selectbox(
    "Fuel Type",
    ["Petrol", "Diesel", "LPG", "CNG"]
)

seller_type = st.selectbox(
    "Seller Type",
    ["Dealer", "Individual", "Trustmark Dealer"]
)

transmission = st.selectbox(
    "Transmission Type",
    ["Automatic", "Manual"]
)

owner_order = [
    'Fourth & Above Owner',
    'Third Owner',
    'Second Owner',
    'First Owner',
    'Test Drive Car'
]

owner = st.selectbox("Owner Type", owner_order)

# ---------------- ENCODING (MATCH TRAINING) ----------------

# Owner → ORDINAL
owner_mapping = {
    'Fourth & Above Owner': 0,
    'Third Owner': 1,
    'Second Owner': 2,
    'First Owner': 3,
    'Test Drive Car': 4
}
owner_encoded = owner_mapping[owner]

# Fuel → ONE HOT (CNG dropped during training)
fuel_Diesel = 1 if fuel == "Diesel" else 0
fuel_LPG = 1 if fuel == "LPG" else 0
fuel_Petrol = 1 if fuel == "Petrol" else 0

# Seller type → ONE HOT (Dealer is base)
seller_type_Individual = 1 if seller_type == "Individual" else 0
seller_type_Trustmark = 1 if seller_type == "Trustmark Dealer" else 0

# Transmission → ONE HOT (Automatic is base)
transmission_Manual = 1 if transmission == "Manual" else 0

# ---------------- PREDICTION ----------------
if st.button("💰 Predict Price"):
    input_data = [[
        km_driven,
        owner_encoded,
        seats,
        yeard_old,
        mileage_value,
        engine_value,
        max_power_value,
        fuel_Diesel,
        fuel_LPG,
        fuel_Petrol,
        seller_type_Individual,
        seller_type_Trustmark,
        transmission_Manual
    ]]

    prediction = model.predict(input_data)

    st.success(f"💵 Estimated Car Price: ₹{prediction[0]:,.2f}")
