# strategy_template.py
"""
Template for implementing trading strategies.
"""

class BaseStrategy:
    def __init__(self):
        pass

    def generate_signals(self, data):
        """Implement signal generation logic here."""
        raise NotImplementedError("Must implement generate_signals method")

# Example usage:
# class MyStrategy(BaseStrategy):
#     def generate_signals(self, data):
#         # Custom logic
#         return signals
