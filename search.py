import sqlite3
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin, OrGroup
from whoosh.query import Or

def search_index(a_val, x_val):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        parser = MultifieldParser(["a", "x"], schema=ix.schema)
        parser.add_plugin(FuzzyTermPlugin())

        # Construct individual fuzzy queries for 'a' and 'x'
        a_query = parser.parse(f"{a_val}~2")
        x_query = parser.parse(f"{x_val}~2")

        # Combine queries using an OR operation
        combined_query = Or([a_query, x_query])

        # Execute the combined fuzzy search
        results = searcher.search(combined_query, limit=None)
        for result in results:
            print(f"foo_id: {result['foo_id']}, bar_id: {result['bar_id']}")



def query_databases(foo_id, bar_id):
    # Connect to the SQLite database
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()

    # Query Foo and Bar tables
    cursor.execute("SELECT * FROM Foo WHERE foo_id=?", (foo_id,))
    foo_result = cursor.fetchone()
    cursor.execute("SELECT * FROM Bar WHERE bar_id=?", (bar_id,))
    bar_result = cursor.fetchone()

    print(f"Foo Result: {foo_result}")
    print(f"Bar Result: {bar_result}")

    cursor.close()
    conn.close()


# Example search
a_val = "a"
x_val = "ach"
print(search_index(a_val, x_val))

# Example DB query (replace with actual foo_id and bar_id from search results)
# query_databases(foo_id, bar_id)
