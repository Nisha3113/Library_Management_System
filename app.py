from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "library.db"


# ----------------------------
# Database Connection
# ----------------------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# Home Page
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------------
# Login Page
# ----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            return redirect(url_for("dashboard"))

        else:
            return render_template(
                "login.html",
                msg="Invalid Username or Password"
            )

    return render_template("login.html")


# ----------------------------
# Dashboard
# ----------------------------
@app.route("/dashboard")
def dashboard():

    conn = get_db()

    total_books = conn.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    available = conn.execute(
        "SELECT COUNT(*) FROM books WHERE status='Available'"
    ).fetchone()[0]

    issued = conn.execute(
        "SELECT COUNT(*) FROM books WHERE status='Issued'"
    ).fetchone()[0]

    books = conn.execute(
        "SELECT * FROM books"
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total=total_books,
        available=available,
        issued=issued,
        books=books
    )


# ----------------------------
# Books Page
# ----------------------------
@app.route("/books")
def books():

    conn = get_db()

    books = conn.execute(
        "SELECT * FROM books ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("books.html", books=books)


# ----------------------------
# Add Book
# ----------------------------
@app.route("/add", methods=["POST"])
def add():

    title = request.form["title"]
    author = request.form["author"]
    category = request.form["category"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO books
        (title, author, category, status)
        VALUES (?, ?, ?, ?)
        """,
        (title, author, category, "Available")
    )

    conn.commit()

    conn.close()

    return redirect(url_for("books"))


# ----------------------------
# Delete Book
# ----------------------------
@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM books WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    return redirect(url_for("books"))


# ----------------------------
# Run Application
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)