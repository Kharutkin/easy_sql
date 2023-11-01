from connection_with_db import req_to_db
from faker import Faker
from transliterate import translit

fake = Faker('ru_RU')


def main():
    for i in range(1):
        name = fake.name()
        email = translit(name.split()[2], reversed=True).replace("'", '') + '@gmagle.com'
        phone = fake.phone_number()
        req = f"INSERT INTO customer(name, phone, email) VALUES ('{name}', '{phone}', '{email}')"
        req_to_db(req)
        print(f'success {i}')
        # print(translit(name, reversed=True), email)


if __name__ == '__main__':
    main()
