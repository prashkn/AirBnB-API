# AirBnB API

Take home assignment for research position. REST API with simple database. Python, Flask, MongoDB

## API Contract

### **GET** `/listing`

Given an `id`, ..., return a single item or list of items that fit the filter.

### **GET** `/listing/{id}`

Given an `id,` return a single item

### **DELETE** `/listing/{id}`

Given an `id`, delete and return a single item

### **POST** `/listing`

Given a request body with parameters such as `bedrooms`, `bathrooms`, ..., create a listing.

### **POST** `/competitive-listing`

Given a request body without the `price` parameter, run an algorithm through a subset of the dataset to find a competitive price for this listing, given its other parameters such as `bedrooms`, `bathrooms`, `country`, etc.
