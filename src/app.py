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
from models import db, User, Character, Planet, Favorite
#from models import Person

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

#aqui vamos a escribir las rutas o endspoints

#USERS 

#lista de todos los users 
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all() 
    all_users_serialize = []
    for user in all_users:
        all_users_serialize.append(user.serialize())
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "data": all_users_serialize
    }

    return jsonify(response_body), 200

#ahora vamos a crear un enppoit que llame al usuario por su ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    single_user = User.query.get(user_id)
    if single_user is None:
        # la F hace que se interprete como una variable y no como un texto 
        return jsonify({ 'msg': f'It does not exist {user_id}'}), 404
    print(type(single_user))
    return jsonify({'msg': 'successful',
                    'data':single_user.serialize()}), 200



# aqui vamos a escribir un endpoit que resgistro a un usuario POST

@app.route('/sign_up', methods= ['POST'])
def add_single_user():
    request_body = request.json
    user_query = User.query.filter_by(email = request_body['email']).first()
    if user_query is None: 
        create_user = User( name = request_body['name'], email = request_body['email'], password = request_body['password'], is_active = request_body['is_active'] )
        db.session.add(create_user)
        db.session.commit()
        response_body = {
            'msg': 'successfully created ' 
        }
        return jsonify(response_body), 200
    else: 
        response_body = {
            'msg': 'user already exists ' 
        }
        return jsonify(response_body), 404
    


#Este endpoint devuelve la lista de favoritos del usuario 

@app.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    user_id = user_id
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    favorites = []
    for favorite in user.favorites:
        if favorite.character:
            favorites.append({"id": favorite.character.id, "name": favorite.character.name})
        elif favorite.planet:
            favorites.append({"id": favorite.planet.id, "name": favorite.planet.name})
    return jsonify(favorites)


#vamos a escribir una enppoint que elimine a un usuario 

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_single_user(user_id):
    user_delete = User.query.filter_by(id = user_id).first()
    if user_delete: 
        # user_delete.is_active = False (esto se escribe por si quiero pausar y no borrarlo)
        db.session.delete(user_delete)
        db.session.commit()
        response_body = {
            'msg': 'successfully deleted / paused '
        }
        return jsonify(response_body), 200
    else: 
        response_body = {
            'msg': 'user does not exists'
        }
        return jsonify(response_body), 404



#PERSONAJES 
# Este endpoint devuelve la información de un personaje específico según su ID

@app.route("/character/<int:character_id>", methods=["GET"])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    return jsonify({"id": character.id, "name": character.name})



#Este endpoint devuelve una lista de todos los personajes 
@app.route("/character", methods=["GET"])
def get_character():
    character = Character.query.all()
    return jsonify([{"id": character.id, "name": character.name} for character in character])




#Este endpoint agrega un nuevo personaje favorito al usuario actual

@app.route("/favorite/character/<int:character_id>", methods=["POST"])
def add_favorite_character(character_id):
    user_id = character_id
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "People not found"}), 404
    user.favorites.append(Favorite(user_id=user_id, character_id = character_id))
    db.session.commit()
    return jsonify({"message": "Favorite added"})






#este endpoint elimina un character favorito 
@app.route("/favorite/character/<int:character_id>", methods=["DELETE"])
def delete_favorite_character(character_id):
    user_id = character_id
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "character not found"}), 404
    favorite = Favorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if favorite is None:
        return jsonify({"error": "Favorite not found"}),  




#PLANETS


#Este endpoint devuelve una lista de todos los planetas

@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([{"id": planet.id, "name": planet.name} for planet in planets])



#Este endpoint devuelve la información de un planeta específico según su ID

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify({"id": planet.id, "name": planet.name})

#Este endpoint agrega un nuevo planeta favorito al usuario actual

@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    user_id = planet_id
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    user.favorites.append(Favorite(user_id=user_id, planet_id=planet_id))
    db.session.commit()
    return jsonify({"message": "Favorite added"})
   


    
#este endpoin elimina un planet favorito

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    user_id = planet_id
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id = planet_id).first()
    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"})


 
  


# this only runs if `$ python src/app.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
