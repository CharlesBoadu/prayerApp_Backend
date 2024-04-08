import os
import psycopg2
import bcrypt

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')


try:
    conn = psycopg2.connect(
        host="localhost",
        database="prayer_app",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    # Execute a command: this creates a new table called users
    cur.execute('DROP TABLE IF EXISTS users;')
    cur.execute('DROP TABLE IF EXISTS prayers;')
    cur.execute('DROP TABLE IF EXISTS favorite_prayers;')

    cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                'first_name varchar (50) NOT NULL,'
                                'last_name varchar (50) NOT NULL,'
                                'email varchar (50) NOT NULL,'
                                'age int NOT NULL,'
                                'phone CHAR (10) NOT NULL,'
                                'role varchar (50) NOT NULL,'
                                'password VARCHAR (1024) NOT NULL,'
                                'temp_password VARCHAR (1024));'
                                )
    cur.execute('CREATE TABLE prayers (id serial PRIMARY KEY,'
                                'prayer TEXT NOT NULL,'
                                'scripture TEXT NOT NULL,'
                                'user_id INT NOT NULL,'
                                'category varchar (50) NOT NULL,'
                                'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                )
    
    cur.execute('CREATE TABLE favorite_prayers (id serial PRIMARY KEY,'
                                'prayer TEXT NOT NULL,'
                                'scripture TEXT NOT NULL,'
                                'user_id INT NOT NULL,'
                                'category varchar (50) NOT NULL,'
                                'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                )

#      # Insert data into the table

    # cur.execute('INSERT INTO users (first_name, last_name, email, age, phone, password)'
    #             'VALUES (%s, %s, %s, %s, %s, %s)',
    #             ('Charles',
    #              'Boadu',
    #             'cobdoc32@gmail.com',
    #             24,
    #             '0555105055',
    #             "b'$2b$12$pAJ3J9OeEY3Fiuzj2qfI/OPqQ4zA9v80BNdJ8R6eR7apXjv3zjZIa'")
    #             )


#     cur.execute('INSERT INTO books (title, author, pages_num, review)'
#                 'VALUES (%s, %s, %s, %s)',
#                 ('Anna Karenina',
#                 'Leo Tolstoy',
#                 864,
#                 'Another great classic!')
#                 )

    conn.commit()
    cur.close()
    conn.close()
except Exception as e:
    print("Error:", e)