from flask import Blueprint, redirect, render_template, url_for, request, jsonify
from .models import WeeklyData, db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

my_view = Blueprint("my_view", __name__)


@my_view.route('/')
def index():
    weekly_data = WeeklyData.query.all()
    generate_weekly_income_chart(weekly_data)
    return render_template('webapp.html', weekly_data=weekly_data)

def generate_weekly_income_chart(weekly_data):
    weeks = [data.week for data in weekly_data]
    total_income = [data.total_income for data in weekly_data]

    plt.bar(weeks, total_income, color='skyblue')
    plt.xlabel('Week')
    plt.ylabel('Total Income')
    plt.title('Weekly Total Income')

    plt.savefig("website/static/mainplot.png", format='png')

@my_view.route('/weekly_data', methods=['POST'])
def submit_weekly_data():
    week = request.form['week']
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
    week = week,
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


# @my_view.route('/')
# def index():
#     daily_data = DailyData.query.all()
#     generate_daily_income_chart(daily_data)
#     return render_template('webapp.html', daily_data=daily_data)

# def generate_daily_income_chart(daily_data):
#     days = [data.day for data in daily_data]
#     total_income = [data.total_income for data in daily_data]

#     plt.bar(days, total_income, color='skyblue')
#     plt.xlabel('Day')
#     plt.ylabel('Total Income')
#     plt.title('Daily Total Income')

#     plt.savefig("website/static/mainplot.png", format='png')

# @my_view.route('/daily_data', methods=['POST'])
# def submit_daily_data():
#     day = request.form['day']
#     total_items = float(request.form['total_items'])
#     most_popular_item = request.form['most_popular_item']
#     least_popular_item = request.form['least_popular_item']
#     total_cost = float(request.form['total_cost'])
#     max_cost = float(request.form['max_cost'])
#     min_cost = float(request.form['min_cost'])
#     average_cost = float(request.form['average_cost'])
#     least_popular_payment = request.form['least_popular_payment']
#     most_popular_staff = request.form['most_popular_staff']

#     new_daily_data = DailyData(
#     day = day,
#     total_items = total_items,
#     most_popular_item = most_popular_item,
#     least_popular_item = least_popular_item,
#     total_cost = total_cost,
#     max_cost = max_cost,
#     min_cost = min_cost,
#     average_cost = average_cost,
#     least_popular_payment = least_popular_payment,
#     most_popular_staff = most_popular_staff
#     )

#     db.session.add(new_daily_data)
#     db.session.commit()


    return redirect(url_for('my_view.index'))