# House Price Prediction

This project predicts house prices using Kaggle's Ames Housing dataset.

## Features
- Uses **Linear Regression** (simple ML model)
- Uses **Random Forest** (stronger ML model)
- Evaluates models with **MSE** and **R²**
- Predicts price for a sample house

## Requirements
- pandas
- scikit-learn

## How to Run
1. Place `train.csv` in the `data/` folder
2. In `house_price.py`, change the dataset path on line 6 from `data/Ames_Housing_Data.csv` to `data/train.csv`
3. Run the script:
   ```bash
   python house_price.py
