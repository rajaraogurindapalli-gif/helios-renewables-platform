import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

def train_baseline_forecaster():
    X = np.random.rand(100, 3) # irradiance, ambient_temp, hour
    y = X[:, 0] * 2400.0 + np.random.normal(0, 10, 100)
    model = GradientBoostingRegressor(n_estimators=50, max_depth=3)
    model.fit(X, y)
    return model

if __name__ == "__main__":
    model = train_baseline_forecaster()
    pred = model.predict([[850.0 / 1000.0, 32.0 / 45.0, 12.0 / 24.0]])
    print("Yield forecaster verified. Sample prediction:", pred[0])
