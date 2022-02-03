from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from .peeker import peek, system_info, PeekNetwork
from . import socketio
from flask_socketio import emit
import gevent

main = Blueprint('main', __name__)

netpeek = PeekNetwork()

@main.route('/')
@login_required
def dashboard():
	return render_template('dashboard.html', system_info=system_info, nics=netpeek.nics)

@main.route('/getStatus')
@login_required
def get_status():
	status = peek()
	return jsonify(status)

@socketio.on('ready', namespace='/socket')
@login_required
def send_network_data():
	emit('nics', netpeek.nics, namespace='/socket')
	while True:
		newdata = netpeek.peek()
		emit('networkdata', newdata, namespace='/socket')
		gevent.sleep(0.1) 