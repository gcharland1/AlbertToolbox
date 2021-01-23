from app import db

class base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class user(base):
    name = db.Column("name", db.String(128), nullable=False)
    email = db.Column("email", db.String(128), nullable=False, unique=True)
    password = db.Column("password", db.String(128), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)