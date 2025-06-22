from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

# Earthquake model (already complete)
class Earthquake(db.Model, SerializerMixin):
    __tablename__ = "earthquakes"

    id = db.Column(db.Integer, primary_key=True)
    magnitude = db.Column(db.Float)
    location = db.Column(db.String)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>"

# New Customer model
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    reviews = db.relationship("Review", back_populates="customer", cascade="all, delete-orphan")
    items = association_proxy("reviews", "item")

    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"

# New Item model
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    reviews = db.relationship("Review", back_populates="item", cascade="all, delete-orphan")

    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, {self.price}>"

# Review model (already provided, slightly refined)
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship("Customer", back_populates="reviews")
    item = db.relationship("Item", back_populates="reviews")

    serialize_rules = ('-customer.reviews', '-item.reviews')

    def __repr__(self):
        return f"<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}>"
