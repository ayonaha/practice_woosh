import sqlite3

# Connect to the SQLite database
# It will create the database file if it doesn't exist
conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()

# Create the Foo table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Foo (
    foo_id INTEGER PRIMARY KEY,
    template_id INTEGER,
    a TEXT,
    b TEXT
)
''')

# Create the Bar table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Bar (
    bar_id INTEGER PRIMARY KEY,
    template_id INTEGER,
    x TEXT,
    y TEXT
)
''')

# Create the Foo2Bar linking table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Foo2Bar (
    foo_id INTEGER,
    bar_id INTEGER,
    FOREIGN KEY (foo_id) REFERENCES Foo (foo_id),
    FOREIGN KEY (bar_id) REFERENCES Bar (bar_id)
)
''')

# Populate the Foo table with dummy data
foo_data = [
    (1, 100, 'Apple', 'Fruit'),
    (2, 101, 'Banana', 'Fruit'),
    (3, 102, 'Carrot', 'Vegetable')
]

cursor.executemany('INSERT INTO Foo (foo_id, template_id, a, b) VALUES (?, ?, ?, ?)', foo_data)

# Populate the Bar table with dummy data
bar_data = [
    (1, 200, 'Xylophone', 'Musical Instrument'),
    (2, 201, 'Yacht', 'Vehicle'),
    (3, 202, 'Zebra', 'Animal')
]

cursor.executemany('INSERT INTO Bar (bar_id, template_id, x, y) VALUES (?, ?, ?, ?)', bar_data)

# Populate the Foo2Bar linking table with dummy data
foo2bar_data = [
    (1, 1),
    (2, 2),
    (3, 3)
]

cursor.executemany('INSERT INTO Foo2Bar (foo_id, bar_id) VALUES (?, ?)', foo2bar_data)

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Database populated successfully.")
