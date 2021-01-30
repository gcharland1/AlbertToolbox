from app import db, mail
import hashlib
import os
import random
import string

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class User(Base):
    name = db.Column("name", db.String(128), nullable=False)
    email = db.Column("email", db.String(128), nullable=False, unique=True)
    password = db.Column("password", db.String(128), nullable=False)
    salt = db.Column("salt", db.String(32), nullable=False)
    tmp_link = db.Column("tmp_link", db.String(255), nullable=False)

    def __init__(self, name, email, password, salt):
        self.name = name
        self.email = email
        self.password = password
        self.salt = salt
        self.tmp_link = ""

    def __repr__(self):
        return '<User %r>' % (self.name)

def hash_string(password, salt=None):
    if salt == None:
        salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    return key, salt

def get_random_string(length=32):
    character_pool = string.ascii_letters + string.digits
    return "".join(random.choice(character_pool) for _ in range(length))