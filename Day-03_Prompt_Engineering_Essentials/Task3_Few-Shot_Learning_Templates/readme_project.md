## 📁 Project structure

```
python-dotenv-project/
│
├── README.md
├── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 📄 README.md

````md
# Python dotenv Example Project

This project shows how to use environment variables in Python using `python-dotenv`.

Environment variables help keep secrets (API keys, configs) out of source code.

---

## Requirements
- Python 3.8+
- pip

---

## Setup

### 1. Create virtual environment (optional)
```bash
python -m venv venv
````

Activate:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create `.env` file

Copy `.env.example` → `.env` and add your values.

---

## Run the project

```bash
python main.py
```

---

## Notes

* Never commit `.env` to Git
* Always load env vars using `load_dotenv()`

````

---

## 📄 main.py
```python
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("❌ OPENROUTER_API_KEY not found")

print("✅ API key loaded successfully")
````

---

## 📄 requirements.txt

```txt
python-dotenv
openai
```

---

## 📄 .env.example

```env
OPENROUTER_API_KEY=your_api_key_here
DEBUG=True
```

---

## 📄 .gitignore

```gitignore
.env
venv/
__pycache__/
```