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






if __name__ == '__main__':
    app.run(port=5555)
