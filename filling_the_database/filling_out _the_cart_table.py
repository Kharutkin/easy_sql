from connection_with_db import req_to_db
from random import randint


def main():
    for i in range(200):
        random_customer_id = randint(286, 788)
        req = f"INSERT INTO cart (customer_id) " \
              f"VALUES ('{random_customer_id}')"
        req_to_db(req)


if __name__ == '__main__':
    main()
