
import numpy as np
from sklearn.linear_model import LinearRegression

class AIPredictiveAnalyzer:
    def __init__(self):
        self.model = LinearRegression()
        print("--> AI Predictive Analytics engine ready hai!")

    def train_and_predict_failure(self, time_ticks, budget_history):
        # Time ticks ko 2D array mein badalna padta hai sklearn ke liye
        X = np.array(time_ticks).reshape(-1, 1)
        y = np.array(budget_history)

        # Model ko train kar rahe hain
        self.model.fit(X, y)

        # Agle 3 ticks mein budget kahan jayega, woh predict karenge
        future_ticks = np.array([[max(time_ticks) + 1], [max(time_ticks) + 2], [max(time_ticks) + 3]])
        predictions = self.model.predict(future_ticks)

        print(f"--> AI Projections for next 3 ticks: {predictions.tolist()}")
        
        # Agar predicted budget negative hone laga toh warning trigger kar do
        if any(p < 0 for p in predictions):
            return "WARNING: AI predicts a potential budget crash or power failure soon!"
        else:
            return "STATUS: Infrastructure is stable for the near future."

# Test karne ke liye
if __name__ == "__main__":
    ai = AIPredictiveAnalyzer()
    ticks = [1, 2, 3, 4, 5]
    budgets = [10000000, 9800000, 9500000, 9200000, 9000000]
    result = ai.train_and_predict_failure(ticks, budgets)
    print(result)