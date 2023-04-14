import csv

import requests
from faker import Faker
from flask import Flask, request, render_template

app = Flask(__name__)

lbs_to_kg = 0.45359237
inch_to_sm = 2.54


def get_requirements():
    with open('requirements.txt', 'r') as f:
        return f.read()


def generate_users(x):
    fake = Faker()
    users = []
    for i in range(x):
        users.append({fake.name(): fake.email()})
    return users


def get_mean():
    height = []
    weight = []
    with open('hw.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            height.append(float(row[' "Height(Inches)"']))
            weight.append(float(row[' "Weight(Pounds)"']))
    return round((sum(weight) / len(weight) * lbs_to_kg), 2), round((sum(height) / len(height) * inch_to_sm), 2)


@app.route("/requirements")
def show_requirements():
    return render_template('index.html', content=get_requirements())


@app.route("/users/generate")
def show_users():
    x = int(request.args.get('number', default=100))
    return render_template('index.html', content=generate_users(x))


@app.route("/mean")
def show_mean():
    return render_template('index.html',
                           content='Average height is {0} sm. Average weight is {1} kg'.format(get_mean()[0],
                                                                                               get_mean()[1]))


@app.route("/space")
def show_astronauts_num():
    r = requests.get('http://api.open-notify.org/astros.json')
    return render_template('index.html', content=f'Numer of astronauts: {r.json()["number"]}')
