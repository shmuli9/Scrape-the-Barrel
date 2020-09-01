from flask import Blueprint, jsonify, render_template
from sqlalchemy.sql import func

from app.models import Auction, Listing, db
from app.scrape import get_auctions, search_for_bottle

app = Blueprint('app', __name__, url_prefix="/")


@app.route('/')
def index():
    return jsonify('Hello World!')


@app.route("/bottle/<bottle>")
def bottle_search(bottle=None):
    if Auction.query.first() is None:
        get_auctions()

    if bottle is not None:
        search_for_bottle(bottle)
        return jsonify(f"Listings retrieved for {bottle}")
    else:
        return jsonify("Please submit a bottle to search for"), 401


def query_for_bottle(query):
    return db.session.query(Listing.name,
                            func.round(func.avg(Listing.price), 2),
                            Auction.end_date) \
        .filter(Listing.sold) \
        .filter(Listing.auction_code == Auction.auction_code) \
        .filter(Listing.name.like(query)) \
        .group_by(Listing.name, Auction.name) \
        .order_by(Auction.end_date).all()


@app.route("/charts")
def charts():
    queries = [query_for_bottle("%No1"), query_for_bottle("%No1 75cl"),
               query_for_bottle("Macallan Edition No2"), query_for_bottle("Macallan Edition No3"),
               query_for_bottle("Macallan Edition No4"),
               query_for_bottle("Macallan Edition No5")]  # , query_for_bottle("%Genesis%")

    data = [
        {
            "series": query[0].name,
            "prices": [listing[1] for listing in query],
            "dates": [listing[2].isoformat() for listing in query]
        } for query in queries if len(query) > 0
    ]

    return render_template("charts.html", data=data)


@app.route("/auctions", methods=["GET"])
def list_auctions():
    if len(Auction.query.all()) == 0:
        get_auctions()

    auctions = [
        {
            "name": auction.name,
            "code": auction.auction_code,
            "end_date": auction.end_date,
            "link": auction.link
        } for auction in Auction.query.all()
    ]

    return render_template("auctions.html", auctions=auctions)
