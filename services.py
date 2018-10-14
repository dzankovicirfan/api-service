# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests

api_url = 'https://api-playground.revelup.com'
API_key = '6c39370b27d0414ea095b47005b09309'
API_secret = '4a1fb827c4954c8bb2b56d74cb085f8dfe4ea12a6cf24297824c68f3d0d843bc'


class User(object):
    '''
    Class user for defining user with api keys
    '''
    header = None

    def __init__(self, api_key, api_secret):
        authorization = '%s:%s' % (api_key, api_secret)
        self.header = {
            'Content-type': 'application/json',
            'API-AUTHENTICATION': authorization
        }


# initializing user
user = User(API_key, API_secret)


# get menu
def order_menu(establishment):
    order_menu = requests.get(
        "%s/weborders/menu/?establishment=%s" % (api_url, establishment),
        headers=user.header
    )
    order_menu = json.loads(order_menu.content)
    return order_menu


# get categories
def category(establishment):
    product_category = requests.get(
        "%s/weborders/product_categories/?establishment=%s" % (api_url, establishment),
        headers=user.header
    )
    product_category = json.loads(product_category.content)
    return product_category


# find category
def find_category(product_category, name, id):
    for category in product_category['data']:
        find_category = category if (category['name'] == name and category['id'] == id) else None
        if find_category:
            break
    return find_category


# get products
def products(establishment):
    products = requests.get(
        "%s/weborders/products/?establishment=%s" % (api_url, establishment),
        headers=user.header
    )
    products = json.loads(products.content)
    return products


# finding product with name and id
def find_product(products, name, id):
    for product in products['data']:
        find_product = product if (product['name'] == name and product['id'] == id) else None
        if find_product:
            return find_product


def calculate(data):
    try:
        calculate = requests.post(
            "%s/specialresources/cart/calculate/" % api_url,
            data=json.dumps(data),
            headers=user.header
        )
        response = json.loads(calculate.content)
        final_total = response['data']['final_total']
    except requests.exceptions.ConnectionError:
        print("Connection refused")
    return final_total or None


# first chose restaurant to get menu
establisment = 2
category_name = "Dinner"
category_id = 72
product_name = "Red Sparkling"
product_id = 274

order_menu = order_menu(establisment)
category = category(establisment)

# now we chose category and category id
find_category = find_category(category, category_name, category_id)

# now we get products, and find product that we want
products = products(establisment)
find_product = find_product(products, product_name, product_id)


data = {
  "establishmentId": 2,
  "items": [
    {
      "modifieritems": [],
      "price": find_product['price'],
      "product": product_id,
      "product_name_override": find_product['name'],
      "quantity": 1,
      "special_request": ""
    }
  ],
  "orderInfo": {
    "dining_option": 0
  }
}

# calculate final_total and print it
calculate = calculate(data)
print(calculate)
