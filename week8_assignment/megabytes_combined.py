# import libraries
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
from io import StringIO

# read excel files
# df = pd.read_excel("monday_data.xlsx")
def analyze_sales(file_path):
    df = pd.read_excel(file_path)

    # get the day name from the file name
    day_name = file_path.split('_')[0].capitalize()

    # create a file to store the output for each day
    output_file_path = f"{day_name}_analysis.txt"
    
    # create a StringIO object to capture printed output
    output_buffer = StringIO()

    # redirect stdout to the StringIO object
    sys.stdout = output_buffer

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                         INFO                                #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # print info of the excel file
# df.info()

    # print a description of the excel file
# print(df.describe())

    # print first 5 rows
# print(df.head())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                         CLEANING                            #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # removes columns
    df = df.drop(columns=["Unnamed: 0", "Transaction ID", "Till ID"])

    # removes rows
    df = df.drop([0])

    if "sunday" in file:
        df = df.drop(df[df["Staff"] == 0].index)

    # removes duplicates
    df = df.drop_duplicates()

    # reset index 0 to x after you removed rows
    df = df.reset_index(drop=True)

    # manually update possible mistakes
    # df.at[21, "Cost"] = 7.00

    if "thursday" in file:
        df.at[21, "Cost"] = 7.00

    if "wednesday" in file:
        df["Payment Method"] = df["Payment Method"].str.capitalize()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                  TRANSACTION TYPE                           #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # counts all transaction types
    transaction_type = df["Transaction Type"].value_counts()
    transaction_type.index.name = None
    print("Payment Type:")
    print(transaction_type.to_string(name=False))
    print()

    # drop void and float check
    df = df.dropna(how="any")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                    PAYMENT METHOD                           #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # counts all payment methods
    payment_method = df["Payment Method"].value_counts()
    payment_method.index.name = None
    print("Sales by Payment Method:")
    print(payment_method.to_string(name=False))
    print()

    # highlight the most common payment method
    most_common_method = df["Payment Method"].mode().iloc[0]
    print(f"The most common payment method is: {most_common_method}")
    print()

    # highlight the least common payment method
    least_method = df["Payment Method"].value_counts()
    least_common_method = min(df["Payment Method"].unique(), key=df["Payment Method"].tolist().count)
    print(f"The least common payment method is: {least_common_method}")
    print()

    # number of items sold by each payment method
    items_sold_by_method = df.groupby("Payment Method")["Total Items"].sum().astype(int)
    items_sold_by_method.index.name = None
    print("Items sold by each payment method:")
    print(items_sold_by_method.to_string(name=False))
    print()

    # total cost made by each payment method
    cost_made_by_method = df.groupby("Payment Method")["Cost"].sum().reset_index()
    cost_made_by_method.index.name = None
    print("Total cost made by each payment method:")
    print(cost_made_by_method.to_string(index=False, header=False))
    print()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                         BASKET                              #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # convert a fake list into an actual list
    def remove_punctuation(basket):
        basket = str(basket)
        basket = basket.replace("[", "")
        basket = basket.replace("]", "")
        basket = basket.replace("'", "")
        return basket

    df["Basket"] = df["Basket"].apply(remove_punctuation)

    def split_basket(basket_str):
        elements = basket_str.split(",")
        stripped_elements = [e.strip() for e in elements]
        return stripped_elements

    df["Basket"] = df["Basket"].apply(split_basket)

    df = df.explode("Basket", ignore_index=False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                         ITEMS                               #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # average price of an item
    average_item_price = df["Cost"].sum() / df["Total Items"].sum()
    print(f"The average item price is: {average_item_price:.2f}")
    print()

    # sum all the items
    total_items = df["Total Items"].sum()
    print(f"The total items sold is: {total_items:.0f}")
    print()

    # the average items in one transaction
    average_items = df["Total Items"].mean()
    print(f"The average items in a basket is: {average_items:.0f}")
    print()

    # the maximum items in one transaction
    max_items = df["Total Items"].max()
    print(f"The maximum items in a basket is: {max_items:.0f}")
    print()

    # the minimum items in one transaction
    min_items = df["Total Items"].min()
    print(f"The minimum items in a basket is: {min_items:.0f}")
    print()

    # the most popular items of the items sold
    most_popular_item = df["Basket"].mode()[0]
    print(f"The most popular item sold is: {most_popular_item}")
    print()

    # the least popular items of the items sold
    item_counts = df["Basket"].value_counts()
    least_popular_item = min(df["Basket"].unique(), key=df["Basket"].tolist().count)
    print(f"The least popular item sold is: {least_popular_item}")
    print()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                         COST                                #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # sum all the cost
    total_cost = df["Cost"].sum()
    print(f"The total cost is: {total_cost:.2f}")
    print()

    # the average cost in one transaction
    average_cost = df["Cost"].mean()
    print(f"The average cost in a basket is: {average_cost:.2f}")
    print()

    # the maximum cost in one transaction
    max_cost = df["Cost"].max()
    print(f"The maximum cost in a basket is: {max_cost:.2f}")
    print()

    # the minimum cost in one transaction
    min_cost = df["Cost"].min()
    print(f"The minimum cost in a basket is: {min_cost:.2f}")
    print()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                         STAFF                               #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # counts all staff
    staff_sale = df["Staff"].value_counts()
    staff_sale.index.name = None
    print("Sales by Staff:")
    print(staff_sale.to_string(name=False))
    print()

    # highlight the most common staff member
    most_common_staff = df["Staff"].mode().iloc[0]
    print(f"The most common staff member is: {most_common_staff}")
    print()

    # highlight the least common staff member
    least_staff = df["Staff"].value_counts()
    least_common_staff = min(df["Staff"].unique(), key=df["Staff"].tolist().count)
    print(f"The least common staff member is: {least_common_staff}")
    print()

    # number of items sold by each staff member
    items_sold_by_staff = df.groupby("Staff")["Total Items"].sum().astype(int)
    items_sold_by_staff.index.name = None
    print("Items sold by each staff member:")
    print(items_sold_by_staff.to_string(name=False))
    print()

    # total cost made by each staff member
    cost_made_by_staff = df.groupby("Staff")["Cost"].sum().reset_index()
    cost_made_by_staff.index.name = None
    print("Total cost made by each staff member:")
    print(cost_made_by_staff.to_string(index=False, header=False))
    print()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         RETURNS                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # return the result
    # return (payment_method, most_common_method, least_common_method, items_sold_by_method, cost_made_by_method, average_item_price, total_items, average_items, max_items, min_items, most_popular_item, least_popular_item, total_cost, max_cost, min_cost, staff_sale, most_common_staff, least_common_staff, items_sold_by_staff, cost_made_by_staff)
    # return cost_made_by_method

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         ENDING                              #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # reset stdout to the original value
    sys.stdout = sys.__stdout__

    # write the captured output to the file
    with open(output_file_path, "w") as output_file:
        output_file.write(output_buffer.getvalue())

def day_of_week_sort_key(file_name):
    day_name = file_name.split('_')[0].capitalize()
    days_in_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days_in_week.index(day_name)

# list all files in the specified directory
directory = "datasets/"
files = [f for f in os.listdir(directory) if f.endswith(".xlsx")]

files.sort(key=day_of_week_sort_key)

# loop through each file and apply the analysis function
for file in files:
    file_path = os.path.join(directory, file)
    print(f"Analysis for {file}:")
    analyze_sales(file_path)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#          DAILY&WEEKLY COST MADE BY STAFF BAR CHART          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# loop through each file and accumulate daily costs made by staff
# daily_cost_made_by_staff = []

# for file in files:
#     file_path = os.path.join(directory, file)
#     print(f"Analysis for {file}:")
#     cost_made_by_staff = analyze_sales(file_path)
#     daily_cost_made_by_staff.append(cost_made_by_staff)

# daily_cost_made_by_staff_concat = pd.concat(daily_cost_made_by_staff)
# weekly_cost_made_by_staff = pd.concat(daily_cost_made_by_staff).groupby("Staff")["Cost"].sum().reset_index()

# create subplots for the bar charts
# fig, axs = plt.subplots(2, 4, figsize=(15, 10))

# fig.suptitle("Daily and Weekly Costs Made by Staff", fontsize=16)

# colors = ['green' if x == weekly_cost_made_by_staff["Cost"].max() else ('red' if x == weekly_cost_made_by_staff["Cost"].min() else 'blue') for x in weekly_cost_made_by_staff["Cost"]]

# loop through the days and create bar charts
# for i, (file, cost_made_by_staff) in enumerate(zip(files, daily_cost_made_by_staff)):
#     axs[i // 4, i % 4].bar(cost_made_by_staff["Staff"].astype(str), cost_made_by_staff["Cost"], color='blue')
#     axs[i // 4, i % 4].set_title(f"{file.split('_')[0].capitalize()}")

# add the weekly chart to the empty subplot
# axs[-1, -1].bar(weekly_cost_made_by_staff["Staff"].astype(str), weekly_cost_made_by_staff["Cost"], color=colors)
# axs[-1, -1].set_title("Weekly")

# set the daily y-axis and x-axis properties
# max_daily_cost = daily_cost_made_by_staff_concat["Cost"].max()
# daily_y_axis_range = range(0, int(max_daily_cost) + 100, 100)

# for ax in axs.flatten():
#     ax.set_ylim([0, max_daily_cost])
#     ax.set_yticks(daily_y_axis_range)

# set the weekly y-axis and x-axis properties
# max_weekly_cost = weekly_cost_made_by_staff["Cost"].max()
# weekly_y_axis_range = range(0, int(max_weekly_cost) + 100, 200)

# axs[-1, -1].set_ylim([0, max_weekly_cost])
# axs[-1, -1].set_yticks(weekly_y_axis_range)

# Save the figure to a file
# plt.savefig("Daily_Weekly_Cost_Made_By_Staff_Bar_Chart.png", bbox_inches="tight")

# Show the bar charts
# plt.tight_layout()
# plt.show()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#          DAILY&WEEKLY COST MADE BY METHOD BAR CHART         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# loop through each file and accumulate daily costs made by staff
# daily_cost_made_by_method = []

# for file in files:
#     file_path = os.path.join(directory, file)
#     print(f"Analysis for {file}:")
#     cost_made_by_method = analyze_sales(file_path)
#     daily_cost_made_by_method.append(cost_made_by_method)

# daily_cost_made_by_method_concat = pd.concat(daily_cost_made_by_method)
# weekly_cost_made_by_method = pd.concat(daily_cost_made_by_method).groupby("Payment Method")["Cost"].sum().reset_index()

# create subplots for the bar charts
# fig, axs = plt.subplots(2, 4, figsize=(15, 10))

# fig.suptitle("Daily and Weekly Costs Made by Method", fontsize=16)

# colors = ['green' if x == weekly_cost_made_by_method["Cost"].max() else ('red' if x == weekly_cost_made_by_method["Cost"].min() else 'blue') for x in weekly_cost_made_by_method["Cost"]]

# loop through the days and create bar charts
# for i, (file, cost_made_by_method) in enumerate(zip(files, daily_cost_made_by_method)):
#     axs[i // 4, i % 4].bar(cost_made_by_method["Payment Method"].astype(str), cost_made_by_method["Cost"], color='blue')
#     axs[i // 4, i % 4].set_title(f"{file.split('_')[0].capitalize()}")

# add the weekly chart to the empty subplot
# axs[-1, -1].bar(weekly_cost_made_by_method["Payment Method"].astype(str), weekly_cost_made_by_method["Cost"], color=colors)
# axs[-1, -1].set_title("Weekly")

# set the daily y-axis and x-axis properties
# max_daily_cost = daily_cost_made_by_method_concat["Cost"].max()
# daily_y_axis_range = range(0, int(max_daily_cost) + 100, 100)

# for ax in axs.flatten():
#     ax.set_ylim([0, max_daily_cost])
#     ax.set_yticks(daily_y_axis_range)

# set the weekly y-axis and x-axis properties
# max_weekly_cost = weekly_cost_made_by_method["Cost"].max()
# weekly_y_axis_range = range(0, int(max_weekly_cost) + 100, 200)

# axs[-1, -1].set_ylim([0, max_weekly_cost])
# axs[-1, -1].set_yticks(weekly_y_axis_range)

# Save the figure to a file
# plt.savefig("Daily_Weekly_Cost_Made_By_Method_Bar_Chart.png", bbox_inches="tight")

# Show the bar charts
# plt.tight_layout()
# plt.show()