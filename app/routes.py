from flask import Blueprint, jsonify, render_template, request

from app.db import *
from app.scrape import get_auctions, search_for_bottle, update_all
from app.thread import CThread

app = Blueprint('app', __name__, url_prefix="/")


@app.route('/')
def index():
    return jsonify('Hello World!')


@app.route("/retrieve_bottle/<bottle>")
def retrieve_bottle(bottle=None):
    """
    Scrapes an individual bottle from SWA
    :param bottle:
    :return:
    """
    check_auctions()

    if bottle is not None:
        search_for_bottle(bottle)
        return jsonify(f"Listings retrieved for {bottle}")
    else:
        return jsonify("Please submit a bottle to search for"), 401


@app.route("/retrieve_all/")
def retrieve_all():
    """
    Retrieves all bottles listed in "my bottles.txt" in the app folder

    Uses threading (CThread) to allow the flask app to continue while long running update task finishes
    """
    check_auctions()

    t_update_all = CThread(target=update_all)
    t_update_all.start()

    return jsonify("Update task started")


# @app.route('/bottles', methods=['POST'])
# def list_bottles():
#     return render_template("", bottles=all_bottles())


@app.route("/charts", methods=['GET', 'POST'])
def charts():
    if request.method == "POST":
        bottles = request.form.getlist("bottles[]")

        if "market" in bottles:
            query = market_trends()
            data = [{
                "series": "Market",
                "prices": [listing[0] for listing in query],
                "dates": [listing[1].isoformat() for listing in query]
            }]
            return jsonify(data)

        data = []
        for bottle in bottles:
            query = query_for_bottle(bottle)
            if len(query) > 0:
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
