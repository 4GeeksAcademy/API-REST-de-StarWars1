"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, FavoritePeople, FavoritePlanet

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


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    person = People.query.get(people_id)
    if person is None:
        raise APIException("Person not found", status_code=404)
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    if not user_id:
        raise APIException("user_id is required", status_code=400)
    
    favorite_people = FavoritePeople.query.filter_by(user_id=user_id).all()
    favorite_planets = FavoritePlanet.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        "favorite_people": [fav.serialize() for fav in favorite_people],
        "favorite_planets": [fav.serialize() for fav in favorite_planets]
    }), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    if not request.is_json:
        raise APIException("Request must be JSON", status_code=415)
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        raise APIException("user_id is required", status_code=400)
    
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    
    if FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first():
        raise APIException("Planet already in favorites", status_code=400)
    
    new_favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Planet added to favorites"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    if not request.is_json:
        raise APIException("Request must be JSON", status_code=415)
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        raise APIException("user_id is required", status_code=400)
    
    person = People.query.get(people_id)
    if person is None:
        raise APIException("Person not found", status_code=404)
    
    if FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first():
        raise APIException("Person already in favorites", status_code=400)
    
    new_favorite = FavoritePeople(user_id=user_id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Person added to favorites"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    if not request.is_json:
        raise APIException("Request must be JSON", status_code=415)
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        raise APIException("user_id is required", status_code=400)
    
    favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        raise APIException("Favorite planet not found", status_code=404)
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Planet removed from favorites"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    if not request.is_json:
        raise APIException("Request must be JSON", status_code=415)
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        raise APIException("user_id is required", status_code=400)
    
    favorite = FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not favorite:
        raise APIException("Favorite person not found", status_code=404)
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Person removed from favorites"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)