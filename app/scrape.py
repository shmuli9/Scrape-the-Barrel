import datetime
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup as bs

from app import db
from app.models import Auction, Listing

BASE_URL = "https://www.scotchwhiskyauctions.com/"


def get_page(url):
    """
    Utility function to request pages
    Ensures that requested URL's are to the correct website

    :param url:
    :return:
    """
    if not url.startswith(BASE_URL):
        url = BASE_URL + url

    print(f"requesting url {url}")
    # cache[url] = requests.get(url).content
    content = requests.get(url).content
    print(f"content retrieved from {url}")
    return content


def search_for_bottle(term):
    """
    Queries SWA for the specified search term.
    If results are across multiple pages, it will query each page in turn

    Each soup (response object) is then parsed by parse_listings() and added to the DB

    :param term: query term to search for on SWA
    :return:
    """

    query = urlencode({"q": term})

    def create_url(query):
        per_page = urlencode({"perpage": 500})
        return f"https://www.scotchwhiskyauctions.com/auctions/search/?{query}&area=all&sort=mostrecent" \
               f"&order=asc&{per_page}"

    search_page = get_page(create_url(query))

    soup = bs(search_page, "html.parser")

    pages = soup.select(".pages > a:not(.curpage)")
    # pages are shown twice on each page so halve
    num_pages = int(len(pages) / 2)

    further_search_pages = []
    for i in range(2, num_pages + 2):
        page_query = urlencode({"page": i, "q": term})
        further_search_pages.append(create_url(page_query))

    parse_listings(soup)

    # go through remaining pages
    if len(further_search_pages) > 0:
        for url in further_search_pages:
            soup = bs(get_page(url), "html.parser")
            parse_listings(soup)

    db.session.commit()


def parse_listings(soup):
    """
    Parses listings from soup object
    Tailored to SWA search page

    If parsed data has changed "sold" status, then existing Listing is updated

    :param soup:
    :return:
    """
    boxes = soup.find_all("a", class_="prodbox")

    for prod in boxes:
        # title
        title = prod.find("span", class_="prodtitle").text.strip() if prod.find("span", class_="prodtitle") else ""

        # id - for use in db and analysis
        id_ = prod.find("span", class_="prodlot").text.strip() if prod.find("span", class_="prodlot") else ""
        id = id_[id_.find(": ") + 2:].replace("-", "")

        # auction
        auction_code = id[:id.find("-")] if id.find("-") != -1 else id[:3]
        auction = Auction.query.filter_by(auction_code=auction_code).first()

        # sold - defined by "Winning bid" text and lack of .reserve or .befirst
        sold = not (
                prod.find("span", class_="befirst")
                or prod.find("span", class_="reserve")
                or prod.find("span", class_="noreserve")
        ) and bool(prod.find("span", class_="price"))

        # price
        price = prod.find("span", class_="price").text.strip().replace("£", "") if sold else None

        link = BASE_URL + prod["href"]

        existing_listing = Listing.query.filter_by(id=id).first()
        if existing_listing is None:
            listing = Listing(id, title, auction, price, link, sold, "Scotch Whisky Auctions")
            db.session.add(listing)
        elif sold and not existing_listing.sold:
            # if existing entry wasnt sold, update sold status and price
            existing_listing.price = price
            existing_listing.sold = sold


def update_all():
    """
    Retrieves all bottles listed in "my bottles.txt" in the app folder, adding/updating the local DB

    :return:
    """
    for bottle in open("app/my bottles.txt", "r").read().split("\n"):
        if bottle:
            print(f"Retrieving {bottle}...")
            search_for_bottle(bottle)
            print(f"Retrieved {bottle} successfully")
    print("Update all task completed")


def get_auctions():
    """
    Get the auction details (basically just the end date actually)

    :return:
    """

    soup = bs(get_page("auctions/"), "html.parser")

    auctions = soup.find_all("a", class_="prodbox")

    for auct in auctions:
        name = auct.find("span", class_="cattitle").text if auct.find("span", class_="cattitle") else ""

        end_date_ = auct.find("span", class_="catdate").text.split("on ")[1]
        end_date = datetime.datetime.strptime(end_date_, "%B %d, %Y")

        num_lots_ = auct.find("span", class_="catproducts").text if auct.find("span", class_="catproducts") else ""
        num_lots = num_lots_[10:num_lots_.find(" lots in this auction.")]

        link = BASE_URL + auct["href"]

        auct_code = name[4:-10].zfill(3)

        auction = Auction(name, end_date, auct_code, num_lots, link, "Scotch Whisky Auctions")

        db.session.add(auction)
        print(f"{name} - {end_date} - {num_lots} - {link}")

    db.session.commit()
    print("Auctions added")
