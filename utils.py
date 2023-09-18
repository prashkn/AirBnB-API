from bson import ObjectId
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model


class AirBnBListing:
    def __init__(self, request_body):
        self.listing_url = get_value(request_body, "listing_url")
        self.name = get_value(request_body, "name")
        self.summary = get_value(request_body, "summary")
        self.space = get_value(request_body, "space")
        self.description = get_value(request_body, "description")
        self.neighborhood_overview = get_value(request_body, "neighborhood_overview")
        self.notes = get_value(request_body, "notes")
        self.transit = get_value(request_body, "transit")
        self.access = get_value(request_body, "access")
        self.interaction = get_value(request_body, "interaction")
        self.house_rules = get_value(request_body, "house_rules")
        self.property_type = get_value(request_body, "property_type")
        self.room_type = get_value(request_body, "room_type")
        self.bed_type = get_value(request_body, "bed_type")
        self.minimum_nights = get_value(request_body, "minimum_nights")
        self.maximum_nights = get_value(request_body, "maximum_nights")
        self.cancellation_policy = get_value(request_body, "cancellation_policy")
        self.last_scraped = get_value(request_body, "last_scraped")
        self.calendar_last_scraped = get_value(request_body, "calendar_last_scraped")
        self.accommodates = get_value(request_body, "accommodates")
        self.bedrooms = get_value(request_body, "bedrooms")
        self.beds = get_value(request_body, "beds")
        self.number_of_reviews = get_value(request_body, "number_of_reviews")
        self.bathrooms = get_value(request_body, "bathrooms")
        self.amenities = get_value(request_body, "amenities")
        self.price = get_value(request_body, "price")
        self.weekly_price = get_value(request_body, "weekly_price")
        self.monthly_price = get_value(request_body, "monthly_price")
        self.cleaning_fee = get_value(request_body, "cleaning_fee")
        self.guests_included = get_value(request_body, "guests_included")
        self.images = get_value(request_body, "images")
        self.host = get_value(request_body, "host")
        self.address = get_value(request_body, "address")
        self.availability = get_value(request_body, "availability")
        self.review_scores = get_value(request_body, "review_scores")
        self.reviews = get_value(request_body, "reviews")
        self.extra_people = get_value(request_body, "extra_people")
        self.address = {"country": get_value(request_body, "country")}


required_fields = [
    "name",
    "property_type",
    "room_type",
    "accommodates",
    "bedrooms",
    "beds",
    "bathrooms",
    "country",
    "minimum_nights",
    "guests_included",
    "extra_people",
    "amenities",
]


def get_value(request_body, key):
    if request_body is None or key not in request_body:
        return ""
    return request_body[key]


def validate_listing(listing):
    for field in required_fields:
        if field == "country":
            if vars(listing)["address"]["country"] == "":
                return False
        elif vars(listing)[field] == "":
            return False
    return True


def get_id(id):
    try:
        return ObjectId(id)
    except:
        return id


def create_linear_regression(documents):
    # convert list of dictionaries to a dataframe and replace any NaN with 0
    df = pd.DataFrame(documents).fillna(0)

    # replace "price" and "cleaning_fee" fields with a "total_price" field
    df["total_price"] = df["price"] + df["cleaning_fee"]
    df = df.drop(columns=["price", "cleaning_fee"], axis=1)

    # define the independent features
    x_cols = list(df.columns)
    x_cols.remove("total_price")

    # create linear regression model
    regr = linear_model.LinearRegression()
    regr.fit(df[x_cols], df["total_price"])

    # create a map between column name and coeff
    feat_to_coef = {}
    for feat, coef in zip(x_cols, regr.coef_):
        feat_to_coef[feat] = coef

    return regr.intercept_, feat_to_coef
