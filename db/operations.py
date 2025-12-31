import random
import string

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def insert_customer(cursor):
    cursor.execute("""
        USE TEST_MAIN
        INSERT INTO Customers (Name, Email) VALUES (?, ?)"""
        ,
        random_string(),
        f"{random_string()}@test.com"
    )

def update_customer(cursor):
    cursor.execute("""
        USE TEST_MAIN
        UPDATE Customers
        SET Email = ?
        WHERE CustomerID = (
            SELECT TOP 1 CustomerID FROM Customers ORDER BY NEWID()
        )
    """, f"{random_string()}@updated.com")

def delete_customer(cursor):
    cursor.execute("""
        USE TEST_MAIN           
        DELETE FROM Customers
        WHERE CustomerID = (
            SELECT TOP 1 CustomerID FROM Customers ORDER BY NEWID()
        )
    """)
