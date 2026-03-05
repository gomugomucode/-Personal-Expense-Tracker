

def get_categories(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories")
    # This returns a list of tuples like [('Food',), ('Transport',)]
    # We use a list comprehension to clean it up to ['Food', 'Transport']
    return [row[0] for row in cursor.fetchall()]