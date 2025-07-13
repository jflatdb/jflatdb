
# 🛠️ Contributing Guide for jflatdb

Thank you for considering contributing to **jflatdb** — a simple, powerful flat-file database framework for Python.  
We welcome all types of contributions: bug reports, feature ideas, code, tests, documentation, and more.

> 🔰 New to open source? We love beginners! This guide will walk you through everything.

---

## 📑 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [How to Contribute](#-how-to-contribute)
- [Project Structure](#-project-structure)
- [Branching & Commit Style](#-branching--commit-style)
- [Testing & Linting](#-testing--linting)
- [Pull Request Checklist](#-pull-request-checklist)
- [Contribution Types](#-contribution-types)
- [Need Help?](#-need-help)

---

## 💬 Code of Conduct

By contributing, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).  
We aim to foster an open and welcoming environment for all.

---

## ⚙️ Getting Started

### 1. Fork the Repository

Click the **Fork** button on [jflatdb GitHub](https://github.com/jflatdb/jflatdb) and clone your fork:

```bash
git clone https://github.com/jflatdb/jflatdb.git
cd jflatdb
```

### 2. Run Tests
```bash
pytest
```

## 🚀 How to Contribute
Here are some ways you can help:
| Contribution Type  | Description                                              |
| ------------------ | -------------------------------------------------------- |
| 🐞 Bug Report      | Found a bug? File a GitHub issue with reproduction steps |
| 💡 Feature Request | Suggest an improvement or enhancement                    |
| 📄 Documentation   | Improve docs, examples, or tutorials                     |
| 👨‍💻 Code         | Add a new feature or fix a bug                           |
| 🧪 Tests           | Add or improve test coverage                             |

## 🌱 Branching & Commit Style
### 📌 Branch Naming Convention:
```bash
feature/<feature-name>
bugfix/<bug-description>
docs/<doc-update>
refactor/<refactor-description>
```

### ✅ Commit Message Convention:
Follow this structure:
```bash
type(scope): short description
```

#### Examples:
- feat(core): add insert method with filters
- fix(utils): handle empty file on load
- docs(readme): update usage example

Valid type values: feat, fix, docs, refactor, test, style, chore
Use [Conventional Commits]() for consistency.

## 🧪 Testing & Linting
Before submitting a pull request, ensure:

### ✅ Tests Pass
```bash
pytest
```

### ✅ Linting is Clean
```bash
flake8 jflatdb/
```
We recommend using [Black]() for consistent formatting.
```bash
black jflatdb/
```

## 📥 Pull Request Checklist
Before you open a pull request:

- [ ] Code is clean and follows PEP8

- [ ] Linting passes (flake8)

- [ ] Tests are added/updated

- [ ] Code is documented with comments and docstrings

- [ ] Your PR is linked to a GitHub issue if relevant

- [ ] You followed the commit and branch naming convention


## 📘 Contrubution Types
| Type          | Tag         | Description                               |
| ------------- | ----------- | ----------------------------------------- |
| New Feature   | `feat:`     | New capability added                      |
| Bug Fix       | `fix:`      | A bug has been fixed                      |
| Documentation | `docs:`     | Documentation changes                     |
| Refactor      | `refactor:` | Code restructure (no new feature/bug fix) |
| Test          | `test:`     | Adding tests                              |
| Chore         | `chore:`    | Maintenance tasks                         |
| Style         | `style:`    | Code formatting, white-space, etc.        |

.

## 🤝 Need Help?
If you're stuck or unsure:

- [Open a GitHub Discussion]()
- [Open an Issue]()

Tag your issue with help wanted or good first issue

## 🙌 Thank You
Thanks for being awesome 💙 Your time and effort make jflatdb better for everyone.
We welcome you to the contributor family!

– The Akki Maintainers
