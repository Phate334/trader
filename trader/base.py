class BaseStrategy:
    """Base class for all strategies."""

    def __init__(self, strategy_name):
        self.strategy_name = strategy_name

    def run_backtest(self):
        """Run backtest and return position."""
        pass

    def load_position(self):
        pass
