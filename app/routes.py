from flask import Blueprint, jsonify, render_template, request
from sqlalchemy.sql import func, distinct

from app.models import Auction, Listing, db
from app.scrape import get_auctions, search_for_bottle

app = Blueprint('app', __name__, url_prefix="/")


@app.route('/')
def index():
    return jsonify('Hello World!')


@app.route("/retrieve_bottle/<bottle>")
def retrieve_bottle(bottle=None):
    if Auction.query.first() is None:
        get_auctions()

    if bottle is not None:
        search_for_bottle(bottle)
        return jsonify(f"Listings retrieved for {bottle}")
    else:
        return jsonify("Please submit a bottle to search for"), 401


@app.route('/bottles', methods=['POST'])
def list_bottles():
    return render_template("", bottles=all_bottles())


def query_for_bottle(query):
    return db.session.query(Listing.name,
                            func.round(func.avg(Listing.price), 2),
                            Auction.end_date) \
        .filter(Listing.sold) \
        .filter(Listing.auction_code == Auction.auction_code) \
        .filter(Listing.name.like(query)) \
        .group_by(Listing.name, Auction.name) \
        .order_by(Auction.end_date).all()


def all_bottles():
    return db.session.query(distinct(Listing.name)).order_by(func.length(Listing.name)).all()


@app.route("/charts", methods=['GET', 'POST'])
def charts():
    if request.method == "POST":
        bottles = request.form.getlist("bottles[]")

        data = []
        for bottle in bottles:
            query = query_for_bottle(bottle)
            data.append(
                {
                    "series": query[0].name,
                    "prices": [listing[1] for listing in query],
                    "dates": [listing[2].isoformat() for listing in query]
                }
            )

        return jsonify(data)

    data = []

    return render_template("charts.html", data=data, all_bottles=all_bottles())


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
