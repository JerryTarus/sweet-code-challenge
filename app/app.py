from flask import Flask, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from models import db, Vendor, Sweet, Vendor_Sweets
import os
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
ma = Marshmallow(app)
CORS(app)

# Initialize migrations
with app.app_context():
    db.create_all()

api = Api(app)

@app.route('/')
def home():
    return 'Aloha Crotonn Candy Family'

# I defined schemas here
class VendorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor

class SweetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sweet

class Vendor_SweetsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_Sweets
        fields = ("id", "price", "sweets_id", "vendor_id")

# Then instantiate schemas
vendor_schema = VendorSchema()
sweet_schema = SweetSchema()
vendorSweet_schema = Vendor_SweetsSchema()

# Defined request parser for POST requests here
post_args = reqparse.RequestParser(bundle_errors=True)
post_args.add_argument('price', type=float, help='Price of the sweet', required=True)
post_args.add_argument('sweets_id', type=int, help='ID of the associated sweet', required=True)
post_args.add_argument('vendor_id', type=int, help='ID of the associated vendor', required=True)

# This is the resource for retrieving all vendors
class Vendors(Resource):
    def get(self):
        vendors = Vendor.query.all()
        res = vendor_schema.dump(vendors, many=True)
        return make_response(jsonify(res), 200)

api.add_resource(Vendors, '/vendors')

# While this resource is for retrieving a specific vendor by ID
class VendorsByID(Resource):
    def get(self, id):
        vendor = Vendor.query.get(id)

        if vendor is None:
            return make_response(jsonify({"Error": "Vendor not found"}), 404)

        sweets = Sweet.query.join(Vendor_Sweets).filter_by(vendor_id=id).all()
        sweets_res = [sweet_schema.dump(sweet) for sweet in sweets]
        vendor_res = vendor_schema.dump(vendor)
        vendor_res["sweets"] = sweets_res

        return vendor_res

api.add_resource(VendorsByID, '/vendor/<int:id>')

# Halafu this resource is for retrieving all sweets
class Sweets(Resource):
    def get(self):
        sweets = Sweet.query.all()
        res = sweet_schema.dump(sweets, many=True)
        return make_response(jsonify(res), 200)

api.add_resource(Sweets, '/sweets')

# Then this is for retrieving a specific sweet by ID
class SweetByID(Resource):
    def get(self, id):
        sweet = Sweet.query.get(id)

        if sweet is None:
            return make_response(jsonify({"Error": "Sweet not found"}), 404)

        return make_response(jsonify(sweet_schema.dump(sweet)), 200)

api.add_resource(SweetByID, '/sweet/<int:id>')

# We delete a vendor sweet by ID
class VendorSweet(Resource):
    def delete(self, id):
        vendor_sweets = Vendor_Sweets.query.get(id)

        if vendor_sweets:
            db.session.delete(vendor_sweets)
            db.session.commit()
            return {"message": "VendorSweet deleted successfully"}

        return make_response(jsonify({"Error": "VendorSweet not found"}), 404)

api.add_resource(VendorSweet, '/vendor_sweets/<int:id>')

# This resource creates a new vendor sweet
class NewVendorSweet(Resource):
    def post(self):
        data = post_args.parse_args()

        sweet = Sweet.query.get(data["sweets_id"])
        vendor = Vendor.query.get(data["vendor_id"])

        if not (sweet and vendor):
            return make_response(jsonify({"errors": ["Validation errors"]}), 400)

        new_vendor_sweet = Vendor_Sweets(**data)
        db.session.add(new_vendor_sweet)
        db.session.commit()

        sweet_data = sweet_schema.dump(sweet)

        return make_response(jsonify(sweet_data), 201)

api.add_resource(NewVendorSweet, '/new_vendorsweets')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
