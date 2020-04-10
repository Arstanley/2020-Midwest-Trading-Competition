from backtester import BackTester, Strategy
import pandas as pd

if __name__ == "__main__":
	stock_market_prices = pd.read_csv("stock_prices_train.csv", index_col = 0)
	risk_free_rates = pd.read_csv("risk_free_train.csv", index_col = 0) 
	strategy = Strategy()
	BT = BackTester(stock_market_prices, risk_free_rates, strategy)
	BT.run(verbose = True)
	BT.evaluate()