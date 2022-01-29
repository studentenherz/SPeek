from flask import Blueprint, redirect, url_for, render_template, flash
from . import db, bcrypt, login_manager
from .forms import LoginForm, ChangePasswordForm
from .models import User
import random
from flask_login import login_user, logout_user, current_user

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.dashboard'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if bcrypt.check_password_hash( user.password, form.password.data):
				login_user(user)
				return redirect(url_for('main.dashboard'))
		else:
			flash('Incorrect user or password', 'error')

	return render_template('login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth.route('/change-password', methods=['GET', 'POST'])
def change_password():

	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=current_user.username).first()
		if user:
			if bcrypt.check_password_hash( user.password, form.current_password.data):
				user.password = bcrypt.generate_password_hash(form.new_password.data)
				db.session.add(user)
				db.session.commit()
				logout_user()
				return redirect(url_for('auth.login'))

	return render_template('change-password.html', form=form)

def register_admin():
	admin = User.query.filter_by(username='admin').first()
	if not admin:
		username = 'admin'
		password = str(random.randint(100000000, 999999999))
		hashed_password = bcrypt.generate_password_hash(password)
		new_user = User(username=username, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		print(f'User generated\nusername: admin\npassword: {password}\nMake sure to change the password for a more secure one on first login!')