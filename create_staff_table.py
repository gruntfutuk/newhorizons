import sqlite3
import logging

# Set up logging
logging.basicConfig(filename='employee_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to the employees database
conn_employees = sqlite3.connect('employees.db')
cursor_employees = conn_employees.cursor()

# Create a new database for staff
conn_staff = sqlite3.connect('staff.db')
cursor_staff = conn_staff.cursor()

# Create the staff table with an index field
cursor_staff.execute("""
CREATE TABLE staff (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
)
""")

# Insert unique employee names from employees.db into staff.db with a 4-digit index starting from 1001
cursor_employees.execute("SELECT DISTINCT name FROM employees")
employee_names = cursor_employees.fetchall()

for idx, (name,) in enumerate(employee_names, start=1001):
    cursor_staff.execute("INSERT INTO staff (id, name) VALUES (?, ?)", (idx, name))

conn_staff.commit()

# Close the connections
conn_employees.close()
conn_staff.close()

print("Staff database created.")
