from binance.client import Client  #https://github.com/sammchardy/python-binance
import random
import common
from decimal import Decimal


def run():

	client = Client('', '')

	symbol = 'BNTBTC'
	amount = 50
	side = Client.SIDE_BUY  #BUY/SELL
	first_order_percentage = 30.0  #first order percentage - market price
	spread = 7  #how many orders
	spread_step_size_percentage = 5.0 # percent from previous order (starting with market price)

	#metadata
	dryMode = True
	side_str = 'selling' if side == Client.SIDE_SELL else 'buying'

	account = client.get_account()

	symbol_info = client.get_symbol_ticker(symbol=symbol)
	market_price = symbol_info['price']
	print('current market price: ' + market_price)

	precision = common.get_symbol_precision(client, symbol)
	quantity_first_order = round(Decimal((first_order_percentage/100.0) * amount), precision)
	quantity_spread = amount - quantity_first_order

	print(side_str + ' ' + str(quantity_first_order) + ' ' + symbol + ' at MARKET price')
	print(side_str + ' ' + str(quantity_spread) + ' ' + symbol + ' at SPREAD')


	if (quantity_first_order > 0):
		#1. Place Market BUY order
		if not dryMode:
			try:
				client.create_order(
			    	symbol=symbol,
			    	type=Client.ORDER_TYPE_MARKET,
			    	side=side,
			    	quantity=quantity_first_order)
			except Exception as e:
				print(e)


	if (quantity_spread > 0):	
		
		base = quantity_spread / (spread-1)
		for i in range(1,spread):
			
			quantity_spread_i = base - (i * random.uniform(0.01, 0.03))
			quantity_spread_i_rounded = round(Decimal(quantity_spread_i), precision)

			price_i = float(market_price) 
			if side == Client.SIDE_SELL:
				price_i += i * (float(market_price) * (spread_step_size_percentage/100.0)) #sell above market price
			else:
				price_i -= i * (float(market_price) * (spread_step_size_percentage/100.0)) #buy below market price

			price_i_rounded = float("{0:.7f}".format(price_i))

			print(side_str + ' ' + str(quantity_spread_i_rounded) + ' ' + symbol[0:3] + ' at ' + str(price_i_rounded) + ' price')

			if not dryMode:
				try:
					client.create_order(
						symbol=symbol,
						quantity=quantity_spread_i_rounded,
						side=side,
						type=Client.ORDER_TYPE_LIMIT,
						price=price_i_rounded,
						timeInForce=Client.TIME_IN_FORCE_GTC)
				except Exception as e:
					print(e)




