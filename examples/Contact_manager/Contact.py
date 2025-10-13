"""
CONTACT MANAGER — using jflatdb

This mini-project demonstrates how to use jflatdb as a lightweight local JSON database
to store and manage contact information.

In this tutorial, you'll learn how to:
1. Initialize a jflatdb database with encryption support.
2. Add, view, search, and delete contacts.
3. Build a simple command-line interface (CLI) for interaction.

Prerequisites:
- The jflatdb package must be available in the root directory of your repository.
- Python 3.8+ installed on your system.

Let's begin!
"""

import sys
import os

"""
Step 1: Add the repository root to the Python path.
This allows Python to find and import the local jflatdb package.
"""
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

"""
Step 2: Import the Database class from jflatdb.
"""
from jflatdb.database import Database

"""
Step 3: Initialize the local database file with a password.
The database file will be created in the same folder as this script.
The password secures your stored JSON data.
"""
db = Database("contacts.json", password="mysecurepass")

"""
Step 4: Define a function to insert new contact records.
Each contact is stored as a JSON object with name, phone, and email fields.
"""
def add_contact(name, phone, email):
    db.insert({"name": name, "phone": phone, "email": email})
    print(f"Contact '{name}' added successfully!")

"""
Step 5: Define a function to view all saved contacts.
This retrieves all entries stored in the local database.
"""
def view_contacts():
    print("\nAll Contacts:")
    contacts = db.all()
    if not contacts:
        print("No contacts found.")
        return
    for contact in contacts:
        print(f"- {contact['name']} | {contact['phone']} | {contact['email']}")

"""
Step 6: Define a function to search for a contact by name.
The search is case-insensitive and uses a lambda filter.
"""
def search_contact(name):
    results = db.search(lambda x: x['name'].lower() == name.lower())
    if results:
        print(f"\nFound Contact: {results[0]}")
    else:
        print("No contact found with that name.")

"""
Step 7: Define a function to delete a contact by name.
If a record matches, it will be permanently removed from the database.
"""
def delete_contact(name):
    deleted = db.delete(lambda x: x['name'].lower() == name.lower())
    if deleted:
        print(f"Contact '{name}' deleted.")
    else:
        print("Contact not found.")

"""
Step 8: Build a simple CLI (Command-Line Interface).
This menu allows you to interact with the database through the terminal.
"""
if __name__ == "__main__":
    while True:
        print("\n=== CONTACT MANAGER ===")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Delete Contact")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            add_contact(name, phone, email)
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact(input("Enter name to search: "))
        elif choice == "4":
            delete_contact(input("Enter name to delete: "))
        elif choice == "5":
            print("Exiting Contact Manager.")
            break
        else:
            print("Invalid choice, try again.")
