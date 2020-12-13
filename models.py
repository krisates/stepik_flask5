from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String)
    password = db.Column(db.String)
    orders = db.relationship("Order")

    def __repr__(self):
        return '<User {}>'.format(self.mail)


class Dish(db.Model):
    __tablename__ = "dish"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    picture = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category")

    def __repr__(self):
        return '<Dish {}>'.format(self.title)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    meals = db.relationship("Dish")

    def __repr__(self):
        return '<Category {}>'.format(self.title)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    price = db.Column(db.Float)
    status_id = db.Column(db.Integer)
    mail = db.Column(db.String)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    dishes = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")

    def __repr__(self):
        return '<Order {}>'.format(self.id)
