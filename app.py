from flask import Flask,render_template,make_response,request,abort,jsonify
from bl.binance.client import run as binance_spread_order

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/binance/spread', methods=['POST'])
def binanace_spread_order():

	if not request.json:
		abort(400)

	api_key= request.json['api_key']
	api_secret = request.json['api_secret']
	symbol = request.json['symbol']
	amount = request.json['amount']
	side = request.json['side']  #BUY/SELL
	first_order_percentage = request.json['first_order_percentage'] #first order percentage - market price
	spread = request.json['spread']  #how many orders
	spread_step_size_percentage = request.json['spread_step_size_percentage'] # percent from previous order (starting with market price)
	dry_mode = request.json['dry_mode']

	try:
		return_log = binance_spread_order(
			api_key=api_key,
			api_secret = api_secret,
			symbol = symbol,
			amount = amount,
			side = side,
			first_order_percentage = first_order_percentage,
			spread = spread,
			spread_step_size_percentage = spread_step_size_percentage,
			dry_mode=dry_mode
		)
		return valid_response(return_log)
	except Exception as e:
		return internal_server_error(e.message)  #status code 500

def valid_response(message):
    response = jsonify(message)
    response.status_code = 200
    return response
	
def internal_server_error(message):
    response = jsonify({'error': message})
    response.status_code = 500
    return response


if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1')#, ssl_context='adhoc')
