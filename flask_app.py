from flask import Flask,render_template,make_response,request,abort,jsonify,current_app
from bl.bncclient import spread_order, get_account_balances, get_all_tickers
from datetime import timedelta
from functools import update_wrapper,wraps

app = Flask(__name__)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/')
@crossdomain(origin='*')
def index():
        return render_template('index.html')

@app.route('/binance/tickers',  methods=['POST','OPTIONS'])
@crossdomain(origin='*', methods=['POST','OPTIONS'], headers=['content-type', 'access-control-allow-origin'])
def get_all_tickers_bnc():

        if not request.json:
                abort(400)

        api_key= request.json['apiKey']
        api_secret = request.json['apiSecret']
        try:
                return_log = get_all_tickers(api_key, api_secret)
                return valid_response(return_log)
        except Exception as e:
                return internal_server_error(e.message)  #status code 500

@app.route('/binance/account/balance',  methods=['POST','OPTIONS'])
@crossdomain(origin='*', methods=['POST','OPTIONS'], headers=['Content-Type'])
def binance_balances():

        if not request.json:
                abort(400)

        api_key= request.json['apiKey']
        api_secret = request.json['apiSecret']
        try:
                return_log = get_account_balances(api_key, api_secret)
                return valid_response(return_log)
        except Exception as e:
                return internal_server_error(e.message)  #status code 500

@app.route('/binance/spread', methods=['POST','OPTIONS'])
@crossdomain(origin='*', methods=['POST','OPTIONS'], headers=['Content-Type'])
def binanace_spread_order():

        if not request.json:
                abort(400)

        api_key= request.json['apiKey']
        api_secret = request.json['apiSecret']
        symbol = request.json['symbol']
        amount = request.json['amount']
        side = request.json['side']  #BUY/SELL
        first_order_percentage = request.json['first_order_percentage'] #first order percentage - market price
        spread = request.json['spread']  #how many orders
        spread_step_size_percentage = request.json['spread_step_size_percentage'] # percent from previous order (starting with market price)
        dry_mode = request.json['dry_mode']

        try:
                return_log = spread_order(
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
                return_log_str = '\n'.join(return_log)
                return valid_response(return_log_str)
        except Exception as e:
                return internal_server_error(e.message)  #status code 500

def valid_response(message):
    response = jsonify(message)
    response.status_code = 200
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def internal_server_error(message):
    response = jsonify({'error': message})
    response.status_code = 500
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


#if __name__ == '__main__':
#       app.run(debug=True, host='127.0.0.1')