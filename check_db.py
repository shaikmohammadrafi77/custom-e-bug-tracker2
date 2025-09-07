import sqlite3

# Path to your SQLite DB (instance/bugtracker.db)
db_path = "instance/bugtracker.db"

# Connect to the DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List all tables
print("Tables in database:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
for row in cursor.fetchall():
    print(" -", row[0])

# Check if 'user' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
user_table = cursor.fetchone()
if user_table:
    print("\n✅ 'user' table exists.")
else:
    print("\n❌ 'user' table NOT found.")

# Close connection
conn.close()

