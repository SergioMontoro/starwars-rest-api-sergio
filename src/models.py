from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favourites = db.relationship('Favourite', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    url_img = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    favourites = db.relationship('Favourite', backref='character', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url_img": self.url_img,
            "description": self.description,
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    url_img = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    diameter = db.Column(db.String(250), nullable=True)
    orbital_period = db.Column(db.String(250), nullable=True)
    rotation_period = db.Column(db.String(250), nullable=True)
    favourites = db.relationship('Favourite', backref='planet', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url_img": self.url_img,
            "description": self.description,
            "climeate": self.climate,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
        }


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    url_img = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    model = db.Column(db.String(250), nullable=True)
    max_atmosphering_speed = db.Column(db.String(250), nullable=True)
    favourites = db.relationship('Favourite', backref='vehicle', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url_img": self.url_img,
            "description": self.description,
            "model": self.model,
            "max_atmospheting_speed": self.max_atmosphering_speed,
        }
    
class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(250), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)

    def __repr__(self):
        return '<Favourite %r>' % self.id

    def serialize(self):
        character = Character.query.filter_by(id = self.character_id).first()
        planet = Planet.query.filter_by(id = self.planet_id).first()
        vehicle = Vehicle.query.filter_by(id = self.vehicle_id).first()
        if self.character_id is not None:
            return {
            "id": self.id,
            "user_id": self.user_id,
            "url": self.url,
            "info": character.serialize(),
        }
        elif self.planet_id is not None:
            return {
            "id": self.id,
            "user_id": self.user_id,
            "url": self.url,
            "info": planet.serialize(),
        }
        else:
            return {
            "id": self.id,
            "user_id": self.user_id,
            "url": self.url,
            "info": vehicle.serialize(),
        }