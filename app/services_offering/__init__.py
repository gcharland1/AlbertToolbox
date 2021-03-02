from app import db

class Base(db.Model):
    __bind_key__ = 'clients'
    __abstract__ = True

    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Client(Base):
    contact_fname = db.Column("contact_fname", db.String(128), nullable=False)
    contact_name = db.Column("contact_name", db.String(128), nullable=False)
    company_name = db.Column("company_name", db.String(128), nullable=False)
    address = db.Column("address", db.String(256), nullable=False)
    city = db.Column("city", db.String(128), nullable=False)
    province = db.Column("province", db.String(128), nullable=False)
    zip = db.Column("zip", db.String(16), nullable=False)

    def __init__(self, contact_fname, contact_name, company_name, address, city, province, zip):
        self.contact_fname = contact_fname
        self.contact_name = contact_name
        self.company_name = company_name
        self.address = address
        self.city = city
        self.province = province
        self.zip = zip

    def __repr__(self):
        return self.company_name
