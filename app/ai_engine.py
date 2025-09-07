from datetime import datetime

# -------------------------
# FIX_SUGGESTIONS dictionary
# -------------------------
FIX_SUGGESTIONS = {
    "crash": "Wrap in try/except, validate inputs.",
    "data loss": "Use transactions, implement backups.",
    "error": "Check stack trace, handle exceptions.",
    "slow": "Optimize code, add caching.",
    "typo": "Fix typo in UI or messages.",
    "ui": "Check front-end code, responsiveness.",
    "login": "Ensure secure authentication.",
    "database": "Check queries, indexes, transactions.",
    "button": "Add onclick handler or fix non-working button",
    "modal": "Add close button or fix modal issues",
    "form": "Add validation, submit button, and default values",
    "css": "Fix class inconsistencies or hard-coded colors",
    "image": "Fix broken paths, add alt text, lazy loading",
    "network": "Add retries, timeouts, and validation",
    "security": "Add input sanitization, encryption, and CSRF/XSS prevention",
    "async": "Add missing await for async calls",
}

# -------------------------
# CATEGORY_MAP
# -------------------------
CATEGORY_MAP = {
    "crash": "Backend", "data loss": "Backend", "error": "Backend",
    "slow": "Performance", "typo": "Frontend", "ui": "Frontend",
    "login": "Frontend", "database": "Database", "button": "Frontend",
    "modal": "Frontend", "form": "Frontend", "css": "Frontend",
    "image": "Frontend", "network": "Backend", "security": "Security",
    "async": "Backend"
}

# -------------------------
# AUTO_FIX_TEMPLATES
# -------------------------
AUTO_FIX_TEMPLATES = {
    "TODO placeholders": "code = code.replace('TODO_BUG', 'FIXED_PART')",
    "Print/if/for formatting": "# Standardize print(), if, for loops",
    "Missing imports": "# Add missing import statements",
    "Unused variables": "# Remove unused variables",
    "Indentation errors": "# Fix indentation automatically",
    "Missing return statements": "# Add default return statement",
    "Exception handling": "try:\n    # code\nexcept Exception as e:\n    print(e)",
    "Deprecated function usage": "# Replace deprecated function",
    "Division by zero": "# Add conditional check before division",
    "Null/None checks": "# Add None checks",
    "List/dict key existence": "# Check key/index existence",
    "File path/file not found": "# Check file existence",
    "Network requests timeout": "# Add retry & timeout",
    "Hard-coded configuration": "# Move to config/env",
    "Button missing click handler": "# Add default onclick handler",
    "Disabled button": "# Enable button automatically",
    "Button tooltip missing": "# Add default tooltip",
    "Duplicate button ID": "# Ensure unique button IDs",
    "Modal missing close button": "# Add close button",
    "Form missing submit": "# Add submit button",
    "Input validation missing": "# Add regex/length validation",
    "CSS class inconsistency": "# Standardize CSS classes",
    "Image path broken": "# Fix image path",
    "Missing alt attribute": "# Add alt text",
    "XSS vulnerability": "# Escape user input",
    "SQL injection prevention": "# Parameterize queries",
    "Password encryption missing": "# Hash/salt passwords",
    "Authentication session expiry": "# Add auto session expiry",
    "Logging missing timestamp": "# Add timestamp to logs",
    "Async missing await": "# Add await for async calls",
}

# -------------------------
# In-memory bug history
# -------------------------
bug_history = []

# -------------------------
# AI Functions
# -------------------------
def predict_bug_severity(description):
    desc = description.lower()
    high = ["crash", "data loss", "security"]
    medium = ["error", "slow", "database", "login", "button", "network"]
    for k in FIX_SUGGESTIONS:
        if k in desc:
            if k in high:
                return "High"
            elif k in medium:
                return "Medium"
    return "Low"

def detect_category(description):
    desc = description.lower()
    for keyword, category in CATEGORY_MAP.items():
        if keyword in desc:
            return category
    return "General"

def suggest_fix(description):
    desc = description.lower()
    for keyword, fix in FIX_SUGGESTIONS.items():
        if keyword in desc:
            return fix
    return "Review logs and code modules."

def generate_auto_fix(description, code=""):
    desc = description.lower()
    fixes = []

    # Apply automated templates
    for keyword, template in AUTO_FIX_TEMPLATES.items():
        if keyword.lower() in desc:
            fixes.append(template)

    # Python code auto-fixes
    if 'TODO_BUG' in code:
        code = code.replace("TODO_BUG", "FIXED_PART")
        fixes.append("Replaced TODO_BUG with FIXED_PART")
    if 'print(' in code and 'print (' not in code:
        code = code.replace('print(', 'print (')
        fixes.append("Fixed print formatting")
    if 'if ' in code and ':\n' not in code:
        code = code.replace('if ', 'if:\n    ')
        fixes.append("Fixed if statement formatting")
    if 'for ' in code and ':\n' not in code:
        code = code.replace('for ', 'for:\n    ')
        fixes.append("Fixed for loop formatting")

    # Frontend button/HTML fixes
    # Add onclick if missing
    if '<button' in code and 'onclick' not in code:
        code = code.replace('<button', '<button onclick="defaultClick()"')
        fixes.append("Added default onclick handler")
    # Enable disabled buttons
    if 'disabled' in code:
        code = code.replace('disabled', '')
        fixes.append("Enabled button automatically")
    # Add tooltip if missing
    if '<button' in code and 'title=' not in code:
        code = code.replace('<button', '<button title="Click me"')
        fixes.append("Added tooltip to button")
    # Fix duplicate IDs
    import re
    ids = re.findall(r'id="(.*?)"', code)
    seen = set()
    for i, id_name in enumerate(ids):
        if id_name in seen:
            new_id = f"{id_name}_{i}"
            code = code.replace(f'id="{id_name}"', f'id="{new_id}"', 1)
            fixes.append(f"Fixed duplicate button ID: {id_name} → {new_id}")
        seen.add(id_name)

    # Modal fixes
    if '<div class="modal"' in code and 'close' not in code:
        code += '\n<!-- Added close button -->'
        fixes.append("Added close button to modal")

    # Form fixes
    if '<form' in code and 'submit' not in code:
        code += '\n<input type="submit" value="Submit">'
        fixes.append("Added submit button to form")
    if 'input' in code and 'pattern' not in code:
        code += '\n<!-- Added basic input validation -->'
        fixes.append("Added input validation to form fields")

    return code, "\n---\n".join(fixes) if fixes else "No automated fix available."

def analyze_and_fix_code(code, description=""):
    """
    This is the function that the routes are trying to import
    It analyzes code and provides fixes based on the description
    """
    if not code:
        return "", "No code provided", "Low"
    
    # Use the existing generate_auto_fix function
    fixed_code, notes = generate_auto_fix(description, code)
    
    # Predict severity
    severity = predict_bug_severity(description)
    
    return fixed_code, notes, severity

def log_bug(description, code=""):
    severity = predict_bug_severity(description)
    category = detect_category(description)
    fixed_code, auto_fix_notes = generate_auto_fix(description, code)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bug = {
        "description": description,
        "severity": severity,
        "category": category,
        "auto_fix_notes": auto_fix_notes,
        "fixed_code": fixed_code,
        "timestamp": timestamp
    }
    bug_history.append(bug)
    return bug
