import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
df = pd.read_csv(url)

print("Dataset Loaded Successfully!")
print(df.head())

# Features: 
# rm: average number of rooms per dwelling
# lstat: % lower status of the population
# pt-ratio: pupil-teacher ratio by town
# crim: per capita crime rate by town
# target (medv): Median value of owner-occupied homes in $1000's

X = df[['rm', 'lstat', 'ptratio', 'crim']]
y = df['medv']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\n--- Real Dataset Model Performance ---")
print(f"Mean Absolute Error (MAE): ${mean_absolute_error(y_test, y_pred) * 1000:,.2f}")
print(f"R2 Score (Accuracy): {r2_score(y_test, y_pred) * 100:.2f}%")

joblib.dump(model, 'real_estate_model.pkl')
print("\nSuccess: Real-world model saved as 'real_estate_model.pkl'")