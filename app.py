from flask import Flask,render_template,make_response,request,abort,jsonify
from bl.client import run as run_logic

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():

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

	return_log = run_logic(
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

	return jsonify(return_log), 200
	

if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1')
