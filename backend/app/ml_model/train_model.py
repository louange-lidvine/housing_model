import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# Paths (relative to train_model.py)
DATASET_PATH = os.path.join(os.path.dirname(__file__), "../../dataset/HousePricePredictionDataset.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

def train_model():
    """Train the model and save it to model.pkl."""
    print("Training model...")
    print(f"Checking dataset path: {os.path.abspath(DATASET_PATH)}")
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    print(f"Loaded dataset with shape: {df.shape}")
    print(f"Dataset columns: {df.columns.tolist()}")

    # Preprocess categorical variables
    df = pd.get_dummies(df, columns=["Location", "Condition", "Garage"], drop_first=True)
    print(f"After preprocessing: {df.columns.tolist()}")

    # Features and target
    X = df.drop(columns=["Id", "Price"])
    y = df["Price"]
    print(f"Features: {X.columns.tolist()}, Target shape: {y.shape}")

    # Train model
    model = LinearRegression()
    model.fit(X, y)
    print("Model trained successfully")

    # Save model
    print(f"Saving model to: {os.path.abspath(MODEL_PATH)}")
    try:
        joblib.dump(model, MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")
    except Exception as e:
        print(f"Error saving model: {e}")
    return model, X.columns

def load_model():
    """Load the model if it exists, otherwise train it."""
    if os.path.exists(MODEL_PATH):
        print(f"Loading existing model from {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
        sample_df = pd.read_csv(DATASET_PATH).head(1)
        sample_df = pd.get_dummies(sample_df, columns=["Location", "Condition", "Garage"], drop_first=True)
        feature_columns = sample_df.drop(columns=["Id", "Price"]).columns
    else:
        print("Model not found, training new model...")
        model, feature_columns = train_model()
    return model, feature_columns