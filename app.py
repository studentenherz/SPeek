from flask import Flask, render_template
from peeker import peek

app = Flask(__name__)

@app.route('/')
def hello():
	state = peek()
	return render_template('dashboard.html', state=state)

if __name__ == '__main__':
	app.run(debug=True)