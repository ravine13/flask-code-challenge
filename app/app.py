#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Hero,Power,Hero_power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db,render_as_batch=True)

db.init_app(app)

@app.route('/')
def home():
    return ''


if __name__ == '__main__':
    app.run(port=5555)
