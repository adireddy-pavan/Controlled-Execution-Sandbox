import ast
import builtins
import io
import sys
import traceback
from datetime import datetime
from multiprocessing import Process, Queue
from contextlib import redirect_stdout, redirect_stderr

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

TIMEOUT = 5  # seconds
LOG_FILE = "violations.log"

# ─────────────────────────────────────────────
# Safe Builtins
# ─────────────────────────────────────────────

SAFE_BUILTINS = {
    name: getattr(builtins, name)
    for name in [
        "abs", "all", "any", "bool", "chr", "dict", "enumerate",
        "float", "int", "len", "list", "map", "max", "min",
        "pow", "print", "range", "round", "set", "str",
        "sum", "tuple", "zip"
    ]
}

# ─────────────────────────────────────────────
# Blocked Names
# ─────────────────────────────────────────────

BLOCKED_NAMES = {
    "__import__", "__builtins__", "__class__", "__bases__", "__subclasses__",
    "exec", "eval", "compile",
    "open", "os", "sys", "subprocess", "socket",
    "globals", "locals", "vars"
}

# ─────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────

def log_violation(msg):
    with open(LOG_FILE, "a") as f:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ts}] {msg}\n")

# ─────────────────────────────────────────────
# AST Security Check
# ─────────────────────────────────────────────

class SandboxViolation(Exception):
    pass


class ASTChecker(ast.NodeVisitor):

    def visit_Import(self, node):
        raise SandboxViolation("Import not allowed")

    def visit_ImportFrom(self, node):
        raise SandboxViolation("Import not allowed")

    def visit_Name(self, node):
        if node.id in BLOCKED_NAMES:
            raise SandboxViolation(f"Blocked name: {node.id}")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr.startswith("__"):
            raise SandboxViolation("Dunder access not allowed")
        self.generic_visit(node)

    def visit_With(self, node):
        raise SandboxViolation("with not allowed")

    def visit_Try(self, node):
        raise SandboxViolation("try/except not allowed")


def static_check(code):
    try:
        tree = ast.parse(code)
        ASTChecker().visit(tree)
        return tree
    except Exception as e:
        raise SandboxViolation(str(e))

# ─────────────────────────────────────────────
# Worker (Runs in separate process)
# ─────────────────────────────────────────────

def worker(code, queue):
    try:
        tree = static_check(code)

        safe_globals = {
            "__builtins__": SAFE_BUILTINS,
            "__name__": "__sandbox__"
        }

        stdout = io.StringIO()
        stderr = io.StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            compiled = compile(tree, "<sandbox>", "exec")
            exec(compiled, safe_globals, {})

        output = stdout.getvalue() + stderr.getvalue()

        queue.put({
            "accepted": True,
            "output": output.strip(),
            "error": "",
            "violation": False
        })

    except SandboxViolation as e:
        queue.put({
            "accepted": False,
            "output": "",
            "error": f"[SECURITY BLOCK] {e}",
            "violation": True
        })

    except Exception as e:
    	queue.put({
    	    "accepted": False,
    	    "output": "",
    	    "error": f"Runtime error: {e}",
    	    "violation": False
        })

# ─────────────────────────────────────────────
# Execute with Timeout
# ─────────────────────────────────────────────

def execute(code):
    queue = Queue()
    p = Process(target=worker, args=(code, queue))

    p.start()
    p.join(TIMEOUT)

    if p.is_alive():
        p.terminate()
        log_violation(f"TIMEOUT: {code[:80]}")
        return {
            "accepted": False,
            "output": "",
            "error": "[TIMEOUT] Execution took too long",
            "violation": True
        }

    if not queue.empty():
        return queue.get()

    return {
        "accepted": False,
        "output": "",
        "error": "[ERROR] Unknown issue",
        "violation": True
    }

# ─────────────────────────────────────────────
# CLI Interface
# ─────────────────────────────────────────────

def main():
    print("\n🔐 Controlled Execution Sandbox")
    print("Type code and press ENTER twice to run")
    print("Commands: exit, help\n")

    while True:
        lines = []

        while True:
            line = input(">>> " if not lines else "... ")
            if not lines and line.lower() == "exit":
                print("Exiting...")
                return
            if not lines and line.lower() == "help":
                print("Enter Python code safely. Dangerous operations are blocked.\n")
                break

            if line == "":
                break

            lines.append(line)

        if not lines:
            continue

        code = "\n".join(lines)

        result = execute(code)

        print("\n-------------------------------")

        if result["accepted"]:
            print("✔ ACCEPTED")
            if result["output"]:
                print(result["output"])
            else:
                print("(no output)")

        elif result["violation"]:
            print("✖ BLOCKED")
            print(result["error"])
            log_violation(f"BLOCKED: {code[:80]}")

        else:
            print("⚠ ERROR")
            print(result["error"])

        print("-------------------------------\n")


if __name__ == "__main__":
    main()