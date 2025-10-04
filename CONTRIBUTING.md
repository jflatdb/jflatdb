# 🤝 Contributing to jflatdb

Thank you for considering contributing to **jflatdb**! 🚀
We’re excited to welcome developers, testers, writers, and enthusiasts to help improve this lightweight JSON-based flat database.

This document provides guidelines, best practices, and steps to make contributing smooth and productive.

---

## 📋 Table of Contents

1. [Code of Conduct](#-code-of-conduct)
2. [How Can I Contribute?](#-how-can-i-contribute)

   * Reporting Bugs
   * Suggesting Features
   * Submitting Enhancements
   * Improving Documentation
3. [Development Setup](#-development-setup)
4. [Pull Request Guidelines](#-pull-request-guidelines)
5. [Commit Message Guidelines](#-commit-message-guidelines)
6. [Issue Guidelines](#-issue-guidelines)
7. [Style Guide](#-style-guide)
8. [Community](#-community)

---

## 📜 Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/).
By participating, you are expected to uphold this code.
Please report unacceptable behavior to **project maintainers**.

---

## 💡 How Can I Contribute?

### 🐞 Reporting Bugs

* Use the **Bug Report Template** when opening issues.
* Include steps to reproduce, expected vs actual behavior, logs, and screenshots if possible.
* Check for duplicate issues before opening a new one.

### ✨ Suggesting Features

* Open a **Feature Request** issue.
* Clearly describe the problem and why the feature is valuable.
* Suggest possible implementations (if any).

### 🛠 Submitting Enhancements

* Identify areas of performance, reliability, or usability that can be improved.
* Ensure changes do not break backward compatibility unless discussed.

### 📖 Improving Documentation

* Enhance `README.md`, `docs/`, or example scripts.
* Fix typos, clarify explanations, and add more examples.

---

## 🖥 Development Setup

1. Fork the repository.
2. Clone your fork:

   ```bash
   git clone https://github.com/jflatdb/jflatdb.git
   ```
3. Navigate into the project:

   ```bash
   cd jflatdb
   ```
4. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```
5. Install dependencies (if any).
6. Run tests before submitting changes:

   ```bash
   pytest
   ```

---

## 🔀 Pull Request Guidelines

* Keep PRs focused and atomic (one change per PR).
* Reference related issue numbers (e.g., `Fixes #42`).
* Ensure all tests pass.
* Add or update documentation if needed.
* PR title should be descriptive and follow [Conventional Commits](https://www.conventionalcommits.org/).

---

## 📝 Commit Message Guidelines

We follow the **Conventional Commits** format:

```
<type>(scope): short description

[optional body]
[optional footer(s)]
```

**Examples:**

* `feat(query): add DISTINCT function support`
* `fix(storage): handle empty dataset correctly`
* `docs: update contributing guide`

**Types:**

* `feat`: New feature
* `fix`: Bug fix
* `docs`: Documentation changes
* `style`: Code style (formatting, missing semicolons)
* `refactor`: Code refactoring (no feature or bug fix)
* `perf`: Performance improvement
* `test`: Adding or fixing tests
* `chore`: Maintenance tasks

---

## 🐛 Issue Guidelines

* Use the provided **issue templates** (`bug_report.md`, `feature_request.md`).
* Provide as much context as possible.
* If you want to work on an issue, please comment **“I’m working on this”** before sending a PR.

---

## 🎨 Style Guide

* Follow **PEP 8** for Python code.
* Use type hints wherever possible.
* Keep functions small and modular.
* Write docstrings for classes, functions, and modules.
* Use meaningful variable and function names.

---

## 🌍 Community

* Discussions happen in GitHub Issues and Discussions.
* Be respectful and constructive.
* Share ideas, feedback, and improvements openly.

---

💡 **Pro Tip:** Start by checking out issues labeled `good first issue` or `help wanted`.

We’re thrilled to see your contributions.
Thank you for making **jflatdb** better! 🙌
