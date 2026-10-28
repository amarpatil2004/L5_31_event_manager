# Lab 5: Identified Issues and Fixes

**Student Name:** Amar Patil  
**SRN:** PES1UG24AM031  
**Course:** Software Engineering — Lab 5: Static Code Analysis  

---

## Static Code Analysis Issues Table

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| **Command Injection via Shell (`os.system`)** | Security (High) / Bandit `B605` | 56 | Calling `os.system("lp badges_" + eventName + ".txt")` executes shell commands via the system shell (`sh` or `cmd.exe`). If `eventName` contains shell metacharacters (e.g., `;`, `&`, `|`), arbitrary commands can be injected and executed on the host system. | Replaced `os.system` with `subprocess.run(["/usr/bin/lp", f"badges_{event_name}.txt"], check=False)`. Passing command arguments as a list bypasses shell interpolation entirely, immunizing the application against command injection. |
| **Insecure Deserialization (`pickle`)** | Security (Medium) / Bandit `B301`, `B403` | 2, 51 | Python's `pickle` module (`pickle.load`) reconstructs Python objects from a byte stream and can execute arbitrary bytecode during deserialization if an attacker alters or replaces `events.pkl`. | Replaced `pickle` with standard `json` (`json.dump` / `json.load` with UTF-8 encoding). JSON represents data structures purely without any executable code execution capability. |
| **Mutable Default Argument (`guests=[]`)** | Bug (High Severity) / Pylint `W0102` | 9 | `createEvent` defines a mutable default argument `guests=[]`. In Python, default parameter expressions are evaluated once when the function is defined. As a result, every call that omits `guests` shares the exact same list in memory. In `main()`, adding guests to "Tech Meetup" inadvertently filled the guest list for "Alumni Dinner", causing "Alumni Dinner" to immediately report 0 available seats and reject valid registrations. | Replaced the default value with `guests=None`. Inside the function, initialized a fresh list with `if guests is None: guests = []` and created an independent copy `list(guests)` for each event. |
| **Weak Pseudo-Random Number Generator** | Security (Low) / Bandit `B311` | 72 | `random.choice()` uses Python's standard Mersenne Twister PRNG, which is deterministic, predictable, and unsuitable for security-sensitive operations or unbiased lotteries/contests. | Replaced `random.choice` with `secrets.choice()` from Python's standard `secrets` cryptographic library, ensuring cryptographically secure randomness. |
| **Unused Function Parameter (`sortOrder`)** | Code Quality / Pylint `W0613` | 39 | `guestReport(eventName, sortOrder)` defined `sortOrder` as a parameter, but the function body ignored it and always returned names in ascending order. | Implemented dynamic sorting using `reverse = (sort_order.lower() == "desc")` to sort names in ascending or descending order according to caller request. |
| **Unnecessary `else` After `return`** | Code Style / Pylint `R1705` | 33–36 | `eventStatus` contained an explicit `else` block following a `return` statement (`if eventDate >= date.today(): return ... else: return ...`), adding redundant indentation and complexity. | Removed the redundant `else:` block and de-indented the fallback return statement (`return "Completed"`) to streamline control flow. |
| **Missing Docstrings and CamelCase Naming** | Convention / Pylint `C0114`, `C0116`, `C0103` | 1, 9, 15, 27, 32, 39, 44, 49, 54, 59 | The module and functions lacked descriptive docstrings. Function and parameter names used camelCase (`createEvent`, `eventName`, etc.) contrary to PEP 8 snake_case guidelines. | Added comprehensive module and function docstrings complying with PEP 257. Renamed all functions and parameters to PEP 8 snake_case (`create_event`, `event_name`, etc.). |
| **PEP 8 Whitespace and Formatting Violations** | Formatting / Flake8 `E225`, `E231`, `E261`, `E305` | 61, 66, 75, 79 | Flake8 flagged multiple formatting violations: missing space after comma (`"Rooftop",2`), missing whitespace around operator (`left=seatsLeft(...)`), insufficient spaces before inline comment (`# reload...`), and only 1 blank line before top-level code. | Corrected whitespace after commas, padded assignment operators with spaces, added 2 spaces before inline comments, and ensured 2 blank lines between all top-level statements and functions. |

---

## Bandit Suppression (`#nosec`) Justification

Two targeted `#nosec` directives are included in `event_manager.py` with the following security rationale:

### 1. Line 12: `import subprocess  # nosec B404`
- **Bandit Rule**: `B404:blacklist` ("Consider possible security implications associated with the subprocess module").
- **Why Bandit flags it**: Bandit provides an informational advisory whenever `subprocess` is imported, prompting developers to audit how processes are launched.
- **Security Justification**: The `subprocess` module was introduced specifically to eliminate the high-severity shell execution vulnerability (`B605`) caused by `os.system`. Simply importing `subprocess` is safe; the security boundary depends on avoiding `shell=True` and passing discrete argument lists. Suppressing `B404` is therefore justified.

### 2. Line 76: `subprocess.run(cmd, check=False)  # nosec B603`
- **Bandit Rule**: `B603:subprocess_without_shell_equals_true` ("subprocess call - check for execution of untrusted input").
- **Why Bandit flags it**: Bandit cautions developers to ensure executable paths and arguments passed to `subprocess.run` cannot be manipulated by untrusted sources.
- **Security Justification**: 
  1. The command array `cmd = ["/usr/bin/lp", f"badges_{event_name}.txt"]` specifies the exact executable path (`/usr/bin/lp`), preventing binary hijacking or relative path traversal (`B607`).
  2. Arguments are passed as elements of a list without invoking a shell (`shell=False` is standard for `subprocess.run`). The underlying OS uses direct process execution (`execve`), which does not evaluate shell control characters (`|`, `;`, `&&`, `` ` ``), completely neutralizing command injection.
  3. `print_badges` is a mock helper retained for static analysis and is never executed during runtime demo operations.
  Therefore, `#nosec B603` is safe, appropriate, and documented.
