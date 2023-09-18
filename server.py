import json
from flask import Flask, request
from bson import json_util
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
from utils import (
    AirBnBListing,
    validate_listing,
    get_id,
    required_fields,
    create_linear_regression,
)

app = Flask(__name__)
config = dotenv_values()

# Create a new client and connect to the server
client = MongoClient(config["uri"], server_api=ServerApi("1"))
db = client.sample_airbnb
listingsAndReviews = db.listingsAndReviews

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(e)
    exit(1)


@app.route("/listing/<id>/")
def get_listing(id):
    """
    Given an id of the AirBnB listing, return information about this listing.
    Will return an error message if the given id is not found in the dataset.

    Arguments:
    id - String - the id of the wanted listing

    Returns:
    json object that either holds the listing object or an error message
    """
    doc = listingsAndReviews.find_one({"_id": get_id(id)})
    if doc:
        return json.loads(json_util.dumps(doc))
    return {"error": {"message": f"document with id {id} could not be found"}}


@app.route("/listing/<id>/", methods=["DELETE"])
def delete_listing(id):
    """
    Given an id of the AirBnB listing, delete that specific listing.
    Will return an error message if the id is not found.

    Arguments:
    id - String - the id of the wanted listing

    Returns:
    json object that either holds the id of the deleted object or an error message
    """
    try:
        doc = listingsAndReviews.delete_one({"_id": get_id(id)})
        if doc.deleted_count == 0:
            return {"result": {"message": f"document with id {id} not recognized."}}
        return {"result": {"message": f"document with id {id} deleted."}}

    except Exception as error:
        return {"error": {"message": error}}


@app.route("/listing/", methods=["POST"])
def post_listing():
    """
    Given a request body with information about a potential listing, post a listing object to the database.
    Will return an error message if the request body does not include all the required fields to create a listing.

    Arguments:
    Request Body - A list of the required fields can be found in the utils.py file, under the 'required_fields' variable

    Returns:
    json object that either holds the posted listing object or an error message
    """
    try:
        item = AirBnBListing(request.form.to_dict())
        if validate_listing(item) and vars(item)["price"] != "":
            ret = listingsAndReviews.insert_one(vars(item))
            _id = ret.inserted_id
            return {
                "result": {
                    "message": f"document with id {_id} inserted.",
                    "data": get_listing(_id),
                }
            }
        return {
            "error": {
                "message": "request body does not have all the required fields to create an AirBnB listing.",
                "required_fields": str(required_fields),
            }
        }

    except Exception as error:
        return {"error": {"message": error}}


@app.route("/competitive-listing/", methods=["POST"])
def post_competitive_listing():
    """
    Given a request body with information about a potential listing, post a listing object to the database using a price matching algorithm to find the best price.
    Will return an error message if the request body does not include all the required fields to create a listing.

    Arguments:
    Request Body - A list of the required fields can be found in the utils.py file, under the 'required_fields' variable

    Returns:
    json object that either holds the posted listing object or an error message
    """
    try:
        raw_vals = request.form.to_dict()
        item = AirBnBListing(raw_vals)

        if validate_listing(item):
            # look for items that have all the following fields populated
            cursor = listingsAndReviews.find(
                {
                    "minimum_nights": {"$ne": ""},
                    "maximum_nights": {"$ne": ""},
                    "accommodates": {"$ne": ""},
                    "bathrooms": {"$ne": ""},
                    "bedrooms": {"$ne": ""},
                    "beds": {"$ne": ""},
                    "guests_involved": {"$ne": ""},
                    "extra_people": {"$ne": ""},
                    "price": {"$ne": ""},
                    "price": {"$ne": 0},
                    "cleaning_fee": {"$ne": ""},
                    "cleaning_fee": {"$ne": 0},
                    "address.country": {"$eq": raw_vals["country"]},
                },
                {
                    "accommodates": 1,
                    "bathrooms": 1,
                    "bedrooms": 1,
                    "beds": 1,
                    "minimum_nights": 1,
                    "guests_included": 1,
                    "extra_people": 1,
                    "price": 1,
                    "cleaning_fee": 1,
                    "amenities": 1,
                    "_id": 0,
                },
            )

            records = list(cursor)
            for record in records:
                # clean up the records for pandas dataframe transformation
                for k, v in record.items():
                    if k == "amenities":
                        record[k] = len(v)
                    elif k == "address":
                        record[k] = record[k]["country"]
                    else:
                        try:
                            record[k] = float(v.to_decimal())
                        except:
                            record[k] = float(v)

            intercept, feat_to_coef = create_linear_regression(records)

            # calculate price
            price = intercept
            for feat, coef in feat_to_coef.items():
                price += float(raw_vals[feat]) * coef
            item.price = round(price, 2)

            # insert the listing
            ret = listingsAndReviews.insert_one(vars(item))
            _id = ret.inserted_id

            message = (
                f'You suggested a price of ${str(round(float(raw_vals["price"]), 2))} for this listing. After comparing your listing with {len(records)} other listings in {raw_vals["country"]}, we believe your listing is better priced at ${str(item.price)}.'
                if "price" in raw_vals
                else f"The most competitive price for this listing is {str(item.price)}"
            )
            return {
                "result": {
                    "message": message,
                    "data": get_listing(_id),
                }
            }
        else:
            return {
                "error": {
                    "message": "request body does not have all the required fields to create an AirBnB listing.",
                    "required_fields": str(required_fields),
                }
            }

    except Exception as error:
        return {"error": {"message": error}}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=105)
