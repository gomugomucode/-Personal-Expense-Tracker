from datetime import datetime # <--- Add this import!

def add_expense(conn, amount, desc, cat_name):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = ?", (cat_name,))
    result = cursor.fetchone()
    
    if result:
        cat_id = result[0]
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO expenses (amount, description, date, category_id) VALUES (?, ?, ?, ?)",
                       (amount, desc, date_now, cat_id))
        conn.commit()
    else:
        print(f"Error: Category '{cat_name}' not found!")