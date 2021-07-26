import psycopg2
from decouple import config


def connecting():
    try:
        connection = psycopg2.connect(user=config('USER'),
                                      password=config('PASSWORD'),
                                      host=config('HOST'),
                                      port=config('PORT'),
                                      database=config('DATABASE'))
        return connection

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


def create_user():
    try:
        connection = connecting()

        cursor = connection.cursor()

        create_table_query = """CREATE TABLE Users (
                                EMAIL TEXT PRIMARY KEY,
                                USERNAME TEXT NOT NULL,
                                PASSWORD TEXT NOT NULL,
                                ID SERIAL)"""

        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL ")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        else:
            print("Error while connecting to PostgreSQL", error)

def insert_user(email, username,password):
    try:
        connection = connecting()

        cursor = connection.cursor()
        insert_table_query = """INSERT INTO Users(EMAIL,USERNAME,PASSWORD)
                                VALUES(%s,%s,%s)"""

        cursor.execute(insert_table_query, (email, username, password,))
        connection.commit()
        print("User inserted successfully in PostgreSQL ")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        else:
            print("Error while connecting to PostgreSQL", error)


def connection_teste():
    try:
        connection = connecting()

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        else:
            print("Error while connecting to PostgreSQL", error)


def get_user_db(email):
    try:
        connection = connecting()

        cursor = connection.cursor()
        select_user_query = """select * from Users where email = %s"""

        cursor.execute(select_user_query, (email,))
        users_data = cursor.fetchall()

        if not users_data:
            text = "User does not exist "
            email = []
            password = []

        else:
            text = "Login Ok"
            for row in users_data:
                email = row[0]
                username = row[1]
                password = row[2]
                id = row[3]

        return text, email, password

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed \n")
        else:
            print("Error while connecting to PostgreSQL", error)


if __name__ == '__main__':
    email = 'mairongallas@gmail.com'
    username = 'mairon'
    password = 'mairon'
    insert_user(email, username, password)