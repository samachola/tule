from app import db

class Users(db.Model):
    """This class represents the Users Table."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(80))
    role = db.Column(db.String(80))
    password = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name, email, password, role):
        """Initialize with details."""
        self.name = name
        self.email = email
        self.role = role
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Users.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Users: {}>".format(self.name)


class Location(db.Model):
    """This class represents the locations table."""

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    county = db.Column(db.String(50))
    location = db.Column(db.String(50))

    def __init__(self, user_id, county, location):
        """Initialize Location details."""
        self.user_id = user_id
        self.county = county
        self.location = location

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Location: {}>".format(self.location)

class Restaurant(db.Model):
    """This class represents the Restaurant Table."""

    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(80))
    restaurant_email = db.Column(db.String(80))
    restaurant_county = db.Column(db.String(80))
    restaurant_location = db.Column(db.String(80))
    restaurant_minorder = db.Column(db.String(80))
    restaurant_phone = db.Column(db.String(80))
    restaurant_mobile = db.Column(db.String(80))
    restaurant_about = db.Column(db.String)
    restaurant_delivery = db.Column(db.String(80))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def __init__(self, restaurant_name, restaurant_email, restaurant_county, restaurant_location, restaurant_minorder, restaurant_phone, restaurant_mobile, restaurant_about, restaurant_delivery):
        """Initialize the restaurant model."""
        self.restaurant_name = restaurant_name
        self.restaurant_email = restaurant_email
        self.restaurant_county = restaurant_county
        self.restaurant_location = restaurant_location
        self.restaurant_minorder = restaurant_minorder
        self.restaurant_phone = restaurant_phone
        self.restaurant_mobile = restaurant_mobile
        self.restaurant_about = restaurant_about
        self.restaurant_delivery = restaurant_delivery

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Restaurant: {}>".format(self.restaurant_name)
