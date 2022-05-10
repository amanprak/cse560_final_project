from connect_db import conn_create
import csv

file = open('webscrap_data/amazon.csv')

print(type(file))

csvreader = csv.reader(file)
header = []
header = next(csvreader)
print(header)

category = []
insert_val = []
count = 1
for row in csvreader:
    if (row[4] not in category) and row[4] != '':
        category.append(row[4])
        insert_val.append({
            "categoryid": count,
            "name": row[4]
        })
        count += 1

conn, cur = conn_create()
cur = conn.cursor()
cur.executemany(
    """INSERT INTO categories(categoryid, name) VALUES (%(categoryid)s, %(name)s)""", insert_val)
conn.commit()
conn.close()
