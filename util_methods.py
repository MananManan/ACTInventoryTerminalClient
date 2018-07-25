from tabulate import tabulate
from sqlalchemy import *
from sqlalchemy.sql import text
from sqlalchemy.exc import ProgrammingError
from functools import partial

# Global vars
options = ["View a table", "Insert into table", "Delete from table","Modify a table", "Quit"]
num_options = len(options)
table_names = []
num_tables = None
primary_keys = dict() #initialize an empty dictionary


def init_app(connection): # this was the method being called from app.py
    global table_names
    global num_tables

    # q stands for query
    
    q = text(
        "SELECT TABLE_NAME "
        "FROM INFORMATION_SCHEMA.TABLES "
        "WHERE TABLE_TYPE='BASE TABLE'"
    ) # this statement is query and accesses the MSSQL's database table, basically gets all the base tables

    result = connection.execute(q).fetchall() #get all the table information, returns a list of tables
    table_names = [item[0] for item in result] #iterate over the fetched tables


    for name in table_names: #start filling the dictionary with the name as table name and value as empty lists, for now
        primary_keys[name] = []

    q = text(
        "SELECT\n"
            "A.TABLE_NAME,\n"
            "A.CONSTRAINT_NAME,\n" 
            "B.COLUMN_NAME,\n"
            "CONSTRAINT_TYPE\n"
        "FROM\n"
            "INFORMATION_SCHEMA.TABLE_CONSTRAINTS A,\n"
            "INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE B\n"
        "WHERE\n" 
            "A.CONSTRAINT_NAME = B.CONSTRAINT_NAME\n"
        "ORDER BY\n"
            "A.TABLE_NAME\n"
    )# see above

    results = connection.execute(q).fetchall() #see above

    for result in results:
        key_type = result[3].lower() #fourth entry is the key type
        if key_type.find("primary") != -1:#if the keytype is primary key
            primary_keys[result[0]].append(result[2]) #add the primary key to the list returned by the dictionary

    num_tables = len(table_names) #find out the number of tables

def show_menu():

    opts = options

    print("What would you like to do?")
    print()
    for (i, item) in enumerate(opts):
        print("\t" + str(i+1)+ ")" + str(item))

def format_into_English_list(lst):
    if len(lst) < 3:
        return " and ".join(lst)
    else:
        return ", ".join(lst[:-1]) + " and " + lst[-1]

def select_table(message, connection):

    choice = -1
    while choice < 0 or choice > num_tables:

        print(message)
        print()

        for (i, table) in enumerate(table_names):
            print("\t", end = '', flush = True)
            print(str(i+1).ljust(4), end = '', flush = True)
            print(str(table))
        print("\t" + "0".ljust(4) + "Go Back")
        print()
        try:
            choice = int(input("Please select a number between 1 and " + str(num_tables) + ": ")) 
        except:
            print("Please enter a valid number")
            print()
            continue

        print()

        if choice > num_tables or choice < 0:
            print("Please enter a valid number")
            print()

    return choice

def view_table(connection):

    choice = select_table("Which table would you like to view?", connection)

    if choice == 0:
        return
    
    q = text(
        "SELECT * FROM " + str(table_names[choice - 1])
    )
    
    results = connection.execute(q)
    cols = results.keys()
    results = results.fetchall()
    print(tabulate(results,cols,tablefmt="pipe")) #tabulates the above things
    return choice

def delete_from_table(connection):
    choice = select_table("Which table would you like to delete from?", connection)

    if choice == 0:
        return
    
    q = text(
        "SELECT * FROM " + str(table_names[choice-1])
        )
    results = connection.execute(q)
    cols = results.keys()
    results = results.fetchall()
    
    
    print(tabulate(results,cols,tablefmt="pipe",showindex=range(1,len(results)+1))) #tabulates the above things
    
    rowdel = input("Enter the row number you want to delete (0 to cancel) : ")
    rowdel = int(rowdel)
    if rowdel == 0:
        return
    queryText = "DELETE FROM " + table_names[choice-1] + " WHERE "
    
    #finding the length of primary key
    primary_key = primary_keys[table_names[choice-1]]
    
    for k in primary_key:
        queryText += k + "="
        i = cols.index(k)
        ans = results[rowdel-1][i]
        if type(ans) == type(0): #if ans is integer
            queryText += str(ans)
        else:
            queryText += "'" + ans + "'"
        queryText += " AND "
    
    queryText += " 0=0 "
    
    transaction = connection.begin()
    
    q = text(queryText)
    try:
        connection.execute(q)
    except Exception as e:
        print("There was an error!")
        print(e)
        print("Going back to the main menu")
    finally:
        transaction.commit()
    
    return choice

def insert_into_table(connection):
    choice = select_table("Which table would you like to insert into?", connection)

    if choice == 0:
        return
    
    q = text(
        "SELECT * FROM " + str(table_names[choice-1])
        )
    results = connection.execute(q)
    cols = results.keys()
    results = results.fetchall()

    print(tabulate(results,cols,tablefmt="pipe")) #tabulates the above things
    insertion = input("Enter insertion in tuple format (0 to cancel): ")
    
    if insertion == "0":
        return
     
    q = text(
        "INSERT INTO " + table_names[choice-1] + " VALUES " + insertion    
        )
    
    transaction = connection.begin()
    
    try:
        connection.execute(q)
    except Exception as e:
        print("There was an error!")
        print(e)
        print("Going back to the main menu")
    finally:
        transaction.commit()
    
    return choice

def modify_table(connection):
    # TODO
    choice = select_table("Which table would you like to insert into?", connection)

    if choice == 0:
        return
    
    q = text(
        "SELECT * FROM " + str(table_names[choice-1])
        )
    results = connection.execute(q)
    cols = results.keys()
    results = results.fetchall()
    
    header = [str(x) + "." + y for x,y in zip(range(1,len(cols)+1), cols)]
    
    print(tabulate(results,header,tablefmt="pipe",showindex=range(1,len(results)+1))) #tabulates the above things
    mod_row = int(input("Enter the row you want to modify stuff in (0 to cancel): "))
    if mod_row == 0:
        return
    mod_col = int(input("Enter the column you want to modify in (0 to cancel): "))
    if mod_col == 0:
        return
    modification = input("Enter your modification (0 to cancel): ")
    if modification == "0":
        return
    
       
    queryText = "UPDATE " + table_names[choice-1] + " SET " + cols[mod_col-1] + "="
    
    if type(results[0][mod_col-1]) == type(0): #if ans is integer
        queryText += str(modification)
    else:
        queryText += "'" + modification + "'"
    
    queryText += " WHERE "
    
    primary_key = primary_keys[table_names[choice-1]]
    
    for k in primary_key:
        queryText += k + "="
        i = cols.index(k)
        ans = results[mod_row-1][i]
        if type(ans) == type(0): #if ans is integer
            queryText += str(ans)
        else:
            queryText += "'" + ans + "'"
        queryText += " AND "
    
    queryText += " 0=0 "

    q = text(queryText)

    transaction = connection.begin()
    
    try:
        connection.execute(q)
    except Exception as e:
        print("There was an error!")
        print(e)
        print("Going back to the main menu")
    finally:
        transaction.commit()
    
    return choice

def repl(connection):

    choice = -1
    hasDoneSomething = False

    while choice != len(options):
        if hasDoneSomething:
            print('-' * 110)
            
        show_menu()
        print()
        try:
            choice = int(input("Select a number between 1 and " + str(num_options) +": ")) 
        except:
            print("Please enter a valid number.")
            print()
            continue

        print()
        hasDoneSomething = True

        if choice == 1:
            view_table(connection)
        elif choice == 2:
            insert_into_table(connection)
        elif choice == 3:
            delete_from_table(connection)
        elif choice ==4:
            modify_table(connection)
        elif choice > 5 or choice < 1:
            print("Please enter a valid number.")
