from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)
    vendor_sweets = db.relationship('VendorSweet', backref='vendor', lazy=True)

# add any models you may need. 
    
class Sweet(db.Model):
    __tablename__ = 'sweet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)
    vendor_sweets = db.relationship('VendorSweet', backref='sweet', lazy=True)

class VendorSweet(db.Model):
    __tablename__ = 'vendor_sweets'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    sweets_id = db.Column(db.Integer, db.ForeignKey('sweet.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)

    @validates('price')
    def validate_price(self, key, value):
        if not value:
            raise ValueError('Price cannot be blank')
        if value < 0:
            raise ValueError('Price cannot be a negative number')
        return value



