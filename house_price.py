import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load dataset
df = pd.read_csv("data/Ames_Housing_Data.csv")

# Step 2: Basic analysis
print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

# Step 3: Price distribution
plt.hist(df["SalePrice"], bins=30, color="skyblue", edgecolor="black")
plt.title("House Price Distribution")
plt.xlabel("Price")
plt.ylabel("Count")
plt.show()

# Step 4: Relationship between area and price
plt.scatter(df["Gr Liv Area"], df["SalePrice"], alpha=0.5, color="green")
plt.title("Living Area vs Sale Price")
plt.xlabel("Living Area (sq ft)")
plt.ylabel("Sale Price")
plt.show()

# Step 5: Simple prediction using average price per sq ft
df["PricePerSqFt"] = df["SalePrice"] / df["Gr Liv Area"]
avg_price_per_sqft = np.mean(df["PricePerSqFt"])
print("Average Price per Sq Ft:", avg_price_per_sqft)

# Predict price for a sample house
sample_area = 1500
predicted_price = sample_area * avg_price_per_sqft
print(f"Predicted Price for {sample_area} sq ft house: ₹{predicted_price:,.0f}")
