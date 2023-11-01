import json
from connection_with_db import req_to_db


def main():
    with open("products.json", "r") as file:
        products = json.load(file)
    for product in products:
        product_id = req_to_db(f"SELECT id, name FROM product WHERE name = '{product}';")
        print(product_id[0][1])
        req = f"INSERT INTO product_photo (url, product_id) " \
              f"VALUES ('{products[product][2][:255]}', '{product_id[0][0]}')"
        req_to_db(req)


if __name__ == '__main__':
    main()
