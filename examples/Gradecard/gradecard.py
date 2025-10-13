"""
STUDENT GRADEBOOK — using jflatdb

This mini-project demonstrates how to use jflatdb for storing and managing
student records (name, subject, marks), and calculating averages.

In this tutorial, you'll learn how to:
1. Initialize a jflatdb database with encryption support.
2. Add student records.
3. View all records.
4. Search for a student by name.
5. Calculate the class average.
6. Build a simple command-line interface (CLI) for interaction.

Prerequisites:
- The jflatdb package must be available in the root directory of your repository.
- Python 3.8+ installed on your system.
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
Step 3: Initialize the gradebook database with a password.
The database file will be created in the same folder as this script.
"""
db = Database("grades.json", password="mysecurepass")

"""
Step 4: Define a function to insert new student records.
Each record contains the student's name, subject, and marks.
"""
def add_record(name, subject, marks):
    db.insert({"name": name, "subject": subject, "marks": marks})
    print(f"Record for '{name}' added.")

"""
Step 5: Define a function to view all student records.
"""
def view_all():
    print("\nAll Student Records:")
    records = db.all()
    if not records:
        print("No records found.")
        return
    for rec in records:
        print(f"{rec['name']} - {rec['subject']}: {rec['marks']} marks")

"""
Step 6: Define a function to search for a student by name.
"""
def search_student(name):
    results = db.search(lambda x: x['name'].lower() == name.lower())
    if results:
        print(f"\nRecords for {name}:")
        for r in results:
            print(f"{r['subject']} - {r['marks']} marks")
    else:
        print("Student not found.")

"""
Step 7: Define a function to calculate and display the class average.
"""
def average_marks():
    records = db.all()
    if not records:
        print("No records found.")
        return
    avg = sum(r["marks"] for r in records) / len(records)
    print(f"\nClass Average Marks: {avg:.2f}")

"""
Step 8: Build a simple CLI (Command-Line Interface).
"""
if __name__ == "__main__":
    while True:
        print("\n=== STUDENT GRADEBOOK ===")
        print("1. Add Record")
        print("2. View All Records")
        print("3. Search Student")
        print("4. Show Class Average")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Student Name: ")
            subject = input("Subject: ")
            marks = float(input("Marks: "))
            add_record(name, subject, marks)
        elif choice == "2":
            view_all()
        elif choice == "3":
            search_student(input("Enter student name: "))
        elif choice == "4":
            average_marks()
        elif choice == "5":
            print("Exiting Gradebook.")
            break
        else:
            print("Invalid choice, try again.")
