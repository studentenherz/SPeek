from flask import Flask, render_template, jsonify, redirect, url_for
from peeker import peek, system_info
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.getenv('SPEEK_KEY', 'default_secret_key_not_very_secret')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	password = db.Column(db.String(80), nullable=False)

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'username'})
	password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'password'})
	submit = SubmitField('Login')

class ChangePassword(FlaskForm):
	current_password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Current password'})
	new_password = PasswordField(validators=[InputRequired(), Length(min=4, max=20), EqualTo('new_password_confirmation', message='Unmatching passwords.')	], render_kw={'placeholder': 'New password'})
	new_password_confirmation = PasswordField('Repeat Password', render_kw={'placeholder' : 'Repeat Password'})
	submit = SubmitField('Change')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if bcrypt.check_password_hash( user.password, form.password.data):
				login_user(user)
				return redirect(url_for('dashboard'))

	return render_template('login.html', form=form)

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():

	form = ChangePassword()
	if form.validate_on_submit():
		user = User.query.filter_by(username=current_user.username).first()
		if user:
			if bcrypt.check_password_hash( user.password, form.current_password.data):
				user.password = bcrypt.generate_password_hash(form.new_password.data)
				db.session.add(user)
				db.session.commit()
				logout_user()
				return redirect(url_for('login'))

	return render_template('change-password.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
	return render_template('dashboard.html', system_info=system_info)

@app.route('/getStatus')
@login_required
def get_status():
	status = peek()
	return jsonify(status)

def register_admin():
	admin = User.query.filter_by(username='admin').first()
	if not admin:
		username = 'admin'
		password = 'admin'
		hashed_password = bcrypt.generate_password_hash(password)
		new_user = User(username=username, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()

if __name__ == '__main__':
	app.run(debug=True)