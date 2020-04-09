from backtester import BackTester, Strategy1
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
	stock_market_prices = pd.read_csv("stock_prices_train.csv", index_col = 0)
	risk_free_rates = pd.read_csv("risk_free_train.csv", index_col = 0) 
	strategy_capm = Strategy1()
	BT = BackTester(stock_market_prices, risk_free_rates, strategy_capm)
	BT.run(verbose = False)

	sns_plot = sns.distplot(BT.dailiy_excR)

	BT.evaluate()
	plt.show()

	sns_plot.savefig("capm_vs_baseline.png")