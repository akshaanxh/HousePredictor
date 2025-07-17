# 🏠 Bengaluru House Price Predictor

> 🌆 *A modern and interactive ML-powered app to estimate property prices in Bengaluru.*  
> Built with 💡 **Streamlit**, 🧠 **Scikit-learn**, and a sleek **glassmorphism UI**.

[![Streamlit App](https://img.shields.io/badge/🚀%20Live%20App-Click%20Here-brightgreen?style=for-the-badge)](https://housepredictor-dyyk36n9dpxqwdwjhsqdaa.streamlit.app/)  
[![MIT License](https://img.shields.io/github/license/akshaanxh/HousePredictor?style=flat-square)](LICENSE)

---

## ✨ Features

🔹 Predict house prices in Bengaluru using linear regression  
🔹 Clean **glass-style UI** with light/dark theme toggle  
🔹 Location input via searchable dropdown  
🔹 Instant, real-time results  
🔹 Built for speed, elegance, and simplicity

---

## 🖼️ Preview

![UI Screenshot](assets/preview.png)

---

## 🛠️ Tech Stack

| Layer        | Tools Used                              |
|--------------|------------------------------------------|
| **Frontend** | Streamlit, HTML/CSS (Glassmorphism)      |
| **Backend**  | Python, Pandas, NumPy, Scikit-learn      |
| **ML Model** | Linear Regression (trained on real data) |
| **Hosting**  | Streamlit Cloud                          |

---

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/akshaanxh/HousePredictor.git
cd HousePredictor

2. (Optional) Create and activate a virtual environment:

   python -m venv venv

   For Windows:
   venv\Scripts\activate

   For macOS/Linux:
   source venv/bin/activate

3. Install dependencies:

   pip install -r requirements.txt

4. Run the Streamlit app:

   streamlit run streamlit_app.py

## File Structure

- streamlit_app.py : Main Streamlit frontend
- BengaluruHouseTrainer.py : Model training script
- house_price_model.pkl : Pretrained regression model
- Bengaluru_House_Data.csv : Dataset used for model training
- assets/ : Folder for background images
- requirements.txt : Python dependencies

## Notes

- Make sure the `assets/` folder contains a valid background image for the UI.
- The trained model is loaded directly from the pickle file.
- You can toggle between dark and light modes within the app.

## License

This project is licensed under the MIT License.
