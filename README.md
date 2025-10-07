<p align="center">
  <img src="https://github.com/jflatdb/jflatdb/raw/main/assets/logo/logo.png" width="200" alt="JFlatDB Logo" />
</p>

<h1 align="center">jflatdb</h1>

<p align="center">
  <b>The next-gen lightweight JSON database for Python — fast, secure, and schema-aware.</b><br>
  Store and query data instantly with zero setup, pure Python power, and human-readable JSON files.
</p>

<p align="center">
  <a href="https://github.com/jflatdb/jflatdb/blob/main/LICENSE"><img src="https://img.shields.io/github/license/jflatdb/jflatdb" alt="License"></a>
  <a href="https://github.com/jflatdb/jflatdb/graphs/contributors"><img src="https://img.shields.io/github/contributors/jflatdb/jflatdb" alt="Contributors"></a>
  <a href="https://github.com/jflatdb/jflatdb/issues"><img src="https://img.shields.io/github/issues/jflatdb/jflatdb" alt="Issues"></a>
  <a href="https://github.com/jflatdb/jflatdb/stargazers"><img src="https://img.shields.io/github/stars/jflatdb/jflatdb" alt="Stars"></a>
  <a href="https://pypi.org/project/jflatdb/"><img src="https://img.shields.io/pypi/dm/jflatdb" alt="Downloads"></a>
  <a href="https://hacktoberfest.com/"><img src="https://img.shields.io/badge/Hacktoberfest-2025-blueviolet" alt="Hacktoberfest"></a>
</p>

---

## 📚 Table of Contents

* [Features](#-features)
* [Installation](#-installation)
* [Quick Start](#-quick-start)
* [Usage Examples](#-usage-examples)
* [Project Structure](#-project-structure)
* [Contributing](#-contributing)
* [License](#-license)
* [Community](#-join-the-community)
* [Credits](#-credits)
* [Support](#-support--contributions)

---

## 🚀 Overview

**jflatdb** is a **file-based, schema-aware JSON database system** that combines the simplicity of NoSQL with **powerful query and indexing features** inspired by SQL — all in pure Python.

No servers.
No setup.
Just plug, code, and store.

Perfect for developers, students, or small apps that need fast, secure, local data storage with minimal dependencies.

---

## ⚡ Features

* 🧩 **Flat-File Simplicity** – Store data in plain JSON files
* ⚙️ **Persistent Indexing** – Fast queries, no rebuild on load
* 🔍 **Powerful Query Engine** – `$gt`, `$lt`, `$in`, `$like`, `$between`, and more
* 🔒 **Encryption & Validation** – Optional AES encryption and schema constraints
* 🧠 **Async & Transactions** – Atomic commits, async-safe operations
* 🛠 **Zero Dependencies** – 100% pure Python
* 💡 **Extensible Design** – Add plugins, custom storages, or new data types

---

## 📦 Installation

```bash
pip install jflatdb
```

or install from source:

```bash
git clone https://github.com/jflatdb/jflatdb.git
cd jflatdb
pip install .
```

---

## ⚡ Quick Start

```python
from jflatdb.database import Database

# Initialize with optional encryption
db = Database("users.json", password="your-password")

# Insert data
db.insert({"name": "Akki", "email": "akki@example.com", "age": 25})

# Query with conditions
users = db.find({"age": {"$gt": 18, "$lt": 30}})
print(users)

# Update and Delete
db.update({"name": "Akki"}, {"email": "new@email.com"})
db.delete({"name": "Akki"})
```

---

## 📁 Project Structure

```bash
jflatdb/
├── jflatdb/
│   ├── __init__.py
│   ├── database.py
│   ├── query_engine.py
│   ├── indexing.py
│   ├── schema.py
│   └── security.py
├── examples/
├── tests/
├── README.md
├── setup.py
└── LICENSE
```

---

## 🎉 Contributors Leaderboard

<!-- readme: contributors -start -->

<!-- readme: contributors -end -->

---

## 🤝 Contributing

We welcome all contributions!
To get started:

1. **Fork** the repository
2. Create a new branch → `git checkout -b feature-name`
3. Commit your changes → `git commit -m "Add feature"`
4. Push your branch → `git push origin feature-name`
5. Open a Pull Request

Check our [CONTRIBUTING.md](https://github.com/jflatdb/jflatdb/blob/main/CONTRIBUTING.md) for more details.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](https://github.com/jflatdb/jflatdb/blob/main/LICENSE) file for details.

---

## 💬 Join the Community

* 💡 [Suggest a Feature](https://github.com/jflatdb/jflatdb/issues/new?labels=enhancement)
* 🐞 [Report a Bug](https://github.com/jflatdb/jflatdb/issues/new?labels=bug)
* 💬 [Start a Discussion](https://github.com/jflatdb/jflatdb/discussions)

---

## 🙌 Credits

Developed and maintained by **Akki**
Inspired by TinyDB, SQLite, and the open-source spirit.

---

## 🙏 Support & Contributions

Your support keeps this project growing! 🌱
If you like **jflatdb**, please ⭐ **star the repo**, share it, and help more developers discover it.

> Let’s redefine simple data storage — one JSON file at a time. 💾🚀

