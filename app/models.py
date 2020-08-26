from datetime import datetime

from flask import current_app

from app import db


class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))

    price = db.Column(db.String(64))
    auction = db.Column(db.String(64))
    link = db.Column(db.String(512))
    auction_date = db.Column(db.DateTime())  # todo: change to relationship to Auctions

    scraped_date = db.Column(db.DateTime())
    site = db.Column(db.String(256))

    def __init__(self, id=None, name="", auction="", price="", auction_date="", site=""):
        self.id = id
        self.name = name

        self.price = price
        self.auction = auction
        self.site = site

        self.auction_date = auction_date
        self.scraped_date = datetime.now().replace(microsecond=0)

        current_app.logger.info(f"New Listing {self} added")

    def __repr__(self):
        return f'<Listing {self.name} - {self.lot} - {self.list_date}>'


class Auction(db.Model):
    __tablename__ = 'auctions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    end_date = db.Column(db.DateTime())

    auction_code = db.Column(db.String(64), index=True)

    number_of_lots = db.Column(db.String(64))
    link = db.Column(db.String(512))

    scraped_date = db.Column(db.DateTime())
    site = db.Column(db.String(256))

    def __init__(self, name, end_date, auction_code, num_lots, link, site):
        self.name = name
        self.end_date = end_date

        self.auction_code = auction_code
        self.number_of_lots = num_lots
        self.link = link

        self.site = site
        self.scraped_date = datetime.now().replace(microsecond=0)

        current_app.logger.info(f"New Auction {self} added")

    def __repr__(self):
        return f'<Auction {self.name}>'
