<p align="center">
  <img src="https://github.com/jflatdb/jflatdb/raw/main/assets/logo/logo.png" width="200" alt="JFlatDB Logo" />
</p>

# jflatdb

**jflatdb** is a lightweight, Python-based flat-file database framework designed for fast, simple, and file-based data storage without the need for a server or SQL engine. Ideal for developers building CLI tools, microservices, or offline applications.

![License](https://img.shields.io/github/license/jflatdb/jflatdb)
![Contributors](https://img.shields.io/github/contributors/jflatdb/jflatdb)
![Issues](https://img.shields.io/github/issues/jflatdb/jflatdb)
![Stars](https://img.shields.io/github/stars/jflatdb/jflatdb)

---

## 🚀 Features

- 📁 Flat-file, schema-free database
- 🧪 Easy read/write/query interface
- 📦 No server or setup needed
- 🔐 Human-readable, JSON-style structure
- 🧩 Modular and extensible

---

## 📦 Installation

```bash
pip install jflatdb
```

or from source 

```bash
git clone https://github.com/jflatdb/jflatdb.git
cd jflatdb
pip install .
````

## Usage

```bash 
from jflatdb.database import Database

db = Database("users.json", password="your-password")

# Create or insert data
db.insert({"name": "Akki", "email": "akki@example.com"})

# Find records
users = db.find({"name": "Akki"})

# Advanced queries with operators
# Greater than, less than, etc.
young_users = db.find({"age": {"$gt": 18, "$lt": 30}})
# IN operator
specific_ids = db.find({"id": {"$in": [1, 2, 3]}})
# LIKE for pattern matching
names_starting_with_a = db.find({"name": {"$like": "A%"}})
# BETWEEN
ages_in_range = db.find({"age": {"$between": [20, 30]}})

# Update records
db.update({"name": "Akki"}, {"email": "new@email.com"})

# Delete records
db.delete({"name": "Akki"})

# Aggregate functions
from jflatdb.query_engine import QueryEngine

# Sample data
data = [
    {"id": 1, "name": "Alice", "salary": 3000},
    {"id": 2, "name": "Bob", "salary": 4000},
    {"id": 3, "name": "Charlie", "salary": 2500}
]

engine = QueryEngine(data)

# Calculate sum
total_salary = engine.sum("salary")  # 9500

# Calculate average
avg_salary = engine.avg("salary")  # 3166.67

# Find minimum
min_salary = engine.min("salary")  # 2500

# Find maximum
max_salary = engine.max("salary")  # 4000

# Count records
total_records = engine.count()  # 3
records_with_salary = engine.count("salary")  # 3

# Filter values between range
mid_salaries = engine.between("salary", 2500, 3500)
# [{"id": 1, "name": "Alice", "salary": 3000}, {"id": 3, "name": "Charlie", "salary": 2500}]

# Group by column
grouped = engine.group_by("department")
```

## 📁 Project Structure

```bash 
jflatdb/
├── jflatdb/
│   ├── __init__.py
│   ├── database.py
│   ├── query_engine.py
│   └── indexing.py
|    ├── scheme.py
├── tests/
├── examples/
├── setup.py
├── README.md
└── LICENSE
```

## 🤝 Contributing
We welcome contributions from the community!

To get started:

Fork the repo

Create a new branch: ```git checkout -b feature-name```

Make your changes and commit: ```git commit -m 'Add feature'```

Push to your branch: ```git push origin feature-name```

Open a Pull Request

Please read our CONTRIBUTING.md for full guidelines.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 💬 Join the Community
- [Submit an Issue](https://github.com/jflatdb/jflatdb/issues)

- [Start a Discussion](https://github.com/jflatdb/jflatdb/discussion/)

- [Suggest a Feature](https://github.com/jflatdb/jflatdb.github/)

---
## 🙌 Credits
Developed and maintained by ```Akki```.

---

## 🙏 Support & Contributions

Your contributions make this project better — whether it's reporting a bug, suggesting a feature, improving the documentation, or writing code. We welcome developers of all levels to participate!

If you like this project, consider ⭐ starring it and sharing it with others.  
Together, let’s build something awesome with `jflatdb`.

Happy coding! 🚀
