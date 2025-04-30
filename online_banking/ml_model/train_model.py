# ml_model/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

print("Starting model training script...")

# --- Configuration ---
CSV_FILE_PATH = 'loan_amount_prediction_dataset_v2.csv'
MODEL_DIR = 'ml_model'
MODEL_FILENAME = 'loan_model.pkl'
MODEL_SAVE_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
# --- End Configuration ---

# Check if dataset exists
if not os.path.exists(CSV_FILE_PATH):
    print(f"Error: Dataset file not found at '{CSV_FILE_PATH}'")
    print("Please ensure the CSV file is in the correct location.")
    exit(1) # Exit the script if data is missing

# Create model directory if it doesn't exist
os.makedirs(MODEL_DIR, exist_ok=True)
print(f"Ensured model directory exists: '{MODEL_DIR}'")

try:
    # Load data
    print(f"Loading dataset from '{CSV_FILE_PATH}'...")
    df = pd.read_csv(CSV_FILE_PATH)
    print("Dataset loaded successfully. Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    # --- Data Preparation ---
    feature_columns = [
        'Age', 'Monthly_Income', 'Credit_Score', 'Loan_Tenure_Years',
        'Existing_Loan_Amount', 'Num_of_Dependents' # Corrected name
    ]
    target_column = 'Loan_Amount'

    # Check if all expected columns exist
    missing_features = [col for col in feature_columns if col not in df.columns]
    if missing_features:
        print(f"Error: Missing feature columns in CSV: {missing_features}")
        exit(1)
    if target_column not in df.columns:
        print(f"Error: Missing target column in CSV: '{target_column}'")
        exit(1)

    # *** DATA CLEANING STEP ***
    # Ensure Loan_Amount is not negative before training
    print(f"Cleaning target column '{target_column}' (replacing negative values with 0)...")
    original_neg_count = (df[target_column] < 0).sum()
    if original_neg_count > 0:
        df[target_column] = df[target_column].apply(lambda x: max(x, 0))
        print(f"Replaced {original_neg_count} negative values in '{target_column}' with 0.")
    else:
        print(f"No negative values found in '{target_column}'.")
    # *** END DATA CLEANING STEP ***

    # Handle potential missing values in features (example: fill with median)
    print("Handling missing values in features (if any)...")
    for col in feature_columns:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"Filled missing values in '{col}' with median ({median_val}).")

    # Prepare features (X) and target (y)
    print("Preparing features (X) and target (y)...")
    X = df[feature_columns]
    y = df[target_column]
    print("Features shape:", X.shape, "Target shape:", y.shape)
    print("Feature columns used:", feature_columns)

    # Train model
    print("Training RandomForestRegressor model...")
    model = RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1, max_depth=10, min_samples_split=5)
    model.fit(X, y)
    print("Model training complete.")

    # Save model
    print(f"Saving model to: '{MODEL_SAVE_PATH}'")
    joblib.dump(model, MODEL_SAVE_PATH)
    print("Model saved successfully.")

except FileNotFoundError:
    print(f"Error: Dataset file not found during processing at '{CSV_FILE_PATH}'")
except KeyError as e:
    print(f"Error: Column not found in dataset - {e}. Please check CSV column names.")
    print("Expected features:", feature_columns)
    print("Expected target:", target_column)
except Exception as e:
    print(f"An unexpected error occurred during training: {e}")
    import traceback
    traceback.print_exc()