from stockx import db

class Shoe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img_small = db.Column(db.Text)
    img_large = db.Column(db.Text)

    def __repr__(self):
        return f"Shoe({self.brand}, {self.name}, {self.desc}, {self.price})"