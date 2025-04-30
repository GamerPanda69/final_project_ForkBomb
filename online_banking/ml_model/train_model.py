import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

print("Starting script...")

# Load data
print("Loading dataset...")
df = pd.read_csv('loan_amount_prediction_dataset_v2.csv')
print("Dataset loaded, shape:", df.shape)

# Prepare features and target
print("Preparing features and target...")
X = df.drop('Loan_Amount', axis=1)
y = df['Loan_Amount']
print("Features shape:", X.shape, "Target shape:", y.shape)

# Train model
print("Training model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)
print("Model training complete.")

# Save model
model_path = os.path.join('ml_model', 'loan_model.pkl')
print("Saving model to:", model_path)
joblib.dump(model, model_path)
print("Model saved successfully.")