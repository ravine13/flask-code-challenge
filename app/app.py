#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
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

@app.route('/resources', methods=['GET'])
def get_resources():
    heroes = Hero.query.all()
    heroes_list = []
    for hero in heroes:
        heroes_list.append({**hero.to_dict()})

    powers = Power.query.all()
    powers_list = []

    for power in powers:
        powers_list.append({**power.to_dict()})

    response_data = {
            "heroes": heroes_list,
            "powers": powers_list
        }


    response = make_response(
            jsonify(response_data),
            200
        )
    return response


@app.route('/resource/<int:id>', methods=['GET', 'PATCH'])
def get_heroes_by_id(id):
    hero = Hero.query.filter_by(id=id).first()

    if hero:
        powers_list = [{**hp.powers.to_dict()} for hp in hero.hero_powers]

        response_data = {**hero.to_dict(), "powers": powers_list}

        return jsonify(response_data), 200
    else:
        response_data = {"error": "Hero not found"}
        response = make_response(jsonify(response_data), 404)
        return response
    
def get_powers_by_id(id):
    power = Power.query.filter_by(id=id).first()

    if power:
        response_data = power.to_dict()

        response = make_response(
            jsonify(response_data),
            200
        )

        return response
    else:
        response_data = {"error": "Power not found"}
        response = make_response(jsonify(response_data),
                                 
         404)
        return response

def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    if 'description' in data:
        power.description = data['description']
        db.session.commit()
        return jsonify(power.to_dict()), 200

    return jsonify({'error': 'No description provided'}), 400


@app.route('/hero_power',method= ['POST'])
def create_hero_power():
    data = request.get_json()


    if 'strength' not in data or 'power_id' not in data or 'hero_id' not in data:
        return jsonify({'errors': ['Missing required fields']}
                       
        ), 400

    power = Power.query.get(data['power_id'])
    hero = Hero.query.get(data['hero_id'])

    if power is None or hero is None:
        return jsonify({'errors': ['Power or Hero not found']}
        
        ), 404

    hero_power = Hero_power(strength=data['strength'], power_id=power.id, hero_id=hero.id)
    db.session.add(hero_power)
    db.session.commit()

    hero = Hero.query.get(data['hero_id'])
    powers_list = [{**hp.powers.to_dict()} for hp in hero.hero_powers]
    response_data = {**hero.to_dict(), "powers": powers_list}

    response = make_response(jsonify(
        response_data
    ),200)

    return response




if __name__ == '__main__':
    app.run(port=5555)
