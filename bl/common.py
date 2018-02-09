
	
def get_symbol_precision(client, symbol):
	symbol_info = client.get_symbol_info(symbol=symbol)
	filters = symbol_info['filters']
	for symbol_filter in filters:
		if (symbol_filter['filterType'] == 'LOT_SIZE'):
			return get_precision(symbol_filter['minQty'])
	return 0	


def get_precision(min_quantity):
	if (float(min_quantity) == 0.001):
		return 3
	if (float(min_quantity) == 0.01):
		return 2
	if (float(min_quantity) == 0.1):
		return 1
	return 0	

