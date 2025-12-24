
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT,
    category TEXT,
    price NUMERIC,
    availability TEXT,
    rating INTEGER,
    product_url TEXT,
    image_url TEXT,
    request_time REAL,
    parsing_time REAL,
    total_time REAL
);

SELECT COUNT(*) FROM books;

SELECT * FROM books LIMIT 5;

SELECT product_url, COUNT(*)
FROM books
GROUP BY product_url
HAVING COUNT(*) > 1;


DELETE FROM books
WHERE id NOT IN (
    SELECT MIN(id)
    FROM books
    GROUP BY product_url
);






