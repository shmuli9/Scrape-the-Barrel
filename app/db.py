import datetime

from app.models import Auction, Listing, db
from app.scrape import get_auctions


def check_auctions():
    """
    Function to ensure that Auctions have been scraped

    :return:
    """
    auction = Auction.query.first()
    today = datetime.datetime.now()

    if auction is None or (auction.end_date.month < today.month or auction.end_date.year < today.year):
        get_auctions()


def query_for_bottle(query):
    """
    Query local DB for bottle
    :param query: search parameter - used in a LIKE to search the DB
    :return: Query object
    """
    return db.session.query(Listing.name,
                            func.round(func.avg(Listing.price), 2),
                            Auction.end_date) \
        .filter(Listing.sold) \
        .filter(Listing.auction_code == Auction.auction_code) \
        .filter(Listing.name.like(query)) \
        .group_by(Listing.name, Auction.name) \
        .order_by(Auction.end_date).all()


def all_bottles():
    """
    Returns a list of all diustinct bottles in local DB
    :return: Query object
    """
    return db.session.query(distinct(Listing.name)).order_by(func.length(Listing.name)).all()


def market_trends():
    """
    Returns average prices for all bottles and auctions in local DB
    Used to plot market trends of bottles scraped so far...
    :return: Query object
    """
    return db.session.query(func.round(func.avg(Listing.price), 2),
                            Auction.end_date) \
        .filter(Listing.sold) \
        .filter(Listing.auction_code == Auction.auction_code) \
        .group_by(Auction.name) \
        .order_by(Auction.end_date).all()
