
import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=TEST_MAIN;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

cnxn = get_connection()
cursor = cnxn.cursor()
# cursor.execute(
#         """

# SELECT * FROM  Payments ;
# """
#     )

# print(cursor.fetchall())


cursor.execute("""
        INSERT INTO Customers (Name, Email) VALUES ("Raji", "raji@email.com")"""
      
    )

print(cursor.rowcount())  #returns the number of rows modified by the last sql 