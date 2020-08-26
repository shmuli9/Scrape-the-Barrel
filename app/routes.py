from flask import request, current_app, flash, redirect, url_for, render_template, Blueprint, jsonify

from app import db
from app.models import Auction

app = Blueprint('app', __name__, url_prefix="/")

@app.route('/')
def index():
    return jsonify('Hello World!')


@app.route("/bottle", methods=["GET", "POST"])
def search_for_bottle():
    return
