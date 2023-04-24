# import mysql.connector
# from mysql.connector import errorcode
# from sqlalchemy import create_engine

from .step import Step


class MySQL(Step):

    def __init__(self):
        super().__init__()

    def execute_database(self, cursor, cnx):
        try:
            cursor.execute("USE PCW_Database")
        except mysql.connector.Error as err:
            print("Database PCW_Database does not exists.")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(cursor)
                print("Database PCW_Database created successfully.")
                cnx.database = "PCW_Database"
            else:
                print(err)
                exit(1)

    def create_database(self, cursor):
        try:
            cursor.execute(
                "CREATE DATABASE PCW_Database DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def connect_database(self):
        try:
            cnx = mysql.connector.connect(user='root', host="127.0.0.1")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
        else:
            print("Successfully connected to the SQL Server")
            cursor = cnx.cursor(buffered=True)
            return cursor, cnx

    def create_table(self, website, cursor):
        TABLES = {}
        TABLES[website] = (
            f"""
        CREATE TABLE {website} (
            ID int AUTO_INCREMENT,
            name varchar(200) NOT NULL,
            price int(10) NOT NULL,
            link varchar(100) NOT NULL,
            picture varchar(100) NOT NULL,
            PRIMARY KEY (ID, name)
            ) ENGINE=InnoDB
            """
        )
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

    def save_data(self, data, inputs, cursor):
        for website in inputs["websites"]:
            print(f"Saving Data for {website}")
            self.create_table(website, cursor)
            add_product = (
                f"""
                                    INSERT IGNORE INTO {website}
                                    (name, price, link, picture)
                                    VALUES (%s, %s, %s, %s)
                            """
            )
            items = data[website].values.tolist()
            for item_info in items:
                name = item_info[0]
                price = item_info[1]
                link = item_info[2]
                picture = item_info[3]
                data_product = (name, price, link, picture)
                cursor.execute(add_product, data_product)


    def process(self, data, inputs, utils):
        cursor, cnx = self.connect_database()
        self.execute_database(cursor, cnx)
        self.save_data(data, inputs, cursor)
        # Make sure data is committed to the database
        cnx.commit()
        print('closing')
        cursor.execute("SELECT * FROM PchomeData")
        cursor.close()
        cnx.close()
        return data


