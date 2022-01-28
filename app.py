from flask import Flask, render_template, jsonify
from peeker import peek

app = Flask(__name__)

@app.route('/')
def dashboard():
	return render_template('dashboard.html')

@app.route('/getStatus')
def get_status():
	status = peek()
	return jsonify(status)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')