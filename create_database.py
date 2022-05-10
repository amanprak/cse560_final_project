import psycopg2
from connect_db import conn_create

conn, cur = conn_create()

try:
    cur.execute('''CREATE TABLE users
		(userId INTEGER PRIMARY KEY,
		password TEXT,
		email TEXT,
		firstName TEXT,
		lastName TEXT,
		address1 TEXT,
		address2 TEXT,
		zipcode TEXT,
		city TEXT,
		state TEXT,
		country TEXT,
		phone TEXT
		)''')

    cur.execute('''CREATE TABLE categories
			(categoryId INTEGER PRIMARY KEY,
			name TEXT
			)''')

    cur.execute('''CREATE TABLE products
			(productId INTEGER PRIMARY KEY,
			name TEXT,
			price TEXT,
			description TEXT,
			image TEXT,
			stock INTEGER,
			categoryId INTEGER,
			FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
			)''')

    cur.execute('''CREATE TABLE cart
			(userId INTEGER,
			productId INTEGER,
			FOREIGN KEY(userId) REFERENCES users(userId),
			FOREIGN KEY(productId) REFERENCES products(productId)
			)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS discount (
			discountid integer NOT NULL,
			description text NULL DEFAULT NULL,
			discountPercentage integer NULL DEFAULT NULL,
			PRIMARY KEY (discountid))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS orders (
			orderid integer NOT NULL,
			userid integer NULL DEFAULT NULL,
			productId integer NULL DEFAULT NULL,
			discountid integer NULL DEFAULT NULL,
			PRIMARY KEY (orderid),
				FOREIGN KEY (userid)
				REFERENCES users (userid)
				ON DELETE NO ACTION
				ON UPDATE NO ACTION,
				FOREIGN KEY (productId)
				REFERENCES products (productId)
				ON DELETE NO ACTION
				ON UPDATE NO ACTION,
				FOREIGN KEY (discountid)
				REFERENCES discount (discountid)
				ON DELETE NO ACTION
				ON UPDATE NO ACTION)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS support (
			supportid integer NOT NULL,
			userid integer NULL DEFAULT NULL,
			body TEXT NULL DEFAULT NULL,
			subject text NULL DEFAULT NULL,
			PRIMARY KEY (supportid),
				FOREIGN KEY (userid)
				REFERENCES users (userid)
				ON DELETE NO ACTION
				ON UPDATE NO ACTION)''')
    cur.close()
    conn.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print('Tables Created Successfully.')
        print('Database connection closed.')
