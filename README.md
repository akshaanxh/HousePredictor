# Bengaluru House Price Predictor

A minimal yet beautiful machine learning web app to predict house prices in Bengaluru using a linear regression model. Built using Streamlit with a clean glassmorphism interface.

## Features

- Predict house prices based on input features
- Location input via dropdown or interactive map
- Light and dark theme toggle
- Custom glass UI using HTML/CSS
- Model trained on Bengaluru housing data

## Installation

1. Clone the repository:

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
