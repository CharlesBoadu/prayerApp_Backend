#Configurations for connecting to a database in elephantSQL
# import os
# import urllib.parse as up
# import psycopg2

# up.uses_netloc.append("postgres")
# url = up.urlparse(os.environ["postgres://janbgdhk:J8VKGaqgF2XuTMTNOLiF-q8GLOTq6usH@ruby.db.elephantsql.com/janbgdhk"])
# conn = psycopg2.connect(database=url.path[1:],
# user=url.janbgdhk,
# password=url.J8VKGaqgF2XuTMTNOLiF-q8GLOTq6usH,
# host=url.hostname,
# port=url.port
# )


#Configurations for connecting to a database using SQLite
# DATABASE_URI = 'sqlite:///app.db'
# DATABASE
# DATABASE = os.path.join(os.path.dirname(__file__), 'app.db')
