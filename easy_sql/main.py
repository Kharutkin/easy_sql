from objects import *

from prettytable import PrettyTable

# sql_table = PrettyTable()

# a = Select('customer.name', 'SUM(price) as price')
# a.join('cart_product', 'product', 'LEFT', 'product_id', 'id')
# a.join('cart_product', 'cart', 'LEFT', 'cart_id', 'id')
# a.join('cart', 'customer', 'LEFT', 'customer_id', 'id')
# a.order_by('SUM(price)', 'DESC')
# a.group_by('customer.name')
# a.having('price', '>', '100000')
# print(a.create_req())
# table = a.lets_go()
# sql_table.field_names = a.column.split(', ')
# for row in table:
#     sql_table.add_row(row)
# # print(sql_table)
table = PrettyTable()
table.field_names = ['name', 'customer.id', 'cart.id']
table.add_row(['Jhon', 0, 0])
table.add_row(['Mike', 1, 1])
table.add_row(['Mike', 1, 2])
table.add_row(['David', 2, 2])
print(table)
