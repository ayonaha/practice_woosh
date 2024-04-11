from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import sqlite3
import shutil
import os

# Define the schema for the Whoosh index
schema = Schema(
    foo_id=ID(stored=True),
    bar_id=ID(stored=True),
    a=TEXT(stored=True),
    x=TEXT(stored=True)
)

# Ensure the index directory exists
if os.path.exists("indexdir"):
    # Recursively delete the directory
    shutil.rmtree("indexdir")

# Create the directory
os.mkdir("indexdir")

# Create or open the index
ix = create_in("indexdir", schema)

# Connect to the SQLite database
conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()

# Perform the SQL query to join Foo, Bar, and Foo2Bar
query = """
SELECT f.foo_id, b.bar_id, f.a, b.x
FROM Foo2Bar fb
JOIN Foo f ON fb.foo_id = f.foo_id
JOIN Bar b ON fb.bar_id = b.bar_id
"""

cursor.execute(query)

# Index the results
writer = ix.writer()
for foo_id, bar_id, a, x in cursor.fetchall():
    writer.add_document(foo_id=str(foo_id), bar_id=str(bar_id), a=a, x=x)
writer.commit()

# Verify the documents were inserted correctly
with ix.searcher() as searcher:
    # Print out the first 10 documents
    all_docs = searcher.documents()
    for doc in all_docs:
        print(doc)

cursor.close()
conn.close()
