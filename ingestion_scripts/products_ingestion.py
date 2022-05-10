from connect_db import conn_create
import csv
import random


def category_id_fetcher(data, category):
    for i, item in enumerate(data):
        if category in item:
            # print('Index of 1 is [{}][{}]'.format(i, item.index(1)))
            return data[i][0]


conn, cur = conn_create()
cur = conn.cursor()

cur.execute('SELECT * FROM categories')
data = cur.fetchall()
print(data)
file = open('webscrap_data/amazon.csv')

print(type(file))

csvreader = csv.reader(file)
header = []
header = next(csvreader)
print(header)

insert_val = []
count = 1
for row in csvreader:
    if row[1] != '' and row[4] != '':
        insert_val.append({
            "productId": count,
            "name": row[1],
            "price": row[7].replace('$', '') if row[7] == '' else str(random.randint(1, 100)) + '.' + str(random.randint(10, 99)),
            "description": row[10] if row[10] != '' else "Product Description Yet To Be Updated By Seller.",
            "stock": row[8] if row[8] != '' else random.randint(0, 100),
            "image": row[15],
            "categoryid": category_id_fetcher(data, row[4])
        })
        count += 1
# print(insert_val)
# k = 100
# print('Product Name->', rows[k][1])
# print('Category->', rows[k][4])
# print('Selling Price->', rows[k][7])
# print('Quantity->', rows[k][8])
# print('Description->', rows[k][9])
# print('Image->', rows[k][15])


cur.executemany(
    """INSERT INTO products(productId, name, price, description, stock, image, categoryid) VALUES (%(productId)s, %(name)s, %(price)s, %(description)s, %(stock)s, %(image)s, %(categoryid)s)""", insert_val)
conn.commit()
conn.close()
