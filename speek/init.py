from . import app, db

with app.app_context():
	db.create_all()
	from .auth import register_admin
	register_admin()