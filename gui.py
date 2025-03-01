import tkinter as tk
from tkinter import messagebox, ttk
from database import create_table, add_contact, edit_contact, delete_contact, search_contacts, create_connection

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Contact Manager")
        create_table()
        
        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Entry fields for contact details
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        tk.Label(self.root, text="Name").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(self.root, text="Phone").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.phone_var).grid(row=1, column=1)

        tk.Label(self.root, text="Email").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.email_var).grid(row=2, column=1)

        # Buttons for actions
        tk.Button(self.root, text="Add Contact", command=self.add_contact).grid(row=3, column=0)
        tk.Button(self.root, text="Edit Contact", command=self.edit_contact).grid(row=3, column=1)
        tk.Button(self.root, text="Delete Contact", command=self.delete_contact).grid(row=3, column=2)

        # Search functionality
        self.search_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.search_var).grid(row=4, column=0)
        tk.Button(self.root, text="Search", command=self.search_contacts).grid(row=4, column=1)

        # Treeview for displaying contacts
        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone", "Email"), show='headings')
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.grid(row=5, column=0, columnspan=3)

    def add_contact(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()

        # Basic validation (optional)
        if not name or not phone or not email:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        # Add contact to the database
        add_contact(name, phone, email)

        # Clear the entry fields after adding
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")

        # Refresh the contact list
        self.refresh_contacts()

    def edit_contact(self):
        selected_item = self.tree.selection()[0]
        contact_id = self.tree.item(selected_item, 'text')
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        edit_contact(contact_id, name, phone, email)
        self.refresh_contacts()

    def delete_contact(self):
        selected_item = self.tree.selection()[0]
        contact_id = self.tree.item(selected_item, 'text')
        delete_contact(contact_id)
        self.refresh_contacts()

    def search_contacts(self):
        query = self.search_var.get()
        results = search_contacts(query)
        self.update_treeview(results)

    def refresh_contacts(self):
        # Clear the current contacts in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch all contacts from the database
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        contacts = cursor.fetchall()
        conn.close()

        # Insert contacts into the Treeview
        for contact in contacts:
            self.tree.insert('', 'end', text=contact[0], values=(contact[1], contact[2], contact[3]))

    def update_treeview(self, contacts):
        # Clear the treeview and insert new contacts
        pass  # Implement updating the treeview with new contacts

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop() 