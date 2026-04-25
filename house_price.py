import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
df = pd.read_csv("data/Ames_Housing_Data.csv")
features = ["Gr Liv Area", "Bedroom AbvGr", "Full Bath", "Garage Cars", "Overall Qual", "Year Built"]
df = df[features + ["SalePrice"]].dropna()
X = df[features]
y = df["SalePrice"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
lin_model = LinearRegression()
lin_model.fit(X_train, y_train)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
lin_pred = lin_model.predict(X_test)
rf_pred = rf_model.predict(X_test)

print("Linear Regression:")
print("  MSE:", mean_squared_error(y_test, lin_pred))
print("  R²:", r2_score(y_test, lin_pred))

print("\nRandom Forest:")
print("  MSE:", mean_squared_error(y_test, rf_pred))
print("  R²:", r2_score(y_test, rf_pred))
sample_house = pd.DataFrame({
    "Gr Liv Area": [1500],
    "Bedroom AbvGr": [3],
    "Full Bath": [2],
    "Garage Cars": [1],
    "Overall Qual": [6],
    "Year Built": [2005]
})

predicted_price = rf_model.predict(sample_house)[0]
print(f"\nPredicted Price for sample house: ₹{predicted_price:,.0f}")
