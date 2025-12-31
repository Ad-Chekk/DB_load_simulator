import streamlit as st
import threading
import pandas as pd
import time

from engine.simulator import LoadSimulator
from db.schema import create_customers_table
from db.connection import get_connection
from db.operations import insert_customer, update_customer, delete_customer
from db.query import fetch_all_customers

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="DB Load Simulator",
    layout="wide",
    page_icon="🗄️"
)

st.title("Database Load Simulator Dashboard")

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "simulator" not in st.session_state:
    st.session_state.simulator = None
    st.session_state.thread = None

# -------------------------------------------------
# SCHEMA SETUP
# -------------------------------------------------
with st.container(border=True):
    st.subheader("📦 Database Setup")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Create Customers Table"):
            create_customers_table()
            st.success("Customers table ready.")
    with col2:
        st.caption("Ensures required schema exists before simulation")

# -------------------------------------------------
# SIMULATION CONTROLS
# -------------------------------------------------
with st.container(border=True):
    st.subheader("⚙️ Load Simulation Controls")

    c1, c2, c3 = st.columns(3)

    with c1:
        qps = st.slider("Queries / Second", 1, 50, 1)

    with c2:
        duration = st.slider("Duration (seconds)", 1, 300, 10)

    with c3:
        st.markdown("**Simulation Actions**")
        start = st.button("▶️ Start")
        stop = st.button("⏹️ Stop")

    if start:
        simulator = LoadSimulator(
            get_connection_fn=get_connection,
            insert_fn=insert_customer,
            update_fn=update_customer,
            delete_fn=delete_customer,
        )

        thread = threading.Thread(
            target=simulator.run,
            args=(qps, duration),
            daemon=True
        )

        st.session_state.simulator = simulator
        st.session_state.thread = thread
        thread.start()

        st.success("Simulation started")

    if stop and st.session_state.simulator:
        st.session_state.simulator.stop()
        st.warning("Simulation stopped")

# -------------------------------------------------
# SIMULATION KPIs
# -------------------------------------------------
with st.container(border=True):
    st.subheader("📊 Simulation Metrics")

    if st.session_state.simulator:
        sim = st.session_state.simulator

        k1, k2, k3 = st.columns(3)
        k1.metric("INSERTS", sim.insert_count)
        k2.metric("UPDATES", sim.update_count)
        k3.metric("DELETES", sim.delete_count)

        total_ops = sim.insert_count + sim.update_count + sim.delete_count
        st.progress(min(total_ops / max(duration * qps, 1), 1.0))

        chart_df = pd.DataFrame({
            "Operation": ["Insert", "Update", "Delete"],
            "Count": [sim.insert_count, sim.update_count, sim.delete_count]
        }).set_index("Operation")

        st.bar_chart(chart_df)

    else:
        st.info("Simulation not running")

# -------------------------------------------------
# MANUAL OPERATIONS
# -------------------------------------------------
with st.container(border=True):
    st.subheader("🛠️ Manual DB Operations")

    col1, col2, col3 = st.columns(3)
    conn = get_connection()
    cursor = conn.cursor()

    with col1:
        if st.button("➕ Manual INSERT"):
            insert_customer(cursor)
            conn.commit()
            st.success("Row inserted")

    with col2:
        if st.button("✏️ Manual UPDATE"):
            update_customer(cursor)
            conn.commit()
            st.success("Row updated")

    with col3:
        if st.button("🗑️ Manual DELETE"):
            delete_customer(cursor)
            conn.commit()
            st.success("Row deleted")

    cursor.close()
    conn.close()

# -------------------------------------------------
# DATA VIEWER
# -------------------------------------------------

from db.query import fetch_all_customers
import pandas as pd
import streamlit as st 

with st.container(border=True):
    st.subheader("📄 Customers Table Viewer")

    if st.button("🔄 Refresh Data"):
        cols, rows = fetch_all_customers()
        df = pd.DataFrame(rows, columns=cols)
        st.dataframe(df, use_container_width=True)
