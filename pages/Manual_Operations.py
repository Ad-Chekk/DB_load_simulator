from db.operations import insert_customer, update_customer, delete_customer
from db.connection import get_connection
import streamlit as st


st.title("Manual DB Operations")

conn = get_connection()
cursor = conn.cursor()

if st.button("Manual INSERT"):
    insert_customer(cursor)
    conn.commit()
    st.success("Row inserted successfully")

if st.button("Manual UPDATE"):
    update_customer(cursor)
    conn.commit()
    st.success("Row updated successfully")

if st.button("Manual DELETE"):
    delete_customer(cursor)
    conn.commit()
    st.success("Row deleted successfully")

cursor.close()
conn.close()


from db.query import fetch_all_customers
import pandas as pd
import streamlit as st 



st.title("View DB")

if st.button("Refresh Data"):
    cols, rows = fetch_all_customers()
    df = pd.DataFrame.from_records(rows, columns=cols)
    st.dataframe(df, use_container_width=True)
