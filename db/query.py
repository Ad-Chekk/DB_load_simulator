from db.connection import get_connection   

def fetch_all_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Customers")
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]

    cursor.close()
    conn.close()

    return columns, rows
