import pyodbc #module to connect to sql server (it needs to be installed first)

#connect information to SQL Server
def connection_information():
    sqlServerName = r"YourServerName"
    databaseName = "YourDatabaseName"
    trusted_connection = "yes"

    connection_string = (
    f"DRIVER={{SQL Server}};"
    f"SERVER={sqlServerName};"
    f"DATABASE={databaseName};"
    f"Trusted_connection={trusted_connection}"
    )

    return connection_string

def get_connection():
    return pyodbc.connect(connection_information())