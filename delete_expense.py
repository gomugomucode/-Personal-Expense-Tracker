def delete_expense(conn, expense_id):
    cursor = conn.cursor()
    
    # Check if the ID actually exists first
    cursor.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        return True
    return False