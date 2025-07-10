import json
from .exceptions.errors import DatabaseError
from .database import Database

class CLI:
    def __init__(self, db: Database):
        self.db = db

    def run(self):
        print("✅ JSON Database CLI Ready. Type `.help` for commands.")
        while True:
            try:
                command = input(">> ").strip()
                if not command:
                    continue

                if command == ".exit":
                    print("Exiting...")
                    break

                elif command == ".help":
                    self.show_help()

                elif command.startswith(".insert"):
                    data = json.loads(command[len(".insert"):].strip())
                    self.db.insert(data)
                    print("Inserted.")

                elif command.startswith(".find"):
                    query = json.loads(command[len(".find"):].strip())
                    results = self.db.find(query)
                    print(f"Found {len(results)} record(s):")
                    for r in results:
                        print(r)

                elif command.startswith(".delete"):
                    query = json.loads(command[len(".delete"):].strip())
                    self.db.delete(query)
                    print("Deleted.")

                elif command.startswith(".update"):
                    parts = command[len(".update"):].strip().split("}", 1)
                    if len(parts) < 2:
                        print("Invalid update syntax.")
                        continue
                    query = json.loads(parts[0] + "}")
                    updates = json.loads(parts[1].strip())
                    self.db.update(query, updates)
                    print("Updated.")

                elif command.startswith(".min"):
                    column = command[len(".min"):].strip()
                    print("Min:", self.db.min(column))

                elif command.startswith(".max"):
                    column = command[len(".max"):].strip()
                    print("Max:", self.db.max(column))

                elif command.startswith(".avg"):
                    column = command[len(".avg"):].strip()
                    print("Average:", self.db.avg(column))

                elif command.startswith(".count"):
                    parts = command.split()
                    column = parts[1] if len(parts) > 1 else None
                    print("Count:", self.db.count(column))

                elif command.startswith(".between"):
                    _, col, low, high = command.split()
                    results = self.db.between(col, int(low), int(high))
                    for r in results:
                        print(r)

                elif command.startswith(".group_by"):
                    column = command[len(".group_by"):].strip()
                    result = self.db.group_by(column)
                    for key, group in result.items():
                        print(f"{key}: {group}")

                else:
                    print("❌ Unknown command. Use `.help` for available commands.")

            except json.JSONDecodeError:
                print("❌ Invalid JSON format.")
            except DatabaseError as e:
                print(f"❌ Database Error: {str(e)}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

    def show_help(self):
        print("""
================= JSON Database CLI Help =================

  .help                              → Show this help menu
  .exit                              → Exit the program

  # Data Commands
  .insert <json>                     → Insert record
  .find <json>                       → Find matching records
  .update <query> <updates>         → Update record(s)
  .delete <query>                   → Delete record(s)

  # Built-in Functions
  .min <column>                     → Get minimum value
  .max <column>                     → Get maximum value
  .avg <column>                     → Get average value
  .count [<column>]                 → Count entries
  .between <column> <min> <max>     → Filter range
  .group_by <column>                → Group records

===========================================================
""")
