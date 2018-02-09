from flask import Flask,render_template,make_response,request,abort,jsonify
from bl.client import run as run_logic

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/run')
def run():
	run_logic()
	return 'done kapara'

@app.route('/request', methods=['POST'])
def post_example():
	if not request.json:
		abort(400)
	print(request.json['title'])
	return jsonify('{task:1}'), 200


if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1')
