import pyodbc

def get_connection():
    """
    SQL Server connection using Windows Authentication.
    DB-specific code isolated here.
    """
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=TEST_MAIN;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str, autocommit=False)
