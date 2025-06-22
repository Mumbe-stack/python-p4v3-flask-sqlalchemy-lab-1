#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake  # and other models like Customer, Item, Review if defined

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Routes
@app.route('/')
def index():
    return make_response({'message': 'Flask SQLAlchemy Lab 1'}, 200)

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()
    if quake:
        return jsonify(quake.to_dict()), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        "count": len(quakes),
        "quakes": [quake.to_dict() for quake in quakes]
    }), 200

# Make app visible to Flask CLI
app = app  # ✅ critical

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    
