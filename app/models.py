from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

team = db.Table('team',
    db.Column("trainer_id", db.Integer, db.ForeignKey('user.id')),
    db.Column("pokemon_id", db.Integer, db.ForeignKey('pokemon.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    team = db.relationship('Pokemon', secondary=team, backref="owner", lazy="dynamic")
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    hp = db.Column(db.String, nullable=False)
    defense = db.Column(db.String, nullable=False)
    attack = db.Column(db.String, nullable=False)
    ability = db.Column(db.String, nullable=False)
    base_experience = db.Column(db.String, nullable=False)
    sprite = db.Column(db.String, nullable=False)
    team = db.relationship('Pokemon', secondary=team, backref="poke", lazy="dynamic")

    def __init__(self, name, hp, defense, attack, ability, base_experience, sprite):
        self.name = name
        self.hp = hp
        self.defense = defense
        self.attack = attack
        self.ability = ability
        self.base_experience = base_experience
        self.sprite = sprite

    def save(self):
        db.session.add(self)
        db.session.commit()