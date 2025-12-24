async function getBooks() {
  const res = await fetch("http://localhost:3000/api/books", {
    cache: "no-store",
  });
  return res.json();
}

export default async function HomePage() {
  const books = await getBooks();

  return (
    <main style={{ padding: "20px" }}>
      <h1>Books Catalogue</h1>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "20px" }}>
        {books.map((book) => (
          <div key={book.id} style={{ border: "1px solid #ccc", padding: "10px" }}>
            <img src={book.image_url} alt={book.title} width="100%" />
            <h3>{book.title}</h3>
            <p><b>Category:</b> {book.category}</p>
            <p><b>Price:</b> £{book.price}</p>
            <p><b>Rating:</b> {book.rating}/5</p>
            <p><b>Status:</b> {book.availability}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
