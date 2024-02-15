from flask import Blueprint, redirect, render_template, url_for, request, jsonify
from .models import WeeklyData, db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import defaultdict

my_view = Blueprint("my_view", __name__)


@my_view.route('/')
def index():
    weekly_data = WeeklyData.query.all()
    generate_weekly_income_chart(weekly_data)
    return render_template('webapp.html', weekly_data=weekly_data)

def generate_weekly_income_chart(weekly_data):
    weeks = [data.day for data in weekly_data]
    total_cost = [data.total_cost for data in weekly_data]

    plt.bar(weeks, total_cost, color='skyblue')
    plt.xlabel('Week')
    plt.ylabel('Total Cost')
    plt.title('Weekly Total Cost')

    plt.savefig("website/static/mainplot.png", format='png')

@my_view.route('/weekly_data', methods=['POST'])
def submit_weekly_data():
    day = request.form['day']
    total_items = float(request.form['total_items'])
    most_popular_item = request.form['most_popular_item']
    least_popular_item = request.form['least_popular_item']
    total_cost = float(request.form['total_cost'])
    max_cost = float(request.form['max_cost'])
    min_cost = float(request.form['min_cost'])
    average_cost = float(request.form['average_cost'])
    least_popular_payment = request.form['least_popular_payment']
    most_popular_staff = request.form['most_popular_staff']

    new_weekly_data = WeeklyData(
    day = day,
    total_items = total_items,
    most_popular_item = most_popular_item,
    least_popular_item = least_popular_item,
    total_cost = total_cost,
    max_cost = max_cost,
    min_cost = min_cost,
    average_cost = average_cost,
    least_popular_payment = least_popular_payment,
    most_popular_staff = most_popular_staff
    )

    db.session.add(new_weekly_data)
    db.session.commit()

    weekly_data = WeeklyData.query.all()

    generate_weekly_income_chart(weekly_data)

    return redirect(url_for('my_view.index'))