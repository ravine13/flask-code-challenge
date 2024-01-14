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

    hero_power_data = [
    {"strength": "Weak", "powers_id": 1, "hero_id": 1},
    {"strength": "Strong", "powers_id": 2, "hero_id": 2},
    {"strength": "Average", "powers_id": 3, "hero_id": 3},
    {"strength": "Strong", "powers_id": 4, "hero_id": 4},
    {"strength": "Weak", "powers_id": 1, "hero_id": 5},
    {"strength": "Average", "powers_id": 2, "hero_id": 6},
    {"strength": "Strong", "powers_id": 3, "hero_id": 7},
    {"strength": "Weak", "powers_id": 4, "hero_id": 8},
    {"strength": "Strong", "powers_id": 1, "hero_id": 9},
    {"strength": "Average", "powers_id": 2, "hero_id": 10},

    ]


    for hero_power in hero_power_data:
        new_hero_power = Hero_power(**hero_power)

        db.session.add(new_hero_power)
        db.session.commit()



if __name__ == '__main__':
    with app.app_context():
        seed_data()