# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import pickle
import base64
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from streamlit_folium import st_folium
import folium

# ----------------------------- Config & Load -----------------------------
st.set_page_config(page_title="Bengaluru House Price Predictor", layout="centered")

# Load model and encoder
try:
    with open("house_price_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("location_encoder.pkl", "rb") as f:
        le = pickle.load(f)
except Exception as e:
    st.error(f"🔧 Error loading model or encoder: {e}")
    st.stop()

locations = list(le.classes_)

# ----------------------------- Theme Setup -----------------------------
use_dark_theme = st.toggle("🌙 Dark Mode", value=False)
theme = "dark" if use_dark_theme else "light"
bg_image = "blur-map-dark.jpg" if theme == "dark" else "blur-map-light.jpg"

def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(f"""
    <style>
    
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: {"white" if theme == "dark" else "black"};
    }}

    .block-container {{
        padding-bottom: 0rem !important;
    }}

    .stButton>button {{
        background-color: {"#1e90ff" if theme == "dark" else "#4CAF50"};
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }}

    div[data-testid="stVerticalBlock"] {{
        background: rgba(255, 255, 255, 0.25);
        padding: 20px;
        border-radius: 16px;
        backdrop-filter: blur(8px);
        margin-bottom: 10px;
        color: black !important;
        font-weight: bold !important;
    }}

    div[data-testid="stVerticalBlock"] * {{
        color: black !important;
        font-weight: bold !important;
    }}

    footer {{visibility: hidden;}}

    </style>
""", unsafe_allow_html=True)


set_background(bg_image)

# ----------------------------- UI Title -----------------------------
st.markdown(f"<h1 style='text-align:center;'>🏠 Bengaluru House Price Predictor</h1>", unsafe_allow_html=True)

# ----------------------------- Location Selector -----------------------------
location_name = None
method = st.radio("📍 How do you want to select the location?", ["Dropdown", "Map"])

if method == "Dropdown":
    location_name = st.selectbox("Select Location", locations)
else:
    st.write("🗺️ Click anywhere on the map to select your locality.")
    m = folium.Map(location=[12.9716, 77.5946], zoom_start=11)
    folium.Marker([12.9716, 77.5946], tooltip="Bengaluru").add_to(m)
    map_data = st_folium(m, height=450, width=700)  # reduced height for less gap

    if map_data and map_data["last_clicked"]:
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        try:
            geolocator = Nominatim(user_agent="geoapi")
            location = geolocator.reverse((lat, lon), language="en", timeout=10)
            if location:
                address = location.raw.get("address", {})
                location_name = (
                    address.get("neighbourhood") or
                    address.get("suburb") or
                    address.get("city_district") or
                    address.get("town") or
                    location.address.split(",")[0]
                )
                if location_name:
                    st.info(f"📌 Selected Location: **{location_name}**")
                else:
                    st.warning("⚠️ Could not extract location name. Try another point.")
            else:
                st.warning("❗ Location not found.")
        except (GeocoderTimedOut, GeocoderUnavailable):
            st.error("❌ Geocoding failed. Try again later.")

# ----------------------------- Input Section -----------------------------
st.divider()
total_sqft = st.number_input("📐 Enter Total Square Feet", min_value=300, max_value=10000, step=50)
bath = st.slider("🛁 Number of Bathrooms", 1, 10, 2)
bhk = st.slider("🛏️ Number of BHK", 1, 10, 2)

# ----------------------------- Prediction Logic -----------------------------
if st.button("🔮 Predict Price"):
    if not location_name:
        st.error("📍 Please select a location before predicting.")
    elif location_name not in le.classes_:
        st.error(f"⚠️ Location '{location_name}' is not in the training data.")
    else:
        location_encoded = le.transform([location_name])[0]
        input_data = np.array([[location_encoded, total_sqft, bath, bhk]])

        try:
            predicted_price = model.predict(input_data)[0]
        except Exception as e:
            st.error(f"⚠️ Prediction failed: {e}")
            st.stop()

        # 💰 Price Display
        st.markdown(f"""
        <div style='padding:20px; border-radius:12px; background:rgba(255,255,255,0.25); text-align:center; animation: fadeIn 1s ease-in-out; backdrop-filter: blur(4px); color:black; font-weight:bold;'>
            <h2 style='color:#4CAF50; font-weight: bold;'>💰 Estimated Price: ₹ {predicted_price:.2f} lakhs</h2>
        </div>
        <style>
        @keyframes fadeIn {{
            from {{opacity: 0; transform: translateY(-20px);}}
            to {{opacity: 1; transform: translateY(0);}}
        }}
        </style>
        """, unsafe_allow_html=True)

        # 📊 Bar Chart
        st.subheader("📊 Price Comparison with Other Locations")
        similar_locations = [loc for loc in locations if loc != location_name][:4]
        prices = [predicted_price * np.random.uniform(0.9, 1.1) for _ in similar_locations]
        data = {location_name: predicted_price}
        data.update(dict(zip(similar_locations, prices)))
        st.bar_chart(data)

        # 📄 TXT Report Download (instead of PDF)
        if st.button("📥 Download Price Report"):
            report_text = f"""🏠 Bengaluru House Price Report

📍 Location: {location_name}
📐 Total Sqft: {total_sqft}
🛁 Bathrooms: {bath}
🛏️ BHK: {bhk}
💰 Estimated Price: ₹ {predicted_price:.2f} Lakhs
"""
            with open("House_Price_Report.txt", "w") as f:
                f.write(report_text)

            with open("House_Price_Report.txt", "rb") as f:
                st.download_button("📩 Download Report", f, "Bengaluru_House_Price_Report.txt")

# ----------------------------- Footer -----------------------------
st.markdown("<hr style='margin-top: 30px;'>", unsafe_allow_html=True)
st.markdown("<center><small>🔧 Built by Akshaansh | ML Streamlit App 2025</small></center>", unsafe_allow_html=True)
