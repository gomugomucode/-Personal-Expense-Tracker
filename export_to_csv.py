import csv

def export_expenses(conn, filename="my_expenses.csv"):
    cursor = conn.cursor()
    query = '''
    SELECT e.id, e.date, e.description, e.amount, c.name 
    FROM expenses e
    JOIN categories c ON e.category_id = c.id
    ORDER BY e.date DESC
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    # Define the headers for the Excel file
    headers = ['ID', 'Date', 'Description', 'Amount', 'Category']

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write the top row
        writer.writerows(rows)    # Write all the data
    
    print(f"✅ Data exported successfully to {filename}!")