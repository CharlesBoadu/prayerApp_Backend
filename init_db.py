import os
import psycopg2

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')


try:
    conn = psycopg2.connect(
        host="localhost",
        database="prayer_app",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    print(conn.get_dsn_parameters(), "\n")

    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    # Execute a command: this creates a new table
    cur.execute('DROP TABLE IF EXISTS users;')
    cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                'first_name varchar (50) NOT NULL,'
                                'last_name varchar (50) NOT NULL,'
                                'email varchar (50) NOT NULL,'
                                'age int NOT NULL,'
                                'phone CHAR (10) NOT NULL,'
                                'password VARCHAR (100) NOT NULL);'
                                )

#      # Insert data into the table

    cur.execute('INSERT INTO users (first_name, last_name, email, age, phone, password)'
                'VALUES (%s, %s, %s, %s, %s, %s)',
                ('Charles',
                 'Boadu',
                'cobdoc32@gmail.com',
                24,
                '0555105055',
                '$2b$05$hCERMsKPsbiVqnMfKzhmJuJQsZ4OMj.BEbQr9dL0qZbnwZp9e3X1a')
                )


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