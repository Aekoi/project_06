import sqlite3
from tkinter import messagebox

# Add all of the necessary imports


class EmployeeManager:
    def __init__(self, db_file):
        # Connect to the SQLite database
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        # Create the 'employees' table if it doesn't exist
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, pass_code TEXT)"
        )

        # Commit the changes to the database
        self.conn.commit()

    def employee_exists(self, email, pass_code):
        self.cursor.execute(
            "SELECT * FROM clients WHERE email = ? OR pass_code = ?",
            (email, pass_code),
        )
        return self.cursor.fetchone() is not None

    def add_employee(self, name, email, pass_code):
        # Insert a new employee into the 'employees' table
        
        if self.client_exists(email, pass_code):
            messagebox.showerror("Ο υπάλληλος υπάρχει ήδη", "Παρακαλώ δοκιμάστε ξανά.")
            return
            
        self.cursor.execute(
            "INSERT INTO employees (name, email, pass_code) VALUES (?, ?, ?)",
            (name, email, pass_code),
        )
        messagebox.showinfo("Καταχώρηση", "Ο υπάλληλος καταχωρήθηκε επιτυχώς")
            
        # Commit the changes to the database
        self.conn.commit()

    def delete_employee(self, id):
        # Delete an employee from the 'employees' table based on the employee ID
        self.cursor.execute("DELETE FROM employees WHERE id=?", (id,))

    def delete_client(self, id):
        confirmation = messagebox.askquestion("Επιβεβαίωση Διαγραφής", "Είστε βέβαιος ότι θέλετε να διαγράψετε τον υπάλληλο;")
        if confirmation == "yes":
            self.cursor.execute("DELETE FROM clients WHERE id=?", (id,))
            self.conn.commit()
            messagebox.showinfo("Διαγραφή Υπαλλήλου", "Ο υπάλληλος διαγράφηκε επιτυχώς.")
        else:
            messagebox.showinfo("Ακύρωση Διαγραφής", "Η διαγραφή του υπαλλήλου ακυρώθηκε.")

        # Commit the changes to the database
        self.conn.commit()

    def search_employee(self, search_term):
        # Search for employees in the 'employees' table based on a search term
        self.cursor.execute(
            "SELECT * FROM employees WHERE name LIKE ? OR email LIKE ? OR pass_code LIKE ?",
            (
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
            ),
        )

        # Return the fetched employees
        return self.cursor.fetchall()

    def update_employee(self, name=None, email=None, pass_code=None):
        # Update an employee's information in the 'employees' table
        updates = {}
        if name:
            updates["name"] = name
        if email:
            updates["email"] = email
        if pass_code:
            updates["pass_code"] = pass_code
        update_query = ", ".join([f"{key}=?" for key in updates.keys()])
        update_values = tuple(updates.values()) + (id,)
        self.cursor.execute(
            f"UPDATE employee SET {update_query} WHERE id=?", update_values
        )
        messagebox.showinfo("Τροποποίηση", "Η τροποποίηση ολοκληρώθηκε επιτυχώς")
        # Commit the changes to the database
        self.conn.commit()

    def get_id_from_name(self, name):
        self.cursor.execute(f"SELECT id FROM employees WHERE name LIKE '{name}'")
        return self.cursor.fetchall()[0]

    def get_all_employees(self):
        # Retrieve all employees from the 'employees' table
        self.cursor.execute("SELECT * FROM employees")

        # Return the fetched employees
        return self.cursor.fetchall()

    def get_employee(self, employee_id):
        # Retrieve an employee from the 'employees' table based on the employee ID
        query = "SELECT * FROM employees WHERE id = ?"
        self.cursor.execute(query, str(employee_id))

        # Return the fetched employee
        return self.cursor.fetchone()

    def __del__(self):
        # Close the database connection when the object is deleted
        self.conn.close()
