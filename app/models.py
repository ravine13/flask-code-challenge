from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)
    powers = db.relationship('Hero_power', back_populates='hero') 

    def __repr__(self):
        return f'<hero {self.name}>'


class Hero_power(db.Model):  
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(255), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    powers_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)
    hero = db.relationship('Hero', back_populates='powers') 
    power = db.relationship('Power', back_populates='heroes')

    @validates('strength')
    def validates_hero_powers(self, key, strength):
        strength_list = ['Strong', 'Weak', 'Average']
        if not any(substring in strength for substring in strength_list):
            raise ValueError("Failed simple hero powers validation")
        return strength

class Power(db.Model): 
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)
    heroes = db.relationship('Hero_power', back_populates='power') 

    @validates('description')
    def validates_power(self, key, description):
        if len(description) < 20:
            raise ValueError("`description` must be present and at least 20 characters long")
        return description
