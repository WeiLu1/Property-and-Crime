from flask import Flask, render_template, request, url_for
import psycopg2
import plotly.express as px
import plotly.utils
from datetime import datetime
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
database = os.getenv('POSTGRES_DATABASE')
user = os.getenv('POSTGRES_USER')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')


crime_query = """
SELECT category, COUNT(DISTINCT(id)) FROM crimes WHERE borough LIKE '{}' GROUP BY category ORDER BY COUNT(DISTINCT(id)) DESC;
"""

properties_query = """
SELECT numberbeds, price FROM propertiesaverage WHERE borough LIKE '{}' ORDER BY numberbeds ASC;
"""

crime_all_query = """
SELECT borough, category, COUNT(DISTINCT(id)) FROM crimes GROUP BY borough, category ORDER BY borough ASC, category ASC;
"""

properties_all_query = """
SELECT borough, numberbeds, price FROM propertiesaverage ORDER BY borough ASC, numberbeds ASC;
"""

dates_query = """
SELECT DISTINCT(date) FROM crimes ORDER BY date DESC;
"""

crime_date_query = """
SELECT category, COUNT(DISTINCT(id)) FROM crimes WHERE borough LIKE '{}' AND date = '{}' GROUP BY category ORDER BY COUNT(DISTINCT(id)) DESC;
"""


def db_data(query):
    conn = psycopg2.connect(database=database, user=user, host=host, port=port)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data


def create_chart(fig):
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        borough = request.form["dropdown"]
        if not borough:
            return render_template("home.html")

        properties = db_data(properties_query.format(borough))
        crimes = db_data(crime_query.format(borough))

        return render_template("home.html", borough=borough, properties=properties, crimes=crimes)
    else:
        return render_template("home.html")


@app.route("/compare", methods=['GET'])
def compare():
    if request.method == 'GET':
        crime = db_data(crime_all_query)
        properties = db_data(properties_all_query)

        line_property = px.line(properties, x=[x[1] for x in properties], y=[x[2] for x in properties], color=[x[0] for x in properties])
        line_property = line_property.update_traces(mode='markers+lines')
        line_property.update_traces(hovertemplate='Number of bedrooms: %{x} <br>Average price (£): %{y}')
        line_property.update_layout(
            xaxis_title="Number of bedrooms",
            yaxis_title="Average price (£)",
            legend_title="Borough"
        )

        bar_crime = px.bar(crime, x=[x[1] for x in crime], y=[x[2] for x in crime], color=[x[0] for x in crime])
        bar_crime.update_traces(hovertemplate='Crime category: %{x} <br>Count: %{y}')
        bar_crime.update_layout(
            xaxis_title="Crime Category",
            yaxis_title="Count",
            legend_title="Borough"
        )

        return render_template("compare.html", plot1=create_chart(line_property), plot2=create_chart(bar_crime))
    else:
        return render_template("compare.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/crimes-by-month", methods=['GET', 'POST'])
def crime_selector():
    dates = [x[0] for x in db_data(dates_query)]

    if request.method == 'POST':
        borough = request.form['dropdownborough']
        if not borough:
            return render_template("crime_selector.html", dates=dates)

        specific_date = request.form['dropdowndate']
        crime_date_data = db_data(crime_date_query.format(borough, specific_date))
        return render_template("crime_selector.html", dates=dates, borough=borough, specificdate=specific_date, crimedatemonths=crime_date_data)

    return render_template("crime_selector.html", dates=dates)


if __name__ == "__main__":
    app.run(debug=True)




