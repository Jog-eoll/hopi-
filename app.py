from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():  # put application's code herec
    return render_template("index.html")


@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/model')
def model():
    return render_template('model.html')
def model():
    datalist = []
    con = sqlite3.connect("model.db")
    cur = con.cursor()
    sql = "select * from model"
    data = cur.execute(sql)

    for item in data :
        datalist.append(item)
    cur.close()
    con.close()
    return render_template('model.html',models = datalist)
@app.route('/PDandPDDate')
def PDandPDDate():
    return render_template('PDandPDDate.html')
@app.route('/PriceandScore')
def PriceandScore():
    return render_template('PriceandScore.html')

@app.route('/team')
def team():
    return render_template('team.html')





if __name__ == '__main__':
    app.run()
