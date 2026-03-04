from add_expense import add_expense
from db import init_db
from show_report import show_report
from get_total_spent import get_total_spent

db_conn = init_db()

# Let's add an expense
add_expense(db_conn, 15.50, "Pizza Night", "Food")
add_expense(db_conn, 40.00, "Gas Station", "Transport")

# Let's see the results
show_report(db_conn)
get_total_spent(db_conn)

db_conn.close()