import sqlite3

conn = sqlite3.connect('../database/brosur.db')

conn.execute('''CREATE TABLE BROSUR
         (
         TITLE           TEXT,
         DATE_CREATE     DATE,
         FILE_URL        TEXT,
         SIZE        TEXT,
         HITS         TEXT
         );''')

conn.commit()
conn.close()
print("Table created successfully")