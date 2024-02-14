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
    total_income = float(request.form['total_income'])
    highest_spend = float(request.form['highest_spend'])
    best_selling_item = request.form['best_selling_item']
    worst_selling_item = request.form['worst_selling_item']
    mvp_staff_member = request.form['mvp_staff_member']
    average_basket_spend = float(request.form['average_basket_spend'])

    new_weekly_data = WeeklyData(
        week=week,
        total_income=total_income,
        highest_spend=highest_spend,
        best_selling_item=best_selling_item,
        worst_selling_item=worst_selling_item,
        mvp_staff_member=mvp_staff_member,
        average_basket_spend=average_basket_spend
    )

    db.session.add(new_weekly_data)
    db.session.commit()

    return redirect(url_for('my_view.index'))