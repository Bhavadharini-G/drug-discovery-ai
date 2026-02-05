import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect('drug_discovery.db')
c = conn.cursor()

# Create a table for compounds if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS compounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    property REAL
)''')

# Insert a sample compound
c.execute("INSERT INTO compounds (name, property) VALUES (?, ?)", ("aspirin", 123.45))
conn.commit()

# Query and print all compounds
for row in c.execute("SELECT * FROM compounds"):
    print(row)

conn.close()
