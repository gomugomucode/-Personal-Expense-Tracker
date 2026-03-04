def get_total_spent(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM expenses')

    # fetchone() returns something like (145.50,)
    result = cursor.fetchone()
    
    # Check if result[0] is None (happens if no expenses exist yet)
    total = result[0] if result[0] is not None else 0.0
    
    print(f'The total balance spent is: ${total:.2f}')
    return total