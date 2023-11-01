from config import *


def update_config(data):
    global host, user, password, db_name
    data_list = data.split()
    list_len = len(data_list)
    update = []
    if list_len % 2:
        return 'Error, the config information is incorrect'
    for i in range(0, list_len, 2):
        match data_list[i]:
            case "host":
                host = data_list[i + 1]
                update.append('host')
            case "user":
                user = data_list[i + 1]
                update.append('user')
            case "password":
                password = data_list[i + 1]
                update.append('password')
            case "db_name":
                db_name = data_list[i + 1]
                update.append('db_name')

    if update:
        return f'Success!!!\nValues:{" ".join(update)} update in config'
    else:
        return 'OOps!!\nNo matches found for the main words'


print(host, user, password, db_name, '\nhost, user, password, db_name')
print(update_config(input("qwerty:")))
print(host, user, password, db_name, '\nhost, user, password, db_name')
