from db.connection import get_connection

def create_customers_table():
    """
    Creates Customers table if not exists.
    SQL Server specific.
    """
    query = """
    IF NOT EXISTS (
        SELECT * FROM sys.tables WHERE name = 'Customers'
    )
    BEGIN
        CREATE TABLE Customers (
            CustomerID INT IDENTITY PRIMARY KEY,
            Name NVARCHAR(100),
            Email NVARCHAR(100),
            CreatedDate DATETIME DEFAULT GETDATE()
        )
    END
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
