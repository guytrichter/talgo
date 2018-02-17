from binance.client import Client  #https://github.com/sammchardy/python-binance
import random
import common
from decimal import Decimal


def run(api_key, api_secret, symbol, amount, side, first_order_percentage, spread, spread_step_size_percentage, dry_mode):

	list = ['starting run']
	
	client = Client(api_key, api_secret)

	side_str = 'selling' if side == 'SELL' else 'buying'

	account = client.get_account()

	symbol_info = client.get_symbol_ticker(symbol=symbol)
	market_price = symbol_info['price']
	list.append('current market price: ' + market_price)

	precision = common.get_symbol_precision(client, symbol)
	quantity_first_order = round(Decimal((first_order_percentage/100.0) * amount), precision)
	quantity_spread = amount - quantity_first_order

	list.append(side_str + ' ' + str(quantity_first_order) + ' ' + symbol + ' at MARKET price')
	list.append(side_str + ' ' + str(quantity_spread) + ' ' + symbol + ' at SPREAD')


	if (quantity_first_order > 0):
		#1. Place Market BUY order
		if not dry_mode:		
			client.create_order(
		    	symbol=symbol,
		    	type=Client.ORDER_TYPE_MARKET,
		    	side=side,
		    	quantity=quantity_first_order)


	if (quantity_spread > 0):	
		
		base = quantity_spread / (spread-1)
		curr = quantity_spread

		for i in range(1,spread):
			
			quantity_spread_i = base - (i * random.uniform(0.01, 0.03))
			quantity_spread_i_rounded = round(Decimal(quantity_spread_i), precision)

			if i == spread-1:
				#last cycle - adjust quantity
				if curr != quantity_spread_i:
					quantity_spread_i_rounded = round(Decimal(curr), precision)

			curr = curr - quantity_spread_i_rounded

			price_i = float(market_price) 
			if side == Client.SIDE_SELL:
				price_i += i * (float(market_price) * (spread_step_size_percentage/100.0)) #sell above market price
			else:
				price_i -= i * (float(market_price) * (spread_step_size_percentage/100.0)) #buy below market price

			price_i_rounded = float("{0:.7f}".format(price_i))

			list.append(side_str + ' ' + str(quantity_spread_i_rounded) + ' ' + symbol[0:3] + ' at ' + str(price_i_rounded) + ' price')

			if not dry_mode:
				client.create_order(
					symbol=symbol,
					quantity=quantity_spread_i_rounded,
					side=side,
					type=Client.ORDER_TYPE_LIMIT,
					price=price_i_rounded,
					timeInForce=Client.TIME_IN_FORCE_GTC)

	return list




