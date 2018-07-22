from sqlalchemy.sql import text
from sqlalchemy.exc import ProgrammingError
from functools import partial

# Global vars
options = ["View a table", "Run another query", "Quit"]
num_options = len(options)
table_names = []
num_tables = None

def init_app(connection):
    
    global table_names
    global num_tables

    q = text(
        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
    )
    result = connection.execute(q).fetchall()
    table_names = [item[0] for item in result]
    q = text(
        "SELECT ColumnName = col.column_name" 
        "FROM information_schema.table_constraints tc"
        "INNER JOIN information_schema.key_column_usage col"
        "ON col.Constraint_Name = tc.Constraint_Name"
        "AND col.Constraint_schema = tc.Constraint_schema"
        "WHERE tc.Constraint_Type = 'Primary Key' AND col.Table_name = '" 
        f"table_names[0]"
        "'" 
    )
    primary_keys = connection.execute(q).fetchall()
    num_tables = len(table_names)

def show_menu():

    opts = options

    print("What would you like to do?")
    for (i, item) in enumerate(opts):
        print(f"\t{i+1}. {item}")

def select_table(message, connection):

    choice = -1
    while choice < 1 or choice > num_tables:

        print(message)
        print()

        for (i, table) in enumerate(table_names):
            print("\t", end = '', flush = True)
            print(f"{i+1}.".ljust(4), end = '', flush = True)
            print(f"{table}")

        print()
        try:
            choice = int(input(f"Please select a number between 1 and {num_tables}: ")) 
        except:
            print("Please enter a valid number")
            print()
            continue

        print()

        if choice > num_tables or choice < 1:
            print("Please enter a valid number")
            print()

    return choice

def view_table(connection):

    choice = select_table("Which table would you like to view?", connection)
 
    q = text(
        f"SELECT * FROM {table_names[choice - 1]}"
    )

    results = connection.execute(q)   
    cols = results.keys()
    results = results.fetchall()

    print(', '.join(cols))
    print()

    for result in results:
        print(result)

    return choice

def delete_from_table(connection):

    choice = select_table("Which table would you like to delete from?", connection)

    q = text(
        f"SELECT * FROM {table_names[choice - 1]}"
    )

    results = connection.execute(q)   
    cols = results.keys()
    results = results.fetchall()

    print(', '.join(cols))
    print()
    for result in results:
        print(result)

    print()


def run_query(connection):
    # TODO
    print("Need to add code here...")
    pass

def repl(connection):

    choice = -1
    hasDoneSomething = False

    while choice != 3:
        if hasDoneSomething:
            print('-' * 110)
        show_menu()
        print()

        try:
            choice = int(input(f"Select a number between 1 and {num_options}: ")) 
        except:
            print("Please enter a valid number.")
            print()
            continue

        print()
        hasDoneSomething = True

        if choice == 1:
            view_table(connection)
            print()
        elif choice == 2:
            run_query(connection)
            print()
        elif choice > 3 or choice < 1:
            print("Please enter a valid number.")
            print()
