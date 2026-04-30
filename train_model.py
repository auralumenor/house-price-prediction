import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_and_save_model(dataset_path="data/Ames_Housing_Data.csv"):
    print(f"Training the model on {dataset_path}...")
    df = pd.read_csv(dataset_path)
    
    # Verify required columns exist
    features = ["Gr Liv Area", "Bedroom AbvGr", "Full Bath", "Garage Cars", "Overall Qual", "Year Built"]
    required_columns = features + ["SalePrice"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Dataset is missing required column: {col}")

    df = df[required_columns].dropna()
    
    if len(df) == 0:
        raise ValueError("Dataset is empty after dropping missing values.")

    X = df[features]
    y = df["SalePrice"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    joblib.dump(rf_model, "model.joblib")
    print("Model saved to model.joblib successfully!")
    return rf_model

if __name__ == "__main__":
    train_and_save_model()
