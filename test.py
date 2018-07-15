from sqlalchemy import create_engine
from sqlalchemy.sql import text

if __name__ == "__main__":

    engine = create_engine('mssql+pymssql://inventorymgmt:angel10!@den1.mssql5.gear.host:1433/inventorymgmt')
    connection = engine.connect()

    s = text(
        "SELECT * FROM VOLUNTEER"
    )
    s = text(
        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
    )

    result = connection.execute(s).fetchall()
    table_names = [item[0] for item in result]
    print(table_names)

    connection.close()
