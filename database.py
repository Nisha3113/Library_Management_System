import sqlite3

# Connect to SQLite Database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# ==========================================
# Create Users Table
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# ==========================================
# Create Books Table
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

# ==========================================
# Insert Default Admin User
# ==========================================
cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
admin = cursor.fetchone()

if admin is None:
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "admin123")
    )

# ==========================================
# Insert Sample Books (Only Once)
# ==========================================
cursor.execute("SELECT COUNT(*) FROM books")
count = cursor.fetchone()[0]

if count == 0:

    books = [
        ("Python Programming", "Guido van Rossum", "Programming", "Available"),
        ("Java Complete Reference", "Herbert Schildt", "Programming", "Available"),
        ("Operating System Concepts", "Galvin", "Computer Science", "Issued"),
        ("Database System Concepts", "Navathe", "Database", "Available"),
        ("Computer Networks", "Forouzan", "Networking", "Available")
    ]

    cursor.executemany(
        """
        INSERT INTO books
        (title, author, category, status)
        VALUES (?, ?, ?, ?)
        """,
        books
    )

# ==========================================
# Save Changes
# ==========================================
conn.commit()

conn.close()

print("===================================")
print(" Library Database Created Successfully ")
print("===================================")
print("Default Login")
print("Username : admin")
print("Password : admin123")