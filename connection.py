import mysql.connector

CREATE_PRODUCTS = "CREATE TABLE products (GameId int (4) PRIMARY KEY NOT NULL, Gamename varchar (25) NOT NULL, Platform varchar (15), Price int (5), Genre varchar (30), Qty int(3));" 

CREATE_CUSTOMERS = "CREATE TABLE customers (Gamename varchar (25) NOT NULL, Cname varchar (25) NOT NULL, Qty int (3) NOT NULL);" 

class Connection(mysql.connector.connection.MySQLConnection):
    def __init__(self, host, username, password, **kwargs):
        super().__init__(host=host, user=username, password=password)

        self.crs = self.cursor(buffered=True)
    

    def create_database(self):
        # Checking if 'vectorgaming' database exists
        try:
            self.crs.execute('USE vectorgaming;')
        # if the database does not exist, create database
        except mysql.connector.errors.ProgrammingError:
            # If vectorgaming database does not exist
            self.crs.execute('CREATE DATABASE vectorgaming;')
            self.crs.execute('USE vectorgaming;')
            self.commit()


    def create_products(self):
        self.crs.execute(
            'SELECT COUNT(*) FROM information_schema.tables WHERE table_name = "products"')
        # If the table 'products' does not exist, create new table
        if self.crs.fetchone()[0] == 0:
            self.crs.execute(CREATE_PRODUCTS)
            self.commit()


    def create_customers(self):
        # To check if customers table exists
        self.crs.execute(
            'SELECT COUNT(*) FROM information_schema.tables WHERE table_name = "customers"')
        # If the table 'customers' does not exist, create new table
        if self.crs.fetchone()[0] == 0:
            self.crs.execute(CREATE_CUSTOMERS)
            self.commit()


    def get_product_names(self):
        self.crs.execute("SELECT Gamename FROM products;")
        returned_products = self.crs.fetchall()
        products = []
        for i in returned_products:
            products.append(i[0])
        return products


    def get_quantity(self, game_name):
            self.crs.execute(f'SELECT Qty FROM products WHERE Gamename = "{game_name}";')
            qty = 0
            for i in self.crs:
                qty = i[0]
            return qty

    def table_is_empty(self, table):
        """
        Check if the given table is empty or not
        :param table: table --- the table which is checked if empty or not
        :return: True if table is empty else return False
        """
        self.crs.execute("SELECT COUNT(*) FROM {table} + ;")
        table_count = None
        for i in self.crs:
            table_count = i[0]
        if table_count == 0:
            return True
        return False




































