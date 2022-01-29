from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from . import db
from .peeker import peek, system_info

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
	return render_template('dashboard.html', system_info=system_info)

@main.route('/getStatus')
@login_required
def get_status():
	status = peek()
	return jsonify(status)