# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
# GET /earthquakes/int:id
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    if earthquake:
        body = {'id': earthquake.id,
                'magnitude': earthquake.magnitude,
                'location': earthquake.location,
                'year': earthquake.year}
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404
    
    return make_response(body, status)


# GET /earthquakes/magnitude/float:magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    quakes = []  # array to store a dictionary for each pet
    for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        quake_dict = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
            }
        quakes.append(quake_dict)
    body = {'count': len(quakes),
            'quakes': quakes
            }
    return make_response(body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
