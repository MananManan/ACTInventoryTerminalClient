from sqlalchemy import create_engine
from sqlalchemy.sql import text

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
    num_tables = len(table_names)

def show_menu():

    opts = options
    n = len(opts)

    print("What would you like to do?")
    for (i, item) in enumerate(opts):
        print(f"\t{i+1}. {item}")

def view_table(connection):

    choice = -1
    while choice < 1 or choice > num_tables:

        print("Which table would you like to view?")
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

def run_query(connection):
    # TODO
    print("Need to add code here...")
    pass

def repl(connection):

    choice = -1

    while choice != 3:
        show_menu()
        print()

        try:
            choice = int(input(f"Select a number between 1 and {num_options}: ")) 
        except:
            print("Please enter a valid number.")
            print()
            continue

        print()

        if choice == 1:
            view_table(connection)
            print()
        elif choice == 2:
            run_query(connection)
            print()
        elif choice > 3 or choice < 1:
            print("Please enter a valid number.")
            print()

    print("Thanks for using the query tool!")


if __name__ == "__main__":
    
    connection = None

    try:
        print("Establishing connection...")
        engine = create_engine('mssql+pymssql://inventorymgmt:angel10!@den1.mssql5.gear.host:1433/inventorymgmt')
        connection = engine.connect()
        print("Connected!")
        print()

        init_app(connection)
        repl(connection)

    finally:
        if connection != None:
            connection.close()
