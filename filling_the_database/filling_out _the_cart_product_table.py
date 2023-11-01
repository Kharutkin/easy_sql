from connection_with_db import req_to_db
from random import randint


def main():
    for i in range(200):
        random_customer_id = randint(286, 788)
        req = f"SELECT id FROM cart"
        cart_id = req_to_db(req)[randint(0, 199)][0]
        req = f"SELECT id FROM cart"
        product_id = req_to_db(req)[randint(0, 19)][0]
        req = f"INSERT INTO cart_product (cart_id, product_id) " \
              f"VALUES ('{cart_id}', '{product_id}')"
        req_to_db(req)


if __name__ == '__main__':
    main()
