import pandas as pd
import numpy as np 

class Strategy:
	def __init__(self):
		self.stock_prices = []
		self.market_prices = []
		self.risk_free_rates = []

	def allocate_portfolio(self, stock_price, market_price, risk_free_rate):	
		self.stock_prices.append(list(stock_price))
		self.market_prices.append(market_price)
		self.risk_free_rates.append(risk_free_rate)
		
		# self.stock_prices, self.market_prices, self.risk_free_rates = np.array(self.stock_prices), np.array(self.market_prices), np.array(self.risk_free_rates)
		# Write Your Strategy Here
		n_stocks = len(stock_price)
		weights = np.repeat(1 / n_stocks, n_stocks)
		return weights

class BackTester:
	def __init__(self, stock_market_prices, risk_free_rates, strategy):
		def transform_rates(rates):
			rates = np.array(rates)
			ret = []
			for i in rates:
				ret.extend([i[0] for _ in range(21)])	
			return ret
		self.stock_prices = stock_market_prices.iloc[:, :-1]
		self.market_prices = stock_market_prices.iloc[:, -1]
		self.risk_free_rates = transform_rates(risk_free_rates)	
		self.strategy = strategy

	def run(self, verbose=True):
		def calc_excR(s_p, r, pre_pos, pre_data):
			pre_stock_price, pre_r = pre_data[0], pre_data[1]
			stock_returns = (np.array(s_p) - np.array(pre_stock_price)) / np.array(s_p)
			return np.sum(stock_returns * np.array(pre_pos))
		cur_position = np.array([None] * np.shape(self.stock_prices)[1])
		pre_data = (None, None, None) 	# For Return Calculation
		self.dailiy_excR = [] 	# Daily Excessive Return	
		for ((idx, stock_price), market_price, risk_free_rate) in zip(self.stock_prices.iterrows(), self.market_prices, self.risk_free_rates):
			if cur_position.any() != None:
				self.dailiy_excR.append(calc_excR(stock_price, risk_free_rate, cur_position, pre_data))
				if verbose:
					print(f"Daily Excessive Return {idx}:" ,self.dailiy_excR[-1])
			cur_position = self.strategy.allocate_portfolio(stock_price, market_price, risk_free_rate)
			pre_data = (stock_price, risk_free_rate)

	def evaluate(self):
		def calc_sharp(daily_excR, r):
			return (np.mean(daily_excR) - r) / np.sqrt(np.var(daily_excR)) * np.sqrt(252)
		print("-------Evaluation-------")
		print("  Year  |   Annulized Sharp Ratio")
		a_sharps = []
		for i in range(10):
			a_sharp = calc_sharp(self.dailiy_excR[i:i+120], self.risk_free_rates[i + 120])
			a_sharps.append(a_sharp)
			print(f"    {i}   |   {a_sharp}  ")
		print(f"Mean: {np.mean(a_sharps)}")