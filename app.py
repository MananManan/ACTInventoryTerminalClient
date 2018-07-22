from sqlalchemy import create_engine
from util_methods import init_app, repl

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
        print("Making sure connection is closed...")

        if connection != None:
            connection.close()
            print("Connection closed.")

        print("Thanks for using the query tool!")
