from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'data'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ACTIVE_DATASET = "data/Ames_Housing_Data.csv"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_dataset():
    global ACTIVE_DATASET
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
            ACTIVE_DATASET = filepath
            return jsonify({"message": "Dataset uploaded and set as active successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

@app.route("/predict", methods=["POST"])
def predict():
    if not os.path.exists(ACTIVE_DATASET):
        return jsonify({"error": "Active dataset not found"}), 500

    try:
        data = request.json
        gr_liv_area = int(data.get("gr_liv_area", 0))
        overall_qual = int(data.get("overall_qual", 5))
        year_built = int(data.get("year_built", 1970))
        bedroom_abvgr = int(data.get("bedroom_abvgr", 3))
        full_bath = int(data.get("full_bath", 2))
        garage_cars = int(data.get("garage_cars", 2))

        # Advanced Data Analysis: Comparative Market Analysis (CMA)
        # Find the most similar properties by calculating a similarity score
        df = pd.read_csv(ACTIVE_DATASET)
        
        # Calculate standard deviations for normalization
        std_area = df['Gr Liv Area'].std() or 1
        std_qual = df['Overall Qual'].std() or 1
        std_year = df['Year Built'].std() or 1
        std_bed = df['Bedroom AbvGr'].std() or 1
        std_bath = df['Full Bath'].std() or 1
        std_garage = df['Garage Cars'].std() or 1
        
        # Calculate distance (lower is more similar)
        df['similarity_score'] = (
            abs(df['Gr Liv Area'] - gr_liv_area) / std_area +
            abs(df['Overall Qual'] - overall_qual) / std_qual +
            abs(df['Year Built'] - year_built) / std_year +
            abs(df['Bedroom AbvGr'] - bedroom_abvgr) / std_bed +
            abs(df['Full Bath'] - full_bath) / std_bath +
            abs(df['Garage Cars'] - garage_cars) / std_garage
        )
        
        # Get the top 5 most similar comparable properties
        similar_properties = df.sort_values('similarity_score').head(5)
        predicted_price = similar_properties['SalePrice'].mean()
        
        return jsonify({"predicted_price": round(predicted_price, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/stats", methods=["GET"])
def get_stats():
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
        total_volume = float(df["SalePrice"].sum())
        avg_area = float(round(df["Gr Liv Area"].mean(), 2))
        
        # Price by Quality
        if "Overall Qual" in df.columns:
            quality_grouped = df.groupby("Overall Qual")["SalePrice"].mean().round(2)
            quality_labels = quality_grouped.index.astype(str).tolist()
            quality_values = [float(v) for v in quality_grouped.values]
        else:
            quality_labels, quality_values = [], []

        if "Yr Sold" in df.columns and "Mo Sold" in df.columns:
            df_sorted = df.sort_values(by=["Yr Sold", "Mo Sold"])
            df_sorted['Period'] = df_sorted['Yr Sold'].astype(str) + "-" + df_sorted['Mo Sold'].astype(str).str.zfill(2) + "-01"
            
            candle_data = df_sorted.groupby('Period').agg(
                Open=('SalePrice', 'first'),
                High=('SalePrice', 'max'),
                Low=('SalePrice', 'min'),
                Close=('SalePrice', 'last'),
                Volume=('SalePrice', 'sum'),
                Transactions=('SalePrice', 'count')
            ).reset_index()
            
            candle_dict = candle_data.rename(columns={
                'Period': 'x',
                'Open': 'o',
                'High': 'h',
                'Low': 'l',
                'Close': 'c',
                'Volume': 'volume',
                'Transactions': 'transactions'
            }).to_dict(orient='records')
        else:
            candle_dict = []

        return jsonify({
            "avg_price": avg_price,
            "max_price": max_price,
            "min_price": min_price,
            "total_records": total_records,
            "total_volume": total_volume,
            "avg_area": avg_area,
            "quality_labels": quality_labels,
            "quality_values": quality_values,
            "candle_data": candle_dict
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/settings", methods=["POST"])
def update_settings():
    return jsonify({"message": "Settings updated (Data analysis mode active)."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
