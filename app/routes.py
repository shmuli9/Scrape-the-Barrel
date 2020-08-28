from flask import Blueprint, jsonify, render_template

from app.models import Auction
from app.scrape import get_auctions, search_for_bottle

app = Blueprint('app', __name__, url_prefix="/")


@app.route('/')
def index():
    return jsonify('Hello World!')


@app.route("/bottle/<bottle>")
def bottle_search(bottle=None):
    if bottle is not None:
        search_for_bottle(bottle)
    else:
        return jsonify("Please submit a bottle to search for"), 401

    # listings = [
    #     {
    #         listing.
    #     } for listing in Listing.query.all()
    # ]

    return jsonify()


@app.route("/charts")
def charts():
    return render_template("charts.html", data={})


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

    # return jsonify(auctions), 200
    return render_template("auctions.html", auctions=auctions)
