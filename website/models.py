from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeeklyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.String(10), nullable=False)
    total_items = db.Column(db.Float, nullable=False)
    most_popular_item = db.Column(db.String(10), nullable=False)
    least_popular_item = db.Column(db.String(10), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    max_cost = db.Column(db.Float, nullable=False)
    min_cost = db.Column(db.Float, nullable=False)
    average_cost = db.Column(db.Float, nullable=False)
    least_popular_payment = db.Column(db.String(10), nullable=False)
    most_popular_staff = db.Column(db.String(10), nullable=False)