DB Load Simulator

A small Streamlit application to generate database load using random
INSERT / UPDATE / DELETE operations and observe their impact.

This tool is mainly intended for:

* Testing CDC / transaction-log based monitoring
* Validating alerts on database changes
* Simulating real-world query activity

Features

* Random load simulation with configurable QPS and duration
* Manual INSERT / UPDATE / DELETE operations
* Live counters for executed operations
* Simple charts for activity visibility
* View full table data on demand
* Database-agnostic simulator design

Project Structure

DB_simulator/
│
├── app.py                  # Streamlit dashboard
│
├── engine/
│   └── simulator.py        # Core load simulation engine
│
├── db/
│   ├── connection.py       # DB connection logic
│   ├── schema.py           # Table creation
│   ├── operations.py       # Insert / Update / Delete queries
│   └── query.py            # Read queries
│
└── README.txt

Prerequisites

* Python 3.9+
* Streamlit
* A running database (PostgreSQL / SQL Server / others)
* Valid DB credentials in db/connection.py

Setup

1. Install dependencies:
   pip install streamlit pandas

2. Configure database connection:
   db/connection.py

3. Run the application:
   streamlit run app.py

How It Works (High Level)

* The simulator opens a database connection
* At a fixed rate (QPS), it randomly chooses:

  * INSERT
  * UPDATE
  * DELETE
* Each operation is executed and committed
* Counters track how many operations ran
* Streamlit displays metrics and charts

Notes

* Load simulation runs in a background thread
* Manual operations are executed independently
* All queries hit the real database
* Intended for testing and monitoring, not production use

Future Improvements (Optional)

* Auto-refresh dashboard
* Error metrics
* Multi-table simulation
* CDC lag visualization
