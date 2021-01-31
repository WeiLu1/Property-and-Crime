from flask import Flask, render_template, request, url_for
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
database = os.getenv('POSTGRES_DATABASE')
user = os.getenv('POSTGRES_USER')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')


def dbcursor():
    conn = psycopg2.connect(database=database, user=user, host=host, port=port)
    cursor = conn.cursor()
    return cursor


def get_properties(borough):
    db = dbcursor()
    db.execute("select numberbeds, price from propertiesaverage where borough like '{}' order by numberbeds asc;".format(borough))
    data = db.fetchall()
    db.close()
    return data


def get_crimes(borough):
    db = dbcursor()
    db.execute("select category, count(distinct(id)) from crimes where borough like '{}' group by category order by count(distinct(id)) desc;".format(borough))
    data = db.fetchall()
    db.close()
    return data


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        borough = request.form["dropdown"]
        print(borough)
        if not borough:
            return render_template("home.html")

        properties = get_properties(borough)
        crimes = get_crimes(borough)

        return render_template("home.html", borough=borough, properties=properties, crimes=crimes)
    else:
        return render_template("home.html")


@app.route("/compare")
def compare():
    return render_template("compare.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)




