import sqlite3

db = sqlite3.connect("instance/database.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

cur.execute("""
CREATE TABLE diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    entry TEXT
)
""")

# Sample users
cur.execute("INSERT INTO users VALUES (NULL, 'teacher1', 'pass', 'teacher')")
cur.execute("INSERT INTO users VALUES (NULL, 'student1', 'pass', 'student')")

db.commit()
db.close()
