from db.connection import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("PRAGMA table_info(experiments);")
print(cur.fetchall())
conn.close()
