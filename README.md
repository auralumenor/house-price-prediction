# Enterprise Property Valuation Analytics 🏢📊

An enterprise-grade house price prediction platform powered by Data Analytics (Comparative Market Analysis) and a beautifully designed, responsive web dashboard.

## 🌟 Key Features

- **Advanced Data Analysis**: Utilizes Comparative Market Analysis (CMA) to calculate similarity scores across housing metrics for highly accurate market valuations.
- **Enterprise Dashboard UI**: Modern, modular interface featuring Light/Dark/System theme switching, elegant CSS animations, and Toast popup notifications.
- **Dynamic Dataset Retraining**: Upload new CSV datasets directly from the UI. The backend automatically processes the new data to update predictions on the fly.
- **Real-Time Market Analytics**: Interactive Chart.js visualizations that map:
  - Average Price by Overall Quality
  - Dataset Price Spread Analysis
- **Vercel Ready**: Pre-configured for seamless serverless deployment on Vercel.

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Pandas, Werkzeug
- **Frontend**: HTML5, CSS3 (Custom Variables & Grid), Vanilla JavaScript
- **Data Visualization**: Chart.js, ApexCharts
- **Icons**: FontAwesome 6
- **Deployment**: Vercel

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

### 3. Run the Server Locally
```bash
python app.py
```
Navigate to `http://127.0.0.1:5000` in your web browser to access the dashboard.

### 4. Deploy to Vercel
This project is configured for Vercel. To deploy:
```bash
npm i -g vercel
vercel deploy
```
Or connect your GitHub repository directly via the Vercel Dashboard.

## 📂 Project Structure

```text
├── app.py                 # Core Flask application and REST API endpoints
├── house_price.py         # Data exploration and basic analysis script
├── requirements.txt       # Project dependencies
├── vercel.json            # Vercel serverless deployment configuration
├── .gitignore             # Configured to ignore local environments
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
