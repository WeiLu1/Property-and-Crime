from flask import Flask, render_template, request, url_for
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.utils
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


def db_data(borough='', properties=False, crimes=False, all=False):
    conn = psycopg2.connect(database=database, user=user, host=host, port=port)
    cursor = conn.cursor()

    if all:
        cursor.execute(crime_all_query)
        data_crime = cursor.fetchall()
        cursor.execute(properties_all_query)
        data_property = cursor.fetchall()
        return data_crime, data_property

    if properties:
        cursor.execute(properties_query.format(borough))
    if crimes:
        cursor.execute(crime_query.format(borough))

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

        properties = db_data(borough=borough, properties=True)
        crimes = db_data(borough=borough, crimes=True)

        return render_template("home.html", borough=borough, properties=properties, crimes=crimes)
    else:
        return render_template("home.html")


@app.route("/compare")
def compare():
    if request.method == 'GET':
        crime, properties = db_data(all=True)

        properties_df = pd.DataFrame([[j for j in i] for i in properties])
        properties_df.rename(columns={0: 'Borough', 1: 'Number of beds', 2: 'Average price (£)'}, inplace=True)

        crime_df = pd.DataFrame([[j for j in i] for i in crime])
        crime_df.rename(columns={0: 'Borough', 1: 'Crime', 2: 'Count'}, inplace=True)

        line_property = px.line(properties_df, x="Number of beds", y="Average price (£)", color='Borough')
        line_property = line_property.update_traces(mode='markers+lines')

        bar_crime = px.bar(crime_df, x="Crime", y="Count", color='Borough')

        return render_template("compare.html", plot1=create_chart(line_property), plot2=create_chart(bar_crime))
    else:
        return render_template("compare.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)




