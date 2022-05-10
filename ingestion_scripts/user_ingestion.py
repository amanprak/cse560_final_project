from connect_db import conn_create
import csv
import random

conn, cur = conn_create()
cur = conn.cursor()

file = open('webscrap_data/user_merge.csv')

print(type(file))

csvreader = csv.reader(file)
header = []
header = next(csvreader)
print(header)

insert_val = []
count = 2
for row in csvreader:
    print(row)
    if count <= 501:
        country = "Australia"
    elif count >= 502 or count <= 1001:
        country = "Canada"
    elif count >= 502+500 or count <= 1001+500:
        country = "UK"
    elif count >= 502+500+500 or count <= 1001+500+500:
        country = "USA"

    if row[9] != '' and row[0] != '':
        insert_val.append({
            "userid": count,
            "password": '81dc9bdb52d04dc20036dbd8313ed055',
            "email": row[9],
            "firstName": row[0],
            "lastname": row[1],
            "address1": row[3],
            "address2": '',
            "city": row[4],
            "state": row[5],
            "country": country,
            "phone": row[7],
            "zipcode": str(random.randint(10000, 99999))
        })
        count += 1
print(insert_val)

cur.executemany(
    """INSERT INTO users(userid, password, email, firstName, lastname, address1, address2, city, state, country, phone, zipcode) VALUES (%(userid)s, %(password)s, %(email)s, %(firstName)s, %(lastname)s, %(address1)s, %(address2)s, %(city)s, %(state)s, %(country)s, %(phone)s, %(zipcode)s)""", insert_val)
conn.commit()
conn.close()
