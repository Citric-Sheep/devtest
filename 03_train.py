import pandas as pd
import pickle
from xgboost import XGBClassifier
from settings import PROCESSED_DATA_PATH, MODEL_PATH, FEATURES, TARGET, TEST_SIZE

def train():
    df = pd.read_pickle(PROCESSED_DATA_PATH)
    df["target"] = df[TARGET].shift(-1)
    df = df.dropna(subset=["target"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    X = df[FEATURES]
    y = df["target"].astype(int)
    split_index = int(len(df) * (1 - TEST_SIZE))
    X_train = X.iloc[:split_index]
    y_train = y.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_test = y.iloc[split_index:]
    model = XGBClassifier()
    model.fit(X_train, y_train)
    print(f"Train score: {model.score(X_train, y_train):.4f}")
    print(f"Test score: {model.score(X_test, y_test):.4f}")
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

if __name__ == "__main__":
    train()
