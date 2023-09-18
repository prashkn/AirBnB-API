# AirBnB API

Take home assignment for PeopleWeave. REST API with simple database. Python, Flask, MongoDB

## Running the server

Run `server.py` to run the server.

From there, you can run the below endpoints using Postman or Insomnia with the base url `http://localhost:105/`.

If you want, I exported my requests on postman so you can easily test out the API for yourself. The json is in this repo, at `AirBnBPostmanRequests.json`.

## API Contract

### **GET** `/listing/{id}`

Given an `id,` return a single item

### **DELETE** `/listing/{id}`

Given an `id`, delete and return a single item

### **POST** `/listing`

Given a request body with parameters about the listing, create a listing. The required parameters for this endpoint are: _name, price, property_type, room_type, accommodates, bedrooms, beds, bathrooms, country, minimum_nights, guests_included, extra_people, amenities_

### **POST** `/competitive-listing`

Given a request body, create a linear regression equation, modeled off a subset of the dataset to find a competitive price for the given listing. The required paramaters for this endpoint are: _name, property_type, room_type, accommodates, bedrooms, beds, bathrooms, country, minimum_nights, guests_included, extra_people, amenities_
