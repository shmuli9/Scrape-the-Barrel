from datetime import datetime

from flask import current_app

from app import db


class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))

    price = db.Column(db.String(64))

    auction_code = db.Column(db.Integer, db.ForeignKey('auctions.auction_code'))
    auction = db.relationship('Auction', back_populates="listings")

    link = db.Column(db.String(512))
    lot = db.Column(db.String(64), index=True)

    sold = db.Column(db.Boolean())

    scraped_date = db.Column(db.DateTime())
    site = db.Column(db.String(256))

    def __init__(self, lot="", name="", auction="", price="", link="", sold=False, site=""):
        self.name = name
        self.lot = lot

        self.price = price
        self.auction = auction
        self.site = site

        self.link = link
        self.sold = sold

        # self.auction_date = auction_date
        self.scraped_date = datetime.now().replace(microsecond=0)

        # current_app.logger.info(f"New Listing {self} added")

    def __repr__(self):
        return f'<Listing {self.name} - {self.auction}>'


class Auction(db.Model):
    __tablename__ = 'auctions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    end_date = db.Column(db.DateTime())

    auction_code = db.Column(db.String(64), index=True, unique=True)

    number_of_lots = db.Column(db.String(64))
    link = db.Column(db.String(512))

    scraped_date = db.Column(db.DateTime())
    site = db.Column(db.String(256))

    listings = db.relationship("Listing", back_populates="auction")

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
