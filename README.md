# Enterprise Property Valuation Analytics 🏢📊

An enterprise-grade house price prediction platform powered by machine learning (Random Forest Regression) and a beautifully designed, responsive web dashboard.

## 🌟 Key Features

- **Advanced Machine Learning**: Utilizes `scikit-learn`'s Random Forest regression algorithm to process multiple housing metrics for highly accurate market valuations.
- **Enterprise Dashboard UI**: Modern, modular interface featuring Light/Dark/System theme switching, elegant CSS animations, and Toast popup notifications.
- **Dynamic Dataset Retraining**: Upload new CSV datasets directly from the UI. The backend automatically processes the new data and retrains the AI model on the fly.
- **Real-Time Market Analytics**: Interactive Chart.js visualizations that map:
  - Model Feature Importance
  - Average Price by Overall Quality
  - Dataset Price Spread Analysis
- **Algorithm Configuration**: Fine-tune the underlying Random Forest hyper-parameters (e.g., Number of Estimators) directly from the dashboard settings.

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Pandas, Joblib
- **Machine Learning**: scikit-learn (RandomForestRegressor)
- **Frontend**: HTML5, CSS3 (Custom Variables & Grid), Vanilla JavaScript
- **Data Visualization**: Chart.js
- **Icons**: FontAwesome 6

## 🚀 Quick Start Guide

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd House_Price_Prediction
```

### 2. Install Dependencies
Ensure you have Python 3.8+ installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Initialize the Model
Before running the application server, you need to build the initial machine learning model.
```bash
python train_model.py
```
*This script will compile `model.joblib` using the default Ames Housing dataset.*

### 4. Run the Server
```bash
python app.py
```
Navigate to `http://127.0.0.1:5000` in your web browser to access the dashboard.

## 📂 Project Structure

```text
├── app.py                 # Core Flask application and REST API endpoints
├── train_model.py         # Machine learning training pipeline and data validation
├── requirements.txt       # Project dependencies
├── .gitignore             # Configured to ignore local environments and model artifacts
├── data/                  # Directory storing CSV datasets
├── static/
│   └── style.css          # Extensive CSS architecture (Themes, Grids, Animations)
└── templates/
    └── index.html         # Frontend Single Page Application (SPA)
```

## 🔐 Custom Data Requirements
If you choose to upload a custom dataset via the dashboard, ensure your CSV contains the following exact column headers to prevent processing errors:
- `SalePrice` (Target Variable)
- `Gr Liv Area`
- `Year Built`
- `Bedroom AbvGr`
- `Full Bath`
- `Garage Cars`
- `Overall Qual`

## 🤝 Contributing
Contributions are welcome. Please ensure your code adheres to standard PEP-8 guidelines and that frontend changes preserve the responsive design system.
