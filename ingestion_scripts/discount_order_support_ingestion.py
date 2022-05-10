from connect_db import conn_create
import random

conn, cur = conn_create()
cur = conn.cursor()

count = 1
discount_insert_val = []
for i in range(1000):
    percent = random.randint(0, 100)
    discount_insert_val.append({
        "discountid": count,
        "description": f"Discount Name: Discount {count} Discount Percentage - {percent}",
        "discountpercentage": percent
    })
    count += 1


order_insert_val = []
count = 1
for i in range(50000*3):
    order_insert_val.append({
        "orderid": count,
        "userid": random.randint(1, 2001),
        "productId": random.randint(1, 9172),
        "discountid": random.randint(1, 1000) if(i % 7 == 0) else None
    })
    count += 1

count = 1
support_insert_val = []
for i in range(1000):
    support_insert_val.append({
        "supportid": count,
        "userid": random.randint(1, 2001),
        "body": f"Ticket Number-{random.randint(10000000, 90000000)}",
        "subject": f"Support Request Raised. Please contact the user"
    })
    count += 1


# cur.executemany(
#     """INSERT INTO discount(discountid, description, discountpercentage) VALUES (%(discountid)s, %(description)s, %(discountpercentage)s)""", discount_insert_val)
cur.executemany(
    """INSERT INTO orders(orderid, userid, productId, discountid) VALUES (%(orderid)s, %(userid)s, %(productId)s, %(discountid)s)""", order_insert_val)
# cur.executemany(
#     """INSERT INTO support(supportid, userid, body, subject) VALUES (%(supportid)s, %(userid)s, %(body)s, %(subject)s)""", support_insert_val)

conn.commit()
conn.close()
