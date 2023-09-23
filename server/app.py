#!/usr/bin/env python3


from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakeries_serialized), 200

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if bakery is None:
        return jsonify({"message": "Bakery not found"}), 404

    new_name = request.form.get("name")
    if new_name:
        bakery.name = new_name
        db.session.commit()
        return jsonify(bakery.to_dict()), 200
    else:
        return jsonify({"message": "Name field is required"}), 400

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    name = data.get("name")
    price = data.get("price")
    bakery_id = data.get("bakery_id")

    if not (name and price and bakery_id):
        return jsonify({"message": "All fields (name, price, bakery_id) are required"}), 400

    baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)
    db.session.add(baked_good)
    db.session.commit()
    return jsonify(baked_good.to_dict()), 201

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if baked_good is None:
        return jsonify({"message": "Baked Good not found"}), 404

    db.session.delete(baked_good)
    db.session.commit()
    return jsonify({"message": "Baked Good deleted successfully"}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
