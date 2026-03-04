def show_report(conn):
    cursor = conn.cursor()
    # Using JOIN to show the Category Name instead of just the ID number
    query = '''
    SELECT e.date, e.description, e.amount, c.name 
    FROM expenses e
    JOIN categories c ON e.category_id = c.id
    ORDER BY e.date DESC
    '''
    cursor.execute(query)
    print("\n--- EXPENSE REPORT ---")
    for row in cursor.fetchall():
        print(f"{row[0]} | {row[1]} | ${row[2]} ({row[3]})")