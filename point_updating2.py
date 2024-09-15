import sqlite3
import logging

# Set up logging
logging.basicConfig(filename='employee_errors.log', level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to the employees database
conn_employees = sqlite3.connect('employees.db')
cursor_employees = conn_employees.cursor()

# Attach the events and staff databases
cursor_employees.execute("ATTACH DATABASE 'events.db' AS events_db")
cursor_employees.execute("ATTACH DATABASE 'staff.db' AS staff_db")

# Find invalid staff_numbers in events table
cursor_employees.execute("""
SELECT events_db.events.staff_number
FROM events_db.events
LEFT JOIN staff_db.staff ON events_db.events.staff_number = staff_db.staff.id
WHERE staff_db.staff.id IS NULL
""")
invalid_staff_numbers = cursor_employees.fetchall()

# Log warning messages for invalid staff_numbers
if invalid_staff_numbers:
    for staff_number in invalid_staff_numbers:
        logging.warning(f"Invalid staff_number '{staff_number[0]}' found in events.db")

# Update the points field in employees table
update_query = """
UPDATE employees
SET points = points + (
    SELECT events_db.events.points
    FROM events_db.events
    JOIN staff_db.staff ON events_db.events.staff_number = staff_db.staff.id
    WHERE employees.staff_number = events_db.events.staff_number
)
WHERE EXISTS (
    SELECT 1
    FROM events_db.events
    JOIN staff_db.staff ON events_db.events.staff_number = staff_db.staff.id
    WHERE employees.staff_number = events_db.events.staff_number
)
"""

cursor_employees.execute(update_query)
conn_employees.commit()

# Detach the events and staff databases
cursor_employees.execute("DETACH DATABASE events_db")
cursor_employees.execute("DETACH DATABASE staff_db")

# Close the connection
conn_employees.close()

print("Points updated successfully.")
