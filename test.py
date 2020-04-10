from backtester import Strategy 
import pandas as pd 
import numpy as np 


def train_test_split(df, split_rate = 0.6):
	num_r, num_c = df.shape[0], df.shape[1]
	cut = int(num_r * split_rate)
	train, test = df.iloc[:cut, :], df.iloc[cut:, :]

	return train, test

def main():
	stock_prices = pd.read_csv("stock_prices_train.csv", index_col = 0)
	risk_free_rates = pd.read_csv("risk_free_train.csv", index_col = 0)
	st = Strategy()

	stock_prices_train, stock_prices_test = train_test_split(stock_prices)



	st.fit(stock_prices_train, risk_free_rates)

if __name__ == "__main__":
	main()