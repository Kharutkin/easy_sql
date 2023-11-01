import json
from random import randint
from connection_with_db import req_to_db


def main():
    with open("products.json", "r") as file:
        products = json.load(file)
    for product in products:
        price = str(randint(5000, 100000))
        req = f"INSERT INTO product (name, description, price) " \
              f"VALUES ('{product}', '{products[product][1]}', {price})"
        print(req)
        req_to_db(req)


if __name__ == '__main__':
    main()
