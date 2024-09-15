import sqlite3
import logging

# Set up logging
logging.basicConfig(filename='employee_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to the employees database
conn_employees = sqlite3.connect('employees.db')
cursor_employees = conn_employees.cursor()

# Attach the events database
cursor_employees.execute("ATTACH DATABASE 'events.db' AS events_db")

# Attach the staff database
cursor_employees.execute("ATTACH DATABASE 'staff.db' AS staff_db")

# Find employee names in events.db that do not exist in employees.db
cursor_employees.execute("""
SELECT events_db.events.name
FROM events_db.events
LEFT JOIN employees ON events_db.events.name = employees.name
WHERE employees.name IS NULL
""")
missing_employees = cursor_employees.fetchall()

# Log error messages for missing employees
if missing_employees:
    for employee in missing_employees:
        logging.error(f"Employee '{employee[0]}' found in events.db but not in employees.db")

# Update the points field in employees table
update_query = """
UPDATE employees
SET points = points + (
    SELECT events_db.events.points
    FROM events_db.events
    WHERE employees.name = events_db.events.name
)
WHERE EXISTS (
    SELECT 1
    FROM events_db.events
    WHERE employees.name = events_db.events.name
)
"""

cursor_employees.execute(update_query)
conn_employees.commit()

# Replace name field with staff_number in employees table
cursor_employees.execute("ALTER TABLE employees ADD COLUMN staff_number INTEGER")
cursor_employees.execute("""
UPDATE employees
SET staff_number = (
    SELECT COALESCE(staff_db.staff.id, 999)
    FROM staff_db.staff
    WHERE staff_db.staff.name = employees.name
)
""")
cursor_employees.execute("ALTER TABLE employees DROP COLUMN name")

# Replace name field with staff_number in events table
cursor_employees.execute("ALTER TABLE events_db.events ADD COLUMN staff_number INTEGER")
cursor_employees.execute("""
UPDATE events_db.events
SET staff_number = (
    SELECT COALESCE(staff_db.staff.id, 999)
    FROM staff_db.staff
    WHERE staff_db.staff.name = events_db.events.name
)
""")
cursor_employees.execute("ALTER TABLE events_db.events DROP COLUMN name")

conn_employees.commit()

# Detach the events and staff databases
cursor_employees.execute("DETACH DATABASE events_db")
cursor_employees.execute("DETACH DATABASE staff_db")

# Close the connection
conn_employees.close()

print("Points updated and staff_number fields added successfully.")
