class AirBnBListing:
    def __init__(self, request_body):
        self._id = get_value(request_body, "_id")
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


required_fields = [
    "listing_url",
    "name",
    "price",
    "property_type",
    "room_type",
    "accommodates",
    "bedrooms",
    "beds",
    "bathrooms",
]

# valid_fields = [
#     "_id",
#     "listing_url",
#     "name",
#     "summary",
#     "space",
#     "description",
#     "neighborhood_overview",
#     "notes",
#     "transit",
#     "access",
#     "interaction",
#     "house_rules",
#     "property_type",
#     "room_type",
#     "bed_type",
#     "minimum_nights",
#     "maximum_nights",
#     "cancellation_policy",
#     "last_scraped",
#     "calendar_last_scraped",
#     "accommodates",
#     "bedrooms",
#     "beds",
#     "number_of_reviews",
#     "bathrooms",
#     "amenities",
#     "price",
#     "weekly_price",
#     "monthly_price",
#     "cleaning_fee",
#     "extra_people",
#     "guests_included",
#     "images",
#     "host",
#     "address",
#     "availability",
#     "review_scores",
#     "reviews",
# ]


def get_value(request_body, key):
    return request_body[key] if key in request_body else ""


def print_listing(listing):
    item = {}
    for key, val in vars(listing).items():
        item[key] = str(val)
    return item


def validate_listing(listing):
    for field in required_fields:
        if field not in vars(listing).keys():
            return False
    return True


# def validate_listing(request_body):
#     for required_field in Listing.get_required_fields():
#         if required_field not in request_body.keys():
#             return str(
#                 {
#                     "error": "request body does not contain "
#                     + required_field
#                     + ", a required field."
#                 }
#             )

#     for field in request_body.keys():
#         if field not in valid_fields:
#             return str(
#                 {
#                     "error": field
#                     + " is not a valid field. Valid fields include "
#                     + str(valid_fields)
#                 }
#             )
