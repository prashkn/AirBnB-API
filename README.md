# AirBnB API

Take home assignment for PeopleWeave. REST API with simple database. Python, Flask, MongoDB.

This submission is also a public repository on my github: https://github.com/prashkn/AirBnB-API

## Running the server

Run `server.py` to run the server. **Please note that you will have to install all the imported libraries before you can run the server. This includes libraries such as flask, bson, pymongo, python-dotenv, certifi, pandas, matplotlib, and scikit-learn.**

From there, you can run the below endpoints using Postman or Insomnia with the base url `http://localhost:105/`. **Please note that you cannot use the Postman Web Version to make requests to your local host. You would need the Desktop Version to make requests to localhost, or configure the Web Version separately. It is recommended to have the Desktop version.**

If you want, I exported my requests on postman so you can easily test out the API for yourself. The json is in this repo, at `AirBnBPostmanRequests.json`.

## API Contract

### **GET** `/listing/{id}`

Given an `id`, return a single item.

### **DELETE** `/listing/{id}`

Given an `id`, delete and return a single item.

### **POST** `/listing`

Given a request body with parameters about the listing, create a listing. The required parameters for this endpoint are: _name, price, property_type, room_type, accommodates, bedrooms, beds, bathrooms, country, minimum_nights, guests_included, extra_people, amenities_

### **POST** `/competitive-listing`

Given a request body, create a linear regression equation, modeled off a subset of the dataset to find a competitive price for the given listing. The required paramaters for this endpoint are: _name, property_type, room_type, accommodates, bedrooms, beds, bathrooms, country, minimum_nights, guests_included, extra_people, amenities_
