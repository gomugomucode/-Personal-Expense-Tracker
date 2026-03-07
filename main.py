# from add_expense import add_expense
# from db import init_db
# from show_report import show_report
# from get_total_spent import get_total_spent

# db_conn = init_db()

# Let's add an expense
# add_expense(db_conn, 15.50, "Pizza Night", "Food")
# add_expense(db_conn, 40.00, "Gas Station", "Transport")


# # Let's see the results
# show_report(db_conn)
# get_total_spent(db_conn)


# db_conn.close()



import sqlite3
from db import init_db
from add_expense import add_expense
from show_report import show_report
from get_total_spent import get_total_spent
from list_categories import get_categories
from delete_expense import delete_expense
from search_expenses import search_expenses, search_expenses_by_month, search_expenses_by_year
from export_to_csv import export_expenses
from category_summary import show_category_summary 
from check_budgets import set_budget, get_budget_status

db_conn = init_db()

userinput = 0

while userinput != 11:
    print("\n--- Menu ---")
    print("1. To add the data")
    print("2. To show the data")
    print("3. To get the total spent balance")
    print("4. To add a new category")
    print("5. To delete an expense")
    print("6. To search expenses")
    print("7. To export data to CSV")
    print("8. To show category summary")
    print("9. To set a monthly budget")
    print("10. To check budget status")
    print("11. To exit the program")

    try:
        userinput = int(input("\nEnter choice: "))
    except ValueError:
        print(" Please enter a valid number!")
        continue

    if userinput == 1:
        available_cats = get_categories(db_conn)
        print(f"Available Categories: {', '.join(available_cats)}")
        
        cat_name = input("Enter Category: ")
        descr = input("Enter description (Min 3 and Max 20): ")

        # YOUR VALIDATION LOGIC
        if len(descr) < 3:
            print("  Error: Minimum 3 characters needed in description.")
            continue
        elif len(descr) > 20: 
            print("  Error: Description is too long (Max 20).")
            continue 
        
        try:
            amou = float(input("Enter amount (in dollars): "))
            if add_expense(db_conn, amou, descr, cat_name):
                print("  Success: Expense recorded.")
            else:
                print("  Error: That category doesn't exist.")
        except ValueError:
            print("  Error: Amount must be a number.")

    elif userinput == 2:
        show_report(db_conn)

    elif userinput == 3:
        get_total_spent(db_conn)
    
    elif userinput == 4:
        new_cat = input("Enter the name of the new category: ")
        if new_cat:
            try:
                cursor = db_conn.cursor()
                cursor.execute("INSERT INTO categories (name) VALUES (?)", (new_cat,))
                db_conn.commit()
                print(f"  Category '{new_cat}' added successfully!")
            except sqlite3.IntegrityError:
                print("  Error: This category already exists.")

    elif userinput == 5:
        show_report(db_conn) 
        try:
            target_id = int(input("\nEnter the ID of the expense to delete: "))
            confirm = input(f"Are you sure you want to delete ID {target_id}? (y/n): ")
            if confirm.lower() == 'y':
                if delete_expense(db_conn, target_id):
                    print(f"  Expense {target_id} deleted.")
                else:
                    print("  Error: ID not found.")
        except ValueError:
            print("  Error: Please enter a valid numerical ID.")
    
    elif userinput == 6:
        print("Search by: 1. Keyword  2. Year  3. Month")
        sub_choice = input("Choice: ")
        
        if sub_choice == '1':
            keyword = input("Keyword: ")
            if len(keyword) < 2:
                print("  Search term too short!")
            else:
                search_expenses(db_conn, keyword)

        elif sub_choice == '2':
            y = input("Year (YYYY): ")
            # YOUR DIGIT VALIDATION
            if y.isdigit():
                search_expenses_by_year(db_conn, y) 
            else:
                print("  Error: Enter a number for the year (e.g., 2026).")

        elif sub_choice == '3':
            m = input("Month (MM): ")
            # YOUR DIGIT VALIDATION
            if m.isdigit():
                search_expenses_by_month(db_conn, m)
            else:
                print("  Error: Enter a number for the month (1-12).")
    
    elif userinput == 7:
        export_expenses(db_conn)

    elif userinput == 8:
        show_category_summary(db_conn)

    elif userinput == 9:
        # BUDGET SETTING
        cat = input("Enter category name: ")
        try:
            lim = float(input("Enter monthly budget limit: "))
            if set_budget(db_conn, cat, lim):
                print(f"  Budget set for {cat}.")
            else:
                print("  Error: Category not found.")
        except ValueError:
            print("  Error: Limit must be a number.")

    elif userinput == 10:
        get_budget_status(db_conn)

    elif userinput == 11:
        print("Exiting...")
        
    else:
        print(" Invalid choice. Please pick 1-11.")

db_conn.close()