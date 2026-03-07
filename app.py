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
    
    # 1. HANDLE ADDING DATA (POST)
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']
        category = request.form['category']
        
        # Validation (Professional touch!)
        if amount and description:
            add_expense(conn, float(amount), description, category)
            conn.close()
            return redirect(url_for('index'))

    # 2. HANDLE SEARCHING/VIEWING DATA (GET)
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

    # 3. HANDLE SUMMARY DATA
    summary_sql = '''
        SELECT c.name, SUM(e.amount) as total
        FROM categories c
        LEFT JOIN expenses e ON c.id = e.category_id
        GROUP BY c.name
        HAVING total > 0
    '''
    summary = conn.execute(summary_sql).fetchall()
    
    # Calculate Grand Total
    grand_total = sum(item['total'] for item in summary if item['total'])
        
    categories = get_categories(conn)
    conn.close()
    
    return render_template('index.html', 
                           expenses=expenses, 
                           categories=categories, 
                           search_query=search_query,
                           summary=summary,
                           grand_total=grand_total)
   

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete(expense_id):
    conn = get_db_connection()
    # Using your existing function to remove it from the DB
    delete_expense(conn, expense_id)
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)