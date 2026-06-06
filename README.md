# 🎓 iTeach — School Management System

A simple school management system built with Python. Comes in two versions: a command-line interface (`main.py`) and a polished web UI built with Streamlit (`app.py`).

---

## 📋 Features

- Register students with name, age, email, parent email, and roll number
- Register teachers with name, age, email, employee ID, and subject
- Add and update subject-wise grades for students
- View student profiles with average score and grade badge
- View teacher profiles
- See all students and teachers in a sortable table
- Data is persisted locally in a JSON file (`school_data.json`)

---

## 🗂️ Project Structure

```
├── main.py             # CLI version (OOP with abstract base classes)
├── app.py              # Streamlit web UI version
└── school_data.json    # Local JSON database (auto-created)
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install streamlit pandas
```

### Run the Web App

```bash
streamlit run app.py
```

### Run the CLI Version

```bash
python main.py
```

---

## 🛠️ Tech Stack

- **Python 3**
- **Streamlit** — web UI
- **JSON** — local data storage
- **OOP / ABC** — abstract base classes for `Person`, `Student`, `Teacher`

---

## 📌 Notes

- Data is stored in `school_data.json` in the same directory
- Roll numbers and Employee IDs must be unique
- Basic email validation is included
