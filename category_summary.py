def show_category_summary(conn):
    cursor = conn.cursor()
    
    # We join the tables, then GROUP BY the category name
    query = '''
    SELECT c.name, SUM(e.amount), COUNT(e.id)
    FROM categories c
    LEFT JOIN expenses e ON c.id = e.category_id
    GROUP BY c.name
    ORDER BY SUM(e.amount) DESC
    '''
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\n" + "="*45)
    print("--- SPENDING BY CATEGORY ---")
    print(f"{'Category':<15} | {'Total ($)':<12} | {'Count'}")
    print("-" * 45)
    
    for row in results:
        # If a category has no expenses, SUM returns None. We handle that with 'or 0'
        category = row[0]
        total = row[1] if row[1] is not None else 0.0
        count = row[2]
        
        print(f"{category:<15} | ${total:<11.2f} | {count} items")
    print("="*45)