import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favourite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




# ENDPOINTS

# Creating an user
@app.route('/signup', methods=['POST'])
def signup():

    name = request.json.get("name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_query = User.query.filter_by(email = email).first()
    if user_query != None:
        return jsonify({"msg": "There is a user with that email"}), 401

    new_user = User(name = name, email = email, password = password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify("The user was added"), 200

# Get all users
@app.route('/users', methods=['GET'])
def get_all_user():
    users_query = User.query.all()
    users_data = list(map(lambda item: item.serialize(), users_query))
    response_body = {
        "msg": "ok",
        "users": users_data
    }

    return jsonify(response_body), 200


# RETRIEVING DATA FROM THE DATABASE


# Show me every character
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters_query = Character.query.all()
    characters_data = list(map(lambda item: item.serialize(), characters_query))
    response_body = {
        "msg": "ok",
        "result": characters_data
    }

    return jsonify(response_body), 200

# Show me ONE character
@app.route('/characters/<int:id>', methods=['GET'])
def character(id):
    character_query = Character.query.filter_by(id = id).first()
    character_data = character_query.serialize()
    response_body = {
        "msg": "ok",
        "result": character_data
    }

    return jsonify(response_body), 200

# Show me every planet
@app.route('/planets', methods=['GET'])
def get_all_planet():
    planet_query = Planet.query.all()
    planet_data = list(map(lambda item: item.serialize(), planet_query))
    response_body = {
        "msg": "ok",
        "result": planet_data
    }

    return jsonify(response_body), 200

# Show me ONE planet
@app.route('/planets/<int:id>', methods=['GET'])
def planet(id):
    planet_query = Planet.query.filter_by(id = id).first()
    planet_data = planet_query.serialize()
    response_body = {
        "msg": "ok",
        "result": planet_data
    }

    return jsonify(response_body), 200

# Show me every vehicle
@app.route('/vehicles', methods=['GET'])
def get_all_vehicle():
    vehicle_query = Vehicle.query.all()
    vehicle_data = list(map(lambda item: item.serialize(), vehicle_query))
    response_body = {
        "msg": "ok",
        "result": vehicle_data
    }

    return jsonify(response_body), 200

# Show me ONE vehicle
@app.route('/vehicles/<int:id>', methods=['GET'])
def vehicle(id):
    vehicle_query = Vehicle.query.filter_by(id = id).first()
    vehicle_data = vehicle_query.serialize()
    response_body = {
        "msg": "ok",
        "result": vehicle_data
    }

    return jsonify(response_body), 200




# ADDING DATA IN THE DATABASE


# Create a character
@app.route('/characters', methods=['POST'])
def add_character():
    name = request.json.get("name", None)
    description = request.json.get("description", None)
    character_query = Character.query.filter_by(name = name).first()
    if character_query != None:
        return jsonify({"msg": "There is a character with that name"}), 401

    new_character = Character(name = name, description = description)
    db.session.add(new_character)
    db.session.commit()
    return jsonify("Character added"), 200

# Create a planet
@app.route('/planets', methods=['POST'])
def add_planet():
    name = request.json.get("name", None)
    climate = request.json.get("climate", None)
    diameter = request.json.get("diameter", None)
    orbital_period = request.json.get("orbital_period", None)
    rotation_period = request.json.get("rotation_period", None)
    planet_query = Planet.query.filter_by(name = name).first()
    if planet_query != None:
        return jsonify({"msg": "There is a planet with that name"}), 401

    new_planet = Planet(name = name, climate = climate, diameter = diameter, orbital_period = orbital_period, rotation_period = rotation_period)
    db.session.add(new_planet)
    db.session.commit()
    return jsonify("Planet added"), 200

# Create a vehicle
@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    name = request.json.get("name", None)
    model = request.json.get("model", None)
    max_atmosphering_speed = request.json.get("max_atmosphering_speed", None)
    vehicle_query = Vehicle.query.filter_by(name = name).first()
    if vehicle_query != None:
        return jsonify({"msg": "There is a vehicle with that name"}), 401

    new_vehicle = Vehicle(name = name, model = model, max_atmosphering_speed = max_atmosphering_speed)
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify("Vehicle added"), 200




# HANDLING FAVOURITES


# Get the list of favorites of an user
@app.route("/user/<int:user_id>/favorites", methods=["GET"])

def get_all_favourites(user_id):
    user_query = User.query.filter_by(id = user_id).first()
    favourite_query = Favourite.query.filter_by(user_id = user_query.id).all()
    favourite_data = list(map(lambda item: item.serialize(), favourite_query))
    response_body = {
        "msg": "ok",
        "favourite": favourite_data
    }

    return jsonify(response_body), 200

# Create favorite character
@app.route('/user/<int:user_id>/favorites/characters/<int:character_id>', methods=['POST'])
def Create_one_favorite_character(user_id, character_id):
    url = request.json.get("url", None)
    user_query = User.query.filter_by(id = user_id).first()
    new_character_favourite = Favourite(user_id = user_query.id, url = url, character_id = character_id)
    db.session.add(new_character_favourite)
    db.session.commit()
    return jsonify("Favorite character added"), 200

# Create favorite planet
@app.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def Create_one_planet_favoutite(user_id, planet_id):
    url = request.json.get("url", None)
    user_query = User.query.filter_by(id = user_id).first()
    new_planet_favourite = Favourite(user_id = user_query.id, url = url, planet_id = planet_id)
    db.session.add(new_planet_favourite)
    db.session.commit()
    return jsonify("Favorite planet added"), 200

# Create favorite vehicle
@app.route('/user/<int:user_id>/favorites/vehicles/<int:vehicle_id>', methods=['POST'])
def Create_one_vehicle_favoutite(user_id, vehicle_id):
    url = request.json.get("url", None)
    user_query = User.query.filter_by(id = user_id).first()
    new_vehicle_favourite = Favourite(user_id = user_query.id, url = url, vehicle_id = vehicle_id)
    db.session.add(new_vehicle_favourite)
    db.session.commit()
    return jsonify("Favorite vehicle added"), 200

# Delete favorite character
@app.route('/user/<int:user_id>/favorites/characters/<int:character_id>', methods=['DELETE'])
def Delete_one_people_favoutite(user_id, character_id):
    user_query = User.query.filter_by(id = user_id).first()
    delete_character_favourite = Favourite.query.filter_by(user_id=user_query.id, character_id=character_id ).first()
    db.session.delete(delete_character_favourite)
    db.session.commit()
    return jsonify("Favorite character deleted"), 200

# Delete favorite planet
@app.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def Delete_one_planet_favoutite(user_id, planet_id):
    user_query = User.query.filter_by(id = user_id).first()
    delete_planet_favourite = Favourite.query.filter_by(user_id=user_query.id, planet_id=planet_id ).first()
    db.session.delete(delete_planet_favourite)
    db.session.commit()
    return jsonify("Favorite planet deleted"), 200

# Delete favorite vehicle
@app.route('/user/<int:user_id>/favorites/vehicles/<int:vehicle_id>', methods=['DELETE'])
def Delete_one_vehicle_favoutite(user_id, vehicle_id):
    user_query = User.query.filter_by(id = user_id).first()
    delete_vehicle_favourite = Favourite.query.filter_by(user_id=user_query.id, vehicle_id=vehicle_id ).first()
    db.session.delete(delete_vehicle_favourite)
    db.session.commit()
    return jsonify("Favorite vehicle deleted"), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
