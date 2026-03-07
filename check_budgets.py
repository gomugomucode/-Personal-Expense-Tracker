def set_budget(conn, cat_name, limit):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = ? COLLATE NOCASE", (cat_name,))
    row = cursor.fetchone()
    if row:
        # REPLACE INTO handles both "Add" and "Update"
        cursor.execute("REPLACE INTO budgets (category_id, limit_amount) VALUES (?, ?)", (row[0], limit))
        conn.commit()
        return True
    return False

def get_budget_status(conn):
    cursor = conn.cursor()
    # This JOIN compares actual spending vs. the budget limit
    query = '''
    SELECT c.name, SUM(e.amount), b.limit_amount
    FROM categories c
    JOIN budgets b ON c.id = b.category_id
    LEFT JOIN expenses e ON c.id = e.category_id
    GROUP BY c.name
    '''
    cursor.execute(query)
    print("\n--- BUDGET STATUS ---")
    for name, spent, limit in cursor.fetchall():
        spent = spent or 0.0
        status = " OK" if spent <= limit else " OVER BUDGET!"
        print(f"{name:<12}: ${spent:>7.2f} / ${limit:>7.2f} {status}")