from models import Vendor, Sweet, Vendor_Sweets
from app import app, db



def seed_data():
    vendor_names = [
        'Sweet Delights', 'Candy Corner', 'Sugar Rush', 'Tasty Treats', 'Delicious Delicacies',
        'Confectionery Castle', 'Dessert Den', 'Pastry Palace', 'Bakery Bazaar', 'Treat Tower'
    ]

    sweet_names = [
        'Chocolate Truffle', 'Vanilla Cupcake', 'Strawberry Tart', 'Blueberry Muffin', 
        'Raspberry Cheesecake', 'Lemon Loaf', 'Caramel Cookie', 'Pistachio Pastry', 
        'Almond Biscotti', 'Coconut Macaroon'
    ]


    # Refactored this code to use list comprehensions for instances

    vendors = [Vendor(name=name) for name in vendor_names]
    sweets = [Sweet(name=name) for name in sweet_names]

    db.session.add_all(vendors + sweets)
    db.session.commit()

    # Simplified this loop here with enumerate and zip
    vendor_sweets = [
        Vendor_Sweets(price=f'{i+1}.99', sweets_id=sweet.id, vendor_id=vendor.id)
        for i, (sweet, vendor) in enumerate(zip(sweets, vendors))
    ]

    db.session.add_all(vendor_sweets)
    db.session.commit()

    print("Seed data successfully updated.")

if __name__ == '__main__':
    with app.app_context():
        seed_data()
