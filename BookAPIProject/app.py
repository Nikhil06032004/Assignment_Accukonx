import sqlite3
import requests

# ---------------- CONFIGURATION ---------------- #

API_URL = "https://fakerapi.it/api/v2/books?_quantity=50"
DATABASE = "books.db"

# ---------------- DATABASE ---------------- #

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            publication_year TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_books(books):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    for book in books:
        cursor.execute("""
            INSERT INTO books (title, author, publication_year)
            VALUES (?, ?, ?)
        """, (
            book["title"],
            book["author"],
            book["publication_year"]
        ))

    conn.commit()
    conn.close()


def get_books():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    conn.close()
    return books

# ---------------- API ---------------- #

def fetch_books():
    response = requests.get(API_URL)
    response.raise_for_status()

    data = response.json()["data"]

    books = []

    for item in data:
        books.append({
            "title": item.get("title", "Unknown"),
            "author": item.get("author", "Unknown"),
            "publication_year": item.get("published", "")[:4]
        })

    return books

# ---------------- MAIN ---------------- #

def main():
    print("\nFetching books from API...\n")

    create_table()

    books = fetch_books()

    insert_books(books)

    stored_books = get_books()

    print(f"Successfully stored {len(stored_books)} books.\n")

    print("-" * 80)

    for book in stored_books:
        print(f"""
ID       : {book[0]}
Title    : {book[1]}
Author   : {book[2]}
Year     : {book[3]}
{'-' * 80}
""")

if __name__ == "__main__":
    main()