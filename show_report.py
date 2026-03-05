def show_report(conn):
    cursor = conn.cursor()
    # Using JOIN to show the Category Name instead of just the ID number
    query = '''
    SELECT e.id, e.date, e.description, e.amount, c.name 
    FROM expenses e
    JOIN categories c ON e.category_id = c.id
    ORDER BY e.date DESC
    '''
    cursor.execute(query)
    print("\n--- EXPENSE REPORT ---")
    print(f"{'ID':<4} | {'Date':<20} | {'Description':<15} | {'Amount':<10} | {'Category'}")

    for row in cursor.fetchall():
        print(f"{row[0]:<4} | {row[1]:<20} | {row[2]:<15} | ${row[3]:<9.2f} | {row[4]}")