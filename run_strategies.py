"""Run all strategies in the strategies folder."""
import logging

from strategies import enable_strategies

if __name__ == "__main__":
    for i, strategy in enumerate(enable_strategies):
        logging.info("Running strategy %d of %d", i + 1, len(enable_strategies))
        new_position = strategy.do_backtest()
