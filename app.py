from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import os
from werkzeug.utils import secure_filename
from train_model import train_and_save_model

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'data'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the trained model
MODEL_PATH = "model.joblib"
ACTIVE_DATASET = "data/Ames_Housing_Data.csv"
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_dataset():
    global model, ACTIVE_DATASET
    if 'dataset' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['dataset']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Train the model with the new dataset
            model = train_and_save_model(filepath)
            ACTIVE_DATASET = filepath
            return jsonify({"message": "Dataset uploaded and model retrained successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

@app.route("/predict", methods=["POST"])
def predict():
    global model
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.json
        # Expecting JSON data matching the features:
        # "Gr Liv Area", "Bedroom AbvGr", "Full Bath", "Garage Cars", "Overall Qual", "Year Built"
        
        sample_house = pd.DataFrame({
            "Gr Liv Area": [int(data.get("gr_liv_area", 0))],
            "Bedroom AbvGr": [int(data.get("bedroom_abvgr", 0))],
            "Full Bath": [int(data.get("full_bath", 0))],
            "Garage Cars": [int(data.get("garage_cars", 0))],
            "Overall Qual": [int(data.get("overall_qual", 0))],
            "Year Built": [int(data.get("year_built", 0))]
        })

        predicted_price = model.predict(sample_house)[0]
        return jsonify({"predicted_price": round(predicted_price, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/stats", methods=["GET"])
def get_stats():
    global model
    try:
        if not os.path.exists(ACTIVE_DATASET):
            return jsonify({"error": "Dataset not found"}), 404
            
        df = pd.read_csv(ACTIVE_DATASET)
        if "SalePrice" not in df.columns:
            return jsonify({"error": "SalePrice column missing"}), 400
            
        avg_price = float(round(df["SalePrice"].mean(), 2))
        max_price = float(round(df["SalePrice"].max(), 2))
        min_price = float(round(df["SalePrice"].min(), 2))
        total_records = int(len(df))
        
        # Price by Quality
        if "Overall Qual" in df.columns:
            quality_grouped = df.groupby("Overall Qual")["SalePrice"].mean().round(2)
            quality_labels = quality_grouped.index.astype(str).tolist()
            quality_values = [float(v) for v in quality_grouped.values]
        else:
            quality_labels, quality_values = [], []
            
        # Feature Importances from the active model
        features = ["Gr Liv Area", "Bedroom AbvGr", "Full Bath", "Garage Cars", "Overall Qual", "Year Built"]
        feature_importance = {}
        if model is not None and hasattr(model, 'feature_importances_'):
            importances = [float(v) for v in model.feature_importances_]
            feature_importance = dict(zip(features, importances))
            # Sort by importance descending
            feature_importance = dict(sorted(feature_importance.items(), key=lambda item: item[1], reverse=True))

        return jsonify({
            "avg_price": avg_price,
            "max_price": max_price,
            "min_price": min_price,
            "total_records": total_records,
            "quality_labels": quality_labels,
            "quality_values": quality_values,
            "feature_importance_labels": list(feature_importance.keys()),
            "feature_importance_values": list(feature_importance.values())
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/settings", methods=["POST"])
def update_settings():
    global model
    try:
        data = request.json
        n_estimators = int(data.get("n_estimators", 100))
        
        # Retrain model with new settings
        from sklearn.ensemble import RandomForestRegressor
        import joblib
        from sklearn.model_selection import train_test_split
        
        df = pd.read_csv(ACTIVE_DATASET)
        features = ["Gr Liv Area", "Bedroom AbvGr", "Full Bath", "Garage Cars", "Overall Qual", "Year Built"]
        df = df[features + ["SalePrice"]].dropna()
        X = df[features]
        y = df["SalePrice"]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
        model.fit(X_train, y_train)
        joblib.dump(model, MODEL_PATH)
        
        return jsonify({"message": f"Model updated with {n_estimators} estimators."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
