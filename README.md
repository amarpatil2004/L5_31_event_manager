# Lab 5: Static Code Analysis — Event Management System

**Student Name:** Amar Patil  
**SRN:** PES1UG24AM031  
**Course:** Software Engineering (PES University)  
**Assigned File:** `event_manager.py`  

---

## About the Program

A booking desk for small events. It creates events with a venue and capacity, registers guests until an event is full, reports seats left, picks a lucky-draw winner, labels events as upcoming or completed, and persists event data safely to `events.json`.

The original codebase had critical quality, style, logic, and security problems flagged by **Pylint**, **Flake8**, and **Bandit**. All identified issues have been systematically resolved and documented.

---

## Static Code Analysis Summary

| Tool | Before Fixes | After Fixes | Status |
|---|---|---|---|
| **Pylint** | 4.64 / 10 | **10.00 / 10** | Passed (Exceeds > 9.5 target) |
| **Bandit** | 4 issues (1 High, 1 Medium, 2 Low) | **0 issues** | Passed (100% clean) |
| **Flake8** | 4 style & whitespace violations | **0 violations** | Passed (100% PEP 8 compliant) |

---

## Project Structure & Deliverables

- `event_manager.py`: Cleaned and optimized version with all security, logic, docstring, naming, and style issues fixed.
- `issues.md`: Completed issue documentation table (8 issues documented in detail) and `#nosec` justifications.
- `reflection.md`: In-depth reflection addressing learning outcomes, critical bugs, tool roles, and engineering takeaways.
- `pylint_report_before.txt` & `pylint_report.txt`: Pylint reports before (4.64/10) and after (10.00/10).
- `bandit_report_before.txt` & `bandit_report.txt`: Bandit reports before (4 findings) and after (0 findings).
- `flake8_report_before.txt` & `flake8_report.txt`: Flake8 reports before (4 violations) and after (clean).

---

## Running the Project & Analysis

### 1. Run the Python Script
```bash
python event_manager.py
```

### 2. Run Static Analysis Tools
```bash
python -m pylint event_manager.py
python -m bandit -r event_manager.py
python -m flake8 event_manager.py
```
