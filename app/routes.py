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
    if len(Auction.query.all()) == 0:
        get_auctions()

    if bottle is not None:
        search_for_bottle(bottle)
        return jsonify(f"Listings retrieved for {bottle}")
    else:
        return jsonify("Please submit a bottle to search for"), 401

    # listings = [
    #     {
    #         listing.
    #     } for listing in Listing.query.all()
    # ]



@app.route("/charts")
def charts():
    query_term = "No2"

    query = db.session.query(Listing.name,
                             func.round(func.avg(Listing.price), 2),
                             Auction.end_date).filter(Listing.sold).filter(
        Listing.auction_code == Auction.auction_code).filter(
        Listing.name.like("%No1")).group_by(Listing.name, Auction.name).order_by(Auction.end_date).all()

    data = [{
        "series": query[0].name,
        "dates": [listing[2].isoformat() for listing in query],
        "prices": [listing[1] for listing in query]
    }]

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
