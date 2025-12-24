import pool from "@/lib/db";
import { NextResponse } from "next/server";

export async function GET() {
  try {
    const result = await pool.query(
  "SELECT * FROM books ORDER BY category"
);
    return NextResponse.json(result.rows);
  } catch (error) {
    console.error("DB ERROR:", error);   
    return NextResponse.json(
      {
        error: "Database error",
        details: error.message   
      },
      { status: 500 }
    );
  }
}