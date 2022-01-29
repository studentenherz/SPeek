from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'username'})
	password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'password'})
	submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
	current_password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Current password'})
	new_password = PasswordField(validators=[InputRequired(), Length(min=4, max=20), EqualTo('new_password_confirmation', message='Unmatching passwords.')	], render_kw={'placeholder': 'New password'})
	new_password_confirmation = PasswordField('Repeat Password', render_kw={'placeholder' : 'Repeat Password'})
	submit = SubmitField('Change')