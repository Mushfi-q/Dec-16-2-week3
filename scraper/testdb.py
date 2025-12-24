import psycopg2
import json

with open("books.json", "r", encoding="utf-8") as f:
    books_data = json.load(f)

conn = psycopg2.connect(
    host="localhost",
    database="books_db",
    user="postgres",
    password="1234",
    port="5432"
)

cursor = conn.cursor()

insert_query = """
INSERT INTO books
(title, category, price, availability, rating,
 product_url, image_url, request_time, parsing_time, total_time)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

for book in books_data:
    cursor.execute(insert_query, (
        book["title"],
        book["category"],
        book["price"],
        book["availability"],
        book["rating"],
        book["product_url"],
        book["img"],
        book["request_time"],
        book["parsing_time"],
        book["total_time"]
    ))

conn.commit()
cursor.close()
conn.close()