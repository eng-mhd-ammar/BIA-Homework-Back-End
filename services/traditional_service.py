import pandas as pd
from sklearn.linear_model import LassoCV
import numpy as np

def run_traditional_on_df(df):
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    lasso = LassoCV(cv=5, random_state=42)
    lasso.fit(X, y)

    selected_features = [i for i, coef in enumerate(lasso.coef_) if coef != 0]

    best_chromosome = [1 if i in selected_features else 0 for i in range(X.shape[1])]

    feature_weights = lasso.coef_.tolist()

    stages = [{"alpha": a, "mse": float(m)} for a, m in zip(lasso.alphas_, np.mean(lasso.mse_path_, axis=1))]

    return {
        "best_chromosome": best_chromosome,
        "selected_features": selected_features,
        "feature_weights": feature_weights,
        "stages": stages
    }
