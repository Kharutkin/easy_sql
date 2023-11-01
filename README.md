# easy_sql

Easy sql is a library for creating sql queries based on PostgreSQL
Currently a select query has been created
Future versions will add "insert into" and "view"

This library was written solely to develop my knowledge of sql queries.
Most likely, it will be easier and more useful for you to learn how to write sql queries yourself.

SELECT:

	This object is written to obtain information from a database

MAIN FUNCTIONS:

__init__:

	To initialize, enter in the select field the columns that you want to see in the finished table. Values ​​are accepted in string format.
	If you omit arguments, all possible columns will be printed.

	EXAMPLE 1:
	
		table = SELECT('id', 'name')
	
	If you need to apply an aggregate function to one of the columns you can do so here.
	There is a list of aggregate functions at the end of this file.
	
	EXAMPLE 2:
	
		table = SELECT('name', 'SUM(price)')
		
	If you need to use the as operator you can use it here.
		
	EXAPMLE 3:
	
		table = SELECT('name', 'SUM(product.price) as price')

lets_go:

	The function collects all the data entered for the request and makes a request to the database. 
	Does not accept arguments.
	Returns the result of an sql query or an error if the entered data is incorrect.

	EXAMPLE:

		table = Select('id', 'email', 'phone')
		table.from_tables('customer')
		sql_table = table.lets_go()
		for row in sql_table:
			print(row)
		
	RESULT:
	
		(286, 'Blinova@gmagle.com', '8 (177) 584-68-29')
		(287, 'Petrova@gmagle.com', '+74326045779')
		(288, 'Arturovich@gmagle.com', '+7 (577) 193-0124')
		(289, 'Rubenovna@gmagle.com', '89182294457')
		(290, 'Prohorova@gmagle.com', '8 330 283 6394')

OTHER FUNCTIONS:

from_tables:

	In this function, you specify the tables from which you need to get information.
	Do not use this function together with join!!!
	Arguments are accepted in string format.

	EXAMPLE:

		table.from_table('customer', 'cart)'

where:

	"where" is used to filter ROWs. Do not use this function for columns where grouping is used!!!
	To filter columns where grouping is applied, use having.
	The argument takes a column, a condition, and a value. These arguments add up to the sql condition
	
	ARGUMENTS:
		
		column: string
		condition: string
		value: integer
        
    EXAMPLE:
    
    	table.where(column='price' condition='>' value=1000)
    
        +-----------------+--------------------+----------------------------------------+
        |      python     |        SQL         |                easy_sql                |
        +-----------------+--------------------+----------------------------------------+
        | if price > 1000 | WHERE (price)>1000 | column='price' condition='>' value=1000|
        +-----------------+--------------------+----------------------------------------+

having:

	"having" is only used to sort GROUPs. 
    The aggregate function is retrieved from the selected columns. Do not use this function to filter rows!!!
    
    ARGUMENTS:
		
		column: string
		condition: string
		value: integer
		
    EXAMPLE:
    
    	table.having(column=price condition=">" value=1000)
    	
        +---------------------+-----------------------+---------------------------------------+
        |        python       |          SQL          |                easy_sql               |
        +---------------------+-----------------------+---------------------------------------+
        | if sum.price > 1000 | WHERE SUM(price)>1000 | column=price condition=">" value=1000 |
        +---------------------+-----------------------+---------------------------------------+

group_by:

	"group by" used for grouping by column
    WARNING If you are using grouping on a specific column,
    please note that all other columns must be formed by aggregate functions
    
    Example grouping:
    
		before grouping                         after grouping by coin
		+--------+-------+                      +--------+------------+
		|  coin  | price |                      |  coin  | SUM(price) |
		+--------+-------+                      +--------+------------+
		| coin 1 |  500  |                      | coin 1 |    1200    |
		| coin 1 |  700  |                      | coin 2 |    800     |
		| coin 2 |  800  |                      +--------+------------+
		+--------+-------+
        
    USE EXAMPLE:
    
    	table.group_by(name)

join:

	"Join" is used to join tables in sql.
	
	JOIN EXAMPLE:
	
		customer:			cart:					customer LEFT JOIN cart ON 
													customer.id=cart.customer.id
		+-------+----+		+-------------+----+	+-------+-------------+---------+
		|  name | id |		| customer_id | id |	|  name | customer.id | cart.id |
		+-------+----+		+-------------+----+	+-------+-------------+---------+
		|  Jhon | 0  |		|      0      | 0  |	|  Jhon |      0      |    0    |
		|  Mike | 1  |		|      1      | 1  |	|  Mike |      1      |    1    |
		| David | 2  |		|      1      | 2  |	|  Mike |      1      |    2    |
		+-------+----+		|      2      | 2  |	| David |      2      |    2    |
							+-------------+----+	+-------+-------------+---------+
		 				
	You can find more information about how join works and its types on the Internet.
	
	USE EXAMPLE:
	
		to join the tables described in the "join example" you need to use the following
		
		table.join('customer', 'id', 'LEFT JOIN', 'cart', 'customer_id')
		
		When filling out a function, rely on the equality of the corresponding fields, as in this case:
		customer.id=cart.customer.id
		
		You can use join multiple times.
		
	MORE INFORMATION:
		https://www.postgresql.org/docs/current/tutorial-join.html

limit:

	"Limit" is used to limit the number of lines output.
	An integer type number is accepted as an argument.
	
	EXAMPLE:
		
		table.limit(5)

AGGREGATE FUNCTIONS:
	
	AVG		the average (arithmetic mean) of all non-null input values
	COUNT	number of input rows for which the value of expression is not null
	MAX		maximum value of expression across all non-null input values
	MIN		minimum value of expression across all non-null input values
	SUM		sum of expression across all non-null input values
	
	More aggregate functions and information about them:
	https://www.postgresql.org/docs/9.5/functions-aggregate.html
