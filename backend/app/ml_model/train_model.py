import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Paths (relative to train_model.py)
DATASET_PATH = os.path.join(os.path.dirname(__file__), "../../dataset/HousePricePredictionDataset.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "scaler.pkl")  # Save scaler for later use

def train_model():
    """Train the model with feature engineering and save it."""
    print("Training model...")
    print(f"Checking dataset path: {os.path.abspath(DATASET_PATH)}")
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
    
    # Load dataset
    df = pd.read_csv(DATASET_PATH)
    print(f"Initial dataset shape: {df.shape}")
    print(f"Initial columns: {df.columns.tolist()}")

    # 1. Remove duplicates
    df = df.drop_duplicates()
    print(f"After removing duplicates: {df.shape}")

    # 2. Handle null values (drop rows with any nulls for simplicity)
    df = df.dropna()
    print(f"After removing nulls: {df.shape}")

    # 3. Separate features and target
    X = df.drop(columns=["Id", "Price"])
    y = df["Price"]

    # 4. Encoding categorical variables
    categorical_cols = ["Location", "Condition", "Garage"]
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    print(f"After encoding: {X.columns.tolist()}")

    # 5. Scaling numerical features
    numerical_cols = ["Area", "Bedrooms", "Bathrooms", "Floors", "YearBuilt"]
    scaler = StandardScaler()
    X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
    print(f"Scaled numerical features: {numerical_cols}")

    # Train model
    model = LinearRegression()
    model.fit(X, y)
    print("Model trained successfully")

    # Save model and scaler
    print(f"Saving model to: {os.path.abspath(MODEL_PATH)}")
    print(f"Saving scaler to: {os.path.abspath(SCALER_PATH)}")
    try:
        joblib.dump(model, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)
        print(f"Model saved to {MODEL_PATH}")
        print(f"Scaler saved to {SCALER_PATH}")
    except Exception as e:
        print(f"Error saving model or scaler: {e}")

    return model, X.columns, scaler

def load_model():
    """Load the model and scaler if they exist, otherwise train them."""
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        print(f"Loading existing model from {MODEL_PATH}")
        print(f"Loading existing scaler from {SCALER_PATH}")
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        # Get feature columns from a sample DataFrame
        sample_df = pd.read_csv(DATASET_PATH).head(1)
        X_sample = sample_df.drop(columns=["Id", "Price"])
        X_sample = pd.get_dummies(X_sample, columns=["Location", "Condition", "Garage"], drop_first=True)
        feature_columns = X_sample.columns
    else:
        print("Model or scaler not found, training new model...")
        model, feature_columns, scaler = train_model()
    return model, feature_columns, scaler

# Update main.py to use the scaler in predictions
def preprocess_input(house_data, feature_columns, scaler):
    """Preprocess input data to match training format."""
    input_df = pd.DataFrame([house_data])
    input_df = pd.get_dummies(input_df, columns=["Location", "Condition", "Garage"])
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[feature_columns]
    numerical_cols = ["Area", "Bedrooms", "Bathrooms", "Floors", "YearBuilt"]
    input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])
    return input_df