import csv
import sqlite3

# ---------------- CONFIGURATION ---------------- #

CSV_FILE = "email.csv"
DATABASE = "users.db"

# ---------------- DATABASE ---------------- #

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            identifier INTEGER,
            first_name TEXT,
            last_name TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- CSV IMPORT ---------------- #

def import_csv():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            cursor.execute("""
                INSERT INTO users(email, identifier, first_name, last_name)
                VALUES (?, ?, ?, ?)
            """, (
                row["Login email"],
                row["Identifier"],
                row["First name"],
                row["Last name"]
            ))

    conn.commit()
    conn.close()


# ---------------- DISPLAY DATA ---------------- #

def display_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    print("\nUsers Stored in Database\n")
    print("-" * 70)

    for user in users:
        print(f"""
ID          : {user[0]}
Email       : {user[1]}
Identifier  : {user[2]}
First Name  : {user[3]}
Last Name   : {user[4]}
{'-' * 70}
""")

    conn.close()


# ---------------- MAIN ---------------- #

def main():
    print("=" * 60)
    print("CSV Data Import to SQLite Database")
    print("=" * 60)

    create_table()
    import_csv()
    display_users()


if __name__ == "__main__":
    main()