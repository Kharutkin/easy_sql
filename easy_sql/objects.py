import psycopg2
from config import *
from Aggregate_Functions import aggregate_functions


class Select:
    """
    This object is written to obtain information from a database.
    """

    def __init__(self, *args):
        self.column = ''
        if args:
            for col in args:
                if not isinstance(col, str):
                    raise ValueError('The arguments are the names of the columns of the '
                                     'future table entered in string format')
                self.column += f'{col}, '
            self.column = self.column[0: -2]
        else:
            self.column = '*'
        self.main_method = 'SELECT'
        self.__tables = ''
        self.__where_column = ''
        self.__where_condition = ''
        self.__where_value = ''
        self.__group_by_element = ''
        self.__having_func = ''
        self.__having_value = ''
        self.__having_condition = ''
        self.__having_column = ''
        self.__order_by_func = ''
        self.__order_by_element = ''
        self.__join_flag = False
        self.__tables_flag = True
        self.__join = []
        self.__limit = 0
        self._req = ''

    def lets_go(self):
        """
        This function applies the generated query to the database.
        Returns a list of tuples.
        Or error)))
        """
        self._req = self.__create_req()
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        try:
            with connection.cursor() as cursor:
                cursor.execute(self._req)
                return cursor.fetchall()

        except Exception as _ex:
            print('[INFO] Error while working PostgreSQL', _ex)

        finally:
            if connection:
                connection.close()

    def __create_req(self):
        """
        This function collects all applied data into a single request
        """
        match self.main_method:
            case "SELECT":
                self.__create_select_req()
            case "Insert_into":
                pass
            case "View":
                pass

        return self._req.strip()

    def from_tables(self, *args):
        """
        In this function, you specify the tables from which you need to get information.
        Do not use this function together with join!!!
        """
        assert isinstance(args[0], str)
        self.__tables = ''
        if len(args) > 1:
            self.__tables_flag = False
        for table in args:
            self.__tables += f'{table}, '
        self.__tables = self.__tables[0: -2]

    def where(self, column, condition, value):
        """
        "where" is used to filter ROWs
        """
        self.__where_column = column
        self.__where_condition = condition
        self.__where_value = str(value)
        self.__tables_flag = True

    def having(self, column, condition, value):
        """
        "having" is only used to sort GROUPs
        The function is retrieved from the selected columns
        """
        self.__having_column = column
        self.__having_condition = condition
        self.__having_value = value
        for col in self.column.split(', '):
            if self.__having_column in col:
                self.__having_func = col.split('(')[0]

    def order_by(self, element='', func='ASC'):
        """
        "order by" is used to sort rows by column
        ASC (default) Ascending
        DESC descending
        """
        self.__order_by_element = element
        self.__order_by_func = func

    def group_by(self, element):
        """
        "group by" used for grouping by column
        WARNING If you are using grouping on a specific column,
        please note that all other columns must be formed by aggregate functions
        Example
        before grouping                         after grouping by coin
        +--------+-------+                      +--------+------------+
        |  coin  | price |                      |  coin  | SUM(price) |
        +--------+-------+                      +--------+------------+
        | coin 1 |  500  |                      | coin 1 |    1200    |
        | coin 1 |  700  |                      | coin 2 |    800     |
        | coin 2 |  800  |                      +--------+------------+
        +--------+-------+
        """
        self.__group_by_element = element

    def join(self, table1, table2, species_of_join, column1, column2):
        self.__join.append({
            'column1': column1,
            'column2': column2,
            'table1': table1,
            'table2': table2,
            'species_of_join': species_of_join.upper() + ' JOIN'
        })
        self.__join_flag = True
        self.__tables_flag = True

    def limit(self, limit: int):
        self.__limit = limit

    def __create_select_req(self):
        if self.__tables_flag:
            assert ValueError('You can use two or more tables only with join or where')
        self._req = self.main_method
        self._req += ' '
        self._req += self.column
        self._req += ' FROM '
        self._req += self.__tables
        if self.__join_flag:
            count_of_join = len(self.__join)
            for join_number in range(count_of_join):
                if join_number == 0:
                    self._req += f"{self.__join[0]['table1']} {self.__join[0]['species_of_join']} " \
                                 f"{self.__join[0]['table2']} ON "
                    self._req += f"{self.__join[0]['table1']}.{self.__join[0]['column1']}=" \
                                 f"{self.__join[0]['table2']}.{self.__join[0]['column2']}"
                else:
                    self._req += f" {self.__join[join_number]['species_of_join']} " \
                                 f"{self.__join[join_number]['table2']} ON "
                    self._req += f"{self.__join[join_number]['table1']}.{self.__join[join_number]['column1']}=" \
                                 f"{self.__join[join_number]['table2']}.{self.__join[join_number]['column2']}"
        if self.__where_value and self.__where_column and self.__where_condition:
            self._req += f' WHERE ({self.__where_column}){self.__where_condition}{self.__where_value}'
        if self.__group_by_element:
            if aggregate_functions_in_column(self.column) == self.__group_by_element:
                self._req += f" GROUP BY {self.__group_by_element}"
            else:
                raise ValueError('you can use group by only if aggregate functions'
                                 ' are used in all columns not participating in the grouping')
        if self.__having_func and self.__having_value and self.__having_condition and self.__having_column:
            self._req += f" HAVING {self.__having_func}({self.__having_column}){self.__having_condition}" \
                         f"{self.__having_value}"
        if self.__order_by_func and self.__order_by_element:
            self._req += f" ORDER BY {self.__order_by_element} {self.__order_by_func}"
        if self.__limit:
            self._req += f" LIMIT {self.__limit}"
        self._req += ';'


def aggregate_functions_in_column(columns):
    columns = columns.split(', ')
    return_column = ''
    for column in columns:
        if not (column.split('(')[0].split(')')[0].upper() in aggregate_functions or
                column.split('(')[0].split(')')[0] in aggregate_functions):
            return_column += f'{column} '
    if return_column:
        return return_column.strip()
    else:
        return False

# class Insert_into:
#     def __init__(self, **kwargs):
#         super().__init__(main_method="INSERT INTO")
#         for arg in kwargs:
#             self.arg = kwargs[arg]
#
#
# class View:
#     def __init__(self, **kwargs):
#         super().__init__(main_method="VEIW")
#         for arg in kwargs:
#             self.arg = kwargs[arg]
