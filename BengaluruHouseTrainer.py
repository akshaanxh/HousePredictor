# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 21:19:26 2025

@author: HII
"""

# -*- coding: utf-8 -*-
"""
BengaluruHousePredictor.py
Clean version for Spyder/local Python IDEs
"""

# 📌 1. Import Libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

# 📌 2. Load Dataset
df = pd.read_csv("C:/Users/HII/Desktop/MACHINE LEARNING/ML PROJECTS/House_Price Predictor/Bengaluru_House_Data.csv")

# 📌 3. Preprocess
df = df.dropna()

# Remove rows with non-numeric total_sqft values
df = df[df['total_sqft'].apply(lambda x: x.replace('.', '', 1).isdigit())]
df['total_sqft'] = df['total_sqft'].astype(float)

# Remove extreme values
df = df[df['bath'] < 10]

# Extract bhk from 'size' (e.g., "3 BHK")
df['bhk'] = df['size'].apply(lambda x: int(x.split(' ')[0]))

# 📌 4. Encode 'location'
le = LabelEncoder()
df['location'] = le.fit_transform(df['location'])

# 📌 5. Features and Labels
X = df[['location', 'total_sqft', 'bath', 'bhk']]
y = df['price']

# 📌 6. Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# 📌 7. Save model and encoder
with open("house_price_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("location_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("✅ Model and encoder saved successfully.")
