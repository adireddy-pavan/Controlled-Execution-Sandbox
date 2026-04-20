# 🔐 Controlled Execution Sandbox

## 📌 Overview

This project implements a **Controlled Execution Sandbox** designed to safely execute untrusted Python code under strict security constraints.

The system prevents unauthorized access to system resources, restricts unsafe operations, and ensures that user-provided code runs in an isolated and controlled environment.

---

## 🎯 Objective

The main objective of this project is to:

* Safely process untrusted user input
* Prevent execution of malicious or restricted operations
* Control resource usage (time limits)
* Provide clear feedback for accepted, blocked, or erroneous inputs

---

## ⚙️ Features

### 🔐 1. AST-Based Security Validation

* Uses Abstract Syntax Tree (AST) to analyze input code
* Blocks unsafe constructs such as:

  * `import` statements
  * `exec`, `eval`
  * file operations (`open`)
  * system-level access

---

### 🛡️ 2. Restricted Execution Environment

* Executes code using limited **safe built-in functions**
* Prevents access to:

  * Operating system
  * File system
  * Network resources

---

### ⚙️ 3. Process Isolation (Multiprocessing)

* Runs code in a **separate process**
* Ensures isolation from the main system
* Prevents crashes or system-level impact

---

### ⏱️ 4. Timeout Control

* Automatically terminates long-running or infinite loops
* Prevents resource exhaustion

---

### 🚨 5. Violation Detection

* Detects:

  * Unauthorized operations
  * Restricted function usage
  * Suspicious behavior

---

### 🧾 6. Logging System

* Logs all violations and suspicious inputs
* Stored in: `violations.log`

---

### 💬 7. User-Friendly Output

* ✔ ACCEPTED → Safe execution
* ✖ BLOCKED → Security violation
* ⚠ ERROR → Runtime error
* ⏱ TIMEOUT → Infinite loop / long execution

---

## 🏗️ System Architecture

```
User Input
   ↓
AST Validation (Security Check)
   ↓
Policy Enforcement (Blocked Names / Safe Builtins)
   ↓
Execution in Isolated Process
   ↓
Timeout Monitoring
   ↓
Output / Error Handling
   ↓
Logging (if violation)
```

---

## 🚀 How to Run the Project

### ✅ Prerequisites

* Python 3.x installed
* Windows OS (recommended)

---

### ▶️ Steps

1. Download or clone the project
2. Open terminal / command prompt
3. Navigate to project folder

```bash
cd your_project_folder
```

4. Run the sandbox:

```bash
python sandbox.py
```

---

## 🧪 Usage Instructions

### ➤ Enter Python code

Type your code line-by-line and press **Enter twice** to execute.

---

### ✅ Example: Safe Input

```
>>> print(5 + 5)
```

Output:

```
✔ ACCEPTED
10
```

---

### ❌ Example: Blocked Input

```
>>> import os
```

Output:

```
✖ BLOCKED
[SECURITY BLOCK] Import not allowed
```

---

### ⚠ Example: Runtime Error

```
>>> print(1/0)
```

Output:

```
⚠ ERROR
Runtime error: division by zero
```

---

### ⏱ Example: Infinite Loop

```
>>> while True: pass
```

Output:

```
[TIMEOUT] Execution took too long
```

---

## 📁 Project Structure

```
.
├── sandbox.py
├── violations.log
├── README.md
```

---

## ⚠️ Limitations

* Not a full OS-level sandbox (no containerization)
* Limited to Python code execution
* Advanced sandbox escape techniques are not covered

---

## 📚 References

* Python Documentation (AST Module)
* Python Multiprocessing Module
* Cybersecurity Sandbox Concepts

---

## 👨‍💻 Author

Pavan Adireddy

---

## 📌 Conclusion

This project demonstrates how untrusted code can be executed safely using a combination of validation, restriction, isolation, and monitoring techniques. It simulates real-world sandboxing concepts used in secure systems.
