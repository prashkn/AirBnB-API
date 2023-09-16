from flask import Flask, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
from utils import AirBnBListing, print_listing

app = Flask(__name__)
config = dotenv_values()

# Create a new client and connect to the server
client = MongoClient(config["uri"], server_api=ServerApi("1"))
db = client.sample_airbnb
listingsAndReviews = db.listingsAndReviews

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


@app.route("/listing/<id>/")
def get_listing(id):
    doc = listingsAndReviews.find_one({"_id": id})
    item = AirBnBListing(doc)
    print(item)
    if doc:
        return print_listing(item)
    return str({"error": "document with id " + id + " could not be found"})


@app.route("/listing/<id>/", methods=["DELETE"])
def delete_listing(id):
    doc = listingsAndReviews.delete_one({"_id": id})
    if doc.deleted_count >= 1:
        return str({"res": doc.deleted_count + " document(s) deleted"})
    return str({"error": "document with id " + id + " could not be deleted"})


@app.route("/listing/", methods=["POST"])
def post_listing():
    print(request.form.to_dict())
    try:
        item = AirBnBListing(request.form.to_dict())
        print("vars")
        print(vars(item))
        # ret = listingsAndReviews.insert_one(vars(item))
        # print(ret)
        return "ret"
    except Exception as error:
        print(error)
        return str({"error": "could not create listing given the request body"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=105)
