#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api, Resource,reqparse
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import db, Hero,Power,Hero_power
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db,render_as_batch=True)
db.init_app(app)
api = Api(app)
ma = Marshmallow(app)
ma.init_app(app)

class HeroSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Hero
   

hero_schema = HeroSchema()


class PowerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Power
   

power_schema = PowerSchema()

class HeroPowerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Hero_power
        fields = ("id", "strength", "hero_id", "powers_id")

heropower_schema = HeroPowerSchema()

patch_args = reqparse.RequestParser(bundle_errors=True)
patch_args.add_argument('id', type=int,help='id of the Power')
patch_args.add_argument('name', type=str, help='Updated name of the Power')
patch_args.add_argument('description', type=str, help='Updated description of the Power')
patch_args.add_argument('hero_ids', type=int, action='append', help='List of Hero IDs to associate with the Power')


post_args = reqparse.RequestParser(bundle_errors=True)
post_args.add_argument('strength', type=str, help='Strength of the Hero_power', required=True)
post_args.add_argument('hero_id', type=int, help='ID of the associated Hero', required=True)
post_args.add_argument('powers_id', type=int, help='ID of the associated Power', required=True)

@app.route('/')
def home():
    return 'hello world'

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        print(heroes) 
        ravine =hero_schema.dump(heroes,many = True)
        print (ravine)
        
        response =  make_response(
            jsonify(ravine),
            200
        )
        return response
    
api.add_resource(Heroes, '/heros')

class HeroById(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        powers = Power.query.join(Hero_power).filter_by(hero_id=id).all()

        if hero is None:
            response = make_response(
                jsonify({"error": "Hero not found"}),
                404
            )
            return response
        else:
            powers_list = []
            for power in powers:
                powers_list.append({
                    "id": power.id,
                    "name": power.name,
                    "description": power.description
                })
            hero_dict = hero_schema.dump(hero)
            hero_dict["powers"] = powers_list

            return hero_dict




api.add_resource(HeroById, '/hero/<int:id>')
        
class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        POWER =power_schema.dump(powers,many = True)
        return make_response(
            jsonify(POWER),
            200
        )

api.add_resource(Powers, '/power')

class PowersByID(Resource):
     def get(self, id):
        powers = Power.query.filter_by(id=id).first()

        if powers is None:
            response = make_response(
                jsonify({"error": "power not found"}),
                404
            )
            return response
        else:
            raven = power_schema.dump(powers)


            return make_response(
                jsonify(raven),
                200
            )


     def patch(self,id):
        power = Power.query.get(id)

        if power is None:
            return (404, {"error": "Power not found"})


        data = patch_args.parse_args()
        if 'description' in data:
            power.description = data['description']
        else:
            return(400, {"errors": ["validation errors"]})

        db.session.commit()

        return make_response(
            jsonify(power_schema.dump(power)),
            200
        )

api.add_resource(PowersByID, '/power/<int:id>')

class HeroPowers(Resource):
    def post(self):
        data = post_args.parse_args()
        new_heropower = Hero_power(
            strength = data["strength"],
            hero_id = data["hero_id"],
            powers_id = data["powers_id"]
        )
        db.session.add(new_heropower)
        db.session.commit()

        raine = heropower_schema.dump(new_heropower)

        return make_response(
            jsonify(raine),
            201
        )

api.add_resource(HeroPowers, '/hero_powers')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
