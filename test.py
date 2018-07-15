from sqlalchemy import create_engine
from sqlalchemy.sql import text

if __name__ == "__main__":
    engine = create_engine('mssql+pymssql://inventorymgmt:angel10!@den1.mssql5.gear.host:1433/inventorymgmt')
    connection = engine.connect()
    s = text(
        "SELECT * FROM VOLUNTEER"
    )
    result =connection.execute(s).fetchall()
    for item in result:
        print(item)
    connection.close()
