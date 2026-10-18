
# 🛡️ CodeShield — Secure Code Assessment

A Python-based static code security assessment tool developed for the CODSOFT Cyber Security Internship — Task 3.

## 📌 Project Overview

CodeShield analyzes Python source code to identify potential security vulnerabilities using Bandit. It presents findings through a Streamlit dashboard and supports JSON report downloads.

## ✨ Features

- Static security analysis of Python source files
- Vulnerability findings with severity levels
- Line numbers and security issue descriptions
- CWE references where available
- Interactive Streamlit dashboard
- Downloadable JSON scan reports
- Vulnerable and improved code examples
- Clear security findings summary

## 🧰 Technologies Used

- Python
- Bandit
- Streamlit

## 📂 Project Structure

```text
Secure_Code_Assessment/
├── app.py
├── scanner.py
├── requirements.txt
├── README.md
├── sample_vulnerable.py
└── sample_fixed.py
```

## ⚙️ Installation

1. Install Python 3.
2. Open the project folder in VS Code.
3. Open the integrated terminal.
4. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## ▶️ Run the Application

Start the CodeShield dashboard:

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## 🔍 How to Use

1. Open the CodeShield dashboard.
2. Upload a Python source file.
3. Start the security scan.
4. Review the findings and severity levels.
5. Examine the flagged code and recommendations.
6. Download the JSON report.

## 🧪 Testing

Two educational sample files are included:

- `sample_vulnerable.py` — demonstrates common security issues.
- `sample_fixed.py` — demonstrates safer coding approaches.

The vulnerable sample produced findings during testing, while the fixed sample produced zero findings in the observed scan.

## 🔐 Secure Coding Practices

- Avoid unsafe shell command execution.
- Use appropriate password hashing methods.
- Keep API keys and secrets outside source code.
- Review findings manually before fixing them.
- Test security improvements after changes.

## ⚠️ Limitations

CodeShield uses static analysis and cannot detect every possible vulnerability. A clean scan does not guarantee that an application is secure. Manual review and additional testing are recommended.

## 🎯 Internship Task

**CODSOFT Cyber Security Internship — Task 3: Secure Code Assessment**

The project demonstrates source-code review, vulnerability identification, secure coding recommendations, and security report generation.
