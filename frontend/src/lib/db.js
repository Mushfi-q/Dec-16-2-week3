import { Pool } from "pg";

const pool = new Pool({
  host: "localhost",
  user: "postgres",
  password: "1234",
  database: "books_db",
  port: 5432,
});

export default pool;