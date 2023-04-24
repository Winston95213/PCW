from django.db import connection


class Global:
    def __init__(self):
        self.signIn = False


class Utiles:
    def __init__(self, response):
        self.response = response
        self.user_name = response["username"]
        self.first_name = response["firstname"]
        self.last_name = response["lastname"]
        self.email = response["email"]
        self.password = response["password"]

    def mysql(self):
        try:
            # Using connection to get a cursor and connect to the mysql connection
            cursor = connection.cursor()
            sqlInsert = f"INSERT INTO user_info(user_name, first_name, last_name, email, password) \
                  VALUES ('{self.user_name}', '{self.first_name}', '{self.last_name}', '{self.email}', '{self.password}')"
            print(sqlInsert)
            cursor.execute(sqlInsert)
            print("SQL Inserted Successfully")

        except Exception as e:
            print(f"Error: {e}")


# Verify the username and password,
# if the password is correct, then allow user to sign in it account
class Verify:
    def __init__(self, response):
        self.response = response
        self.user_name = response["username"]
        self.password = response["password"]

    def verify(self):
        try:
            # Using connection to get a cursor and connect to the mysql connection
            cursor = connection.cursor()
            sqlSelect = f"SELECT * FROM user_info WHERE user_name = '{self.user_name}' AND password = '{self.password}'"
            print(sqlSelect)
            cursor.execute(sqlSelect)
            # SQL Pass Through
            result = cursor.fetchall()
            print(result)
            if result:
                return True
            else:
                return False

        except Exception as e:
            print(f"Error: {e}")
