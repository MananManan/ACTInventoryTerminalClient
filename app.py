from sqlalchemy import create_engine
from util_methods import *

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
