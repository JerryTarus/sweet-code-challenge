from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, validates
from datetime import datetime

db = SQLAlchemy()

class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow)
    sweets = relationship('Vendor_Sweets', back_populates='vendor')

    def __repr__(self):
        return f'<Vendor {self.name}>'

class Vendor_Sweets(db.Model):
    __tablename__ = 'vendor_sweets'

    id = Column(Integer, primary_key=True)
    price = Column(DECIMAL, nullable=False)
    sweets_id = Column(Integer, ForeignKey('sweets.id'), nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendor.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow)
    sweet = relationship('Sweet', back_populates='vendor')
    vendor = relationship('Vendor', back_populates='sweets')

    @validates('price')
    def validates_price(self, key, price):
        if not price:
            raise ValueError("Price cannot be blank")

        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be a negative number")

        return price

class Sweet(db.Model):
    __tablename__ = 'sweets'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, server_default=func.now(), onupdate=datetime.utcnow)
    vendor = relationship('Vendor_Sweets', back_populates='sweet')
