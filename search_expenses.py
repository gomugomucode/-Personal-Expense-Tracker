def search_expenses(conn, keyword):
    cursor = conn.cursor()
    # We use % around the keyword to find it anywhere in the text
    search_term = f"%{keyword}%"
    
    query = '''
    SELECT e.id, e.date, e.description, e.amount, c.name 
    FROM expenses e
    JOIN categories c ON e.category_id = c.id
    WHERE e.description LIKE ? OR c.name LIKE ?
    ORDER BY e.date DESC
    '''
    
    cursor.execute(query, (search_term, search_term))
    results = cursor.fetchall()
    
    if not results:
        print(f"\n      No expenses found matching '{keyword}'.")
    else:
        print(f"\n--- SEARCH RESULTS FOR '{keyword}' ---")
        print(f"{'ID':<4} | {'Date':<20} | {'Description':<15} | {'Amount':<10} | {'Category'}")
        print("-" * 75)
        for row in results:
            print(f"{row[0]:<4} | {row[1]:<20} | {row[2]:<15} | ${row[3]:<9.2f} | {row[4]}")


def search_expenses_by_year(conn, keyword):
    cursor = conn.cursor()
    # We use % around the keyword to find it anywhere in the text
    search_term = f"{keyword}%"
    
    query = '''
    SELECT e.id, e.date, e.description, e.amount, c.name 
    FROM expenses e
    JOIN categories c ON e.category_id = c.id
    WHERE e.date LIKE ? 
    ORDER BY e.date DESC
    '''
    
    cursor.execute(query, [search_term])
    results = cursor.fetchall()
    
    if not results:
        print(f"\n      No expenses found matching '{keyword}'.")
    else:
        print(f"\n--- SEARCH RESULTS FOR '{keyword}' ---")
        print(f"{'ID':<4} | {'Date':<20} | {'Description':<15} | {'Amount':<10} | {'Category'}")
        print("-" * 75)
        for row in results:
            print(f"{row[0]:<4} | {row[1]:<20} | {row[2]:<15} | ${row[3]:<9.2f} | {row[4]}")


def search_expenses_by_month(conn, keyword):
    cursor = conn.cursor()
    # We use % around the keyword to find it anywhere in the text
    search_term = f"%{keyword}%"
    
    query = '''
    SELECT e.id, e.date, e.description, e.amount, c.name 
    FROM expenses e
    JOIN categories c ON e.category_id = c.id
    WHERE e.date LIKE ? 
    ORDER BY e.date DESC
    '''
    
    cursor.execute(query, [search_term])
    results = cursor.fetchall()
    
    if not results:
        print(f"\n      No expenses found matching '{keyword}'.")
    else:
        print(f"\n--- SEARCH RESULTS FOR '{keyword}' ---")
        print(f"{'ID':<4} | {'Date':<20} | {'Description':<15} | {'Amount':<10} | {'Category'}")
        print("-" * 75)
        for row in results:
            print(f"{row[0]:<4} | {row[1]:<20} | {row[2]:<15} | ${row[3]:<9.2f} | {row[4]}")