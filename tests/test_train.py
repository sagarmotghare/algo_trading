import unittest
import pandas as pd
from train import calculate_moving_avg, get_train_test_data, train_model

class TestModelTraining(unittest.TestCase):
    def setUp(self):
        # Create sample data
        data = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]
        })
        self.data = calculate_moving_avg(data)

    def test_train_model(self):
        X_train, X_test, y_train, y_test = get_train_test_data(self.data)
        model, predictions = train_model(X_train, X_test, y_train, y_test)
        self.assertEqual(len(predictions), len(y_test))

if __name__ == "__main__":
    unittest.main()
