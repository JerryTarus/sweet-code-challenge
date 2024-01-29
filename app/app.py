#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Vendor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'Welcome to Crotonn Pies'


# GET /vendors
@app.route('/vendors')
def get_vendors():
    vendors = Vendor.query.all()
    vendor_data = [{'id': vendor.id, 'name': vendor.name} for vendor in vendors]
    return jsonify(vendor_data)

# GET /vendors/:id
@app.route('/vendors/<int:vendor_id>')
def get_vendor(vendor_id):
    vendor = Vendor.query.get(vendor_id)
    if vendor:
        vendor_data = {'id': vendor.id, 'name': vendor.name, 'vendor_sweets': []}
        for vendor_sweet in vendor.vendor_sweets:
            sweet_data = {'id': vendor_sweet.sweet.id, 'name': vendor_sweet.sweet.name, 'price': vendor_sweet.price}
            vendor_data['vendor_sweets'].append(sweet_data)
        return jsonify(vendor_data)
    else:
        return jsonify({'error': 'Vendor not found'}), 404


# GET /sweets
@app.route('/sweets')
def get_sweets():
    sweets = Sweet.query.all()
    sweet_data = [{'id': sweet.id, 'name': sweet.name} for sweet in sweets]
    return jsonify(sweet_data)


# GET /sweets/:id
@app.route('/sweets/<int:sweet_id>')
def get_sweet(sweet_id):
    sweet = Sweet.query.get(sweet_id)
    if sweet:
        sweet_data = {'id': sweet.id, 'name': sweet.name}
        return jsonify(sweet_data)
    else:
        return jsonify({'error': 'Sweet not found'}), 404




if __name__ == '__main__':
    app.run(port=5555)
