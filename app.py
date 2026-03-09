from flask import Flask, render_template, request, redirect, url_for
import sqlite3
# Assuming your previous logic is in these files
from list_categories import get_categories 
from add_expense import add_expense
from delete_expense import delete_expense # Reusing your existing logic!

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    
    # 1. Handle Form Submission (Adding Expense)
    if request.method == 'POST':
        try:
            amount = request.form.get('amount')
            description = request.form.get('description')
            category = request.form.get('category')
            
            if amount and description:
                # Use your existing add_expense logic
                add_expense(conn, float(amount), description, category)
                # We don't close yet; we redirect to refresh the page
                return redirect(url_for('index'))
        except Exception as e:
            print(f"Error adding expense: {e}")

    # 2. Handle Search Query
    search_query = request.args.get('q', '')
    if search_query:
        sql = '''
            SELECT e.id, e.date, e.description, e.amount, c.name 
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.description LIKE ? OR c.name LIKE ?
            ORDER BY e.date DESC
        '''
        term = f"%{search_query}%"
        expenses = conn.execute(sql, (term, term)).fetchall()
    else:
        expenses = conn.execute('''
            SELECT e.id, e.date, e.description, e.amount, c.name 
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            ORDER BY e.date DESC
        ''').fetchall()

    # 3. Handle Summary Data for Chart and Cards
    summary_sql = '''
        SELECT c.name, SUM(e.amount) as total
        FROM categories c
        LEFT JOIN expenses e ON c.id = e.category_id
        GROUP BY c.name
        HAVING total > 0
    '''
    summary = conn.execute(summary_sql).fetchall()
    
    # Prepare chart data
    chart_labels = [row['name'] for row in summary]
    chart_values = [row['total'] for row in summary]
    grand_total = sum(row['total'] for row in summary if row['total'])
    
    # Get categories for the dropdown
    categories = get_categories(conn)
    
    conn.close() # Close at the very end

    return render_template('index.html', 
                           expenses=expenses, 
                           categories=categories, 
                           search_query=search_query,
                           summary=summary,
                           grand_total=grand_total,
                           chart_labels=chart_labels,
                           chart_values=chart_values)  

   

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete(expense_id):
    conn = get_db_connection()
    # Using your existing function to remove it from the DB
    delete_expense(conn, expense_id)
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)