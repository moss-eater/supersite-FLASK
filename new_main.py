from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def get_db_connection():
    conn = sqlite3.connect("diary.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table (run once automatically)
conn = get_db_connection()
conn.execute("""
CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    subject TEXT NOT NULL,
    content TEXT NOT NULL
)
""")
conn.commit()
conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    entries = conn.execute("SELECT * FROM diary ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("index.html", entries=entries)

@app.route("/add", methods=("GET", "POST"))
def add():
    if request.method == "POST":
        date = request.form["date"]
        subject = request.form["subject"]
        content = request.form["content"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO diary (date, subject, content) VALUES (?, ?, ?)",
            (date, subject, content)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)
