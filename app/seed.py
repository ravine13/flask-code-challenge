from models import db 
from models import Power, Hero, Hero_power
from app import app

def seed_data():
    powers = [

  { "name": "super strength", "description": "gives the wielder super-human strengths" },
  { "name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed" },
  { "name": "super human senses", "description": "allows the wielder to use her senses at a super-human level" },
  { "name": "elasticity", "description": "can stretch the human body to extreme lengths" }

]
    for power_info in powers:
        power = Power(**power_info)
        db.session.add(power)
        db.session.commit()


    heros_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    for heros_info in heros_data:
        hero =  Hero(**heros_info)
        db.session.add(hero)
        db.session.commit()


    strengths = ["Strong", "Weak", "Average"]

    for hero in Hero.query.all():
        for _ in range(3):
            power = Power.query.get(Power.query.order_by(db.func.random()).first().id)
            hero= Hero(hero_power=hero,power=power,strength=strengths.pop())

            db.session.add(Hero_power)
            db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_data()