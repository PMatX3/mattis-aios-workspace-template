# Install

> Install an AIOS module from the module-installs directory.

## Variables

module_path: $ARGUMENTS (path to the module folder, e.g., `module-installs/infra-os`)

---

## Instructions

You are installing an AIOS module. Follow these steps:

### Step 1: Locate the module

The module path is provided in `$ARGUMENTS`. It will look like `module-installs/infra-os` or `@module-installs/infra-os` (strip any leading `@`).

If no path was provided, list available modules:
```bash
ls module-installs/
```
Then ask the user: "Which module would you like to install?"

### Step 2: Read the INSTALL.md

Read the `INSTALL.md` file from the module directory. This file contains all installation instructions for Claude to follow.

### Step 3: Follow the INSTALL.md instructions exactly

Execute every step in the INSTALL.md. The INSTALL.md is authoritative — follow it as written, including:
- Running prerequisite checks
- Asking scoping questions if required
- Creating files from templates in the module's `templates/` folder
- Modifying existing workspace files (prime, implement, CLAUDE.md, etc.)
- Running verification steps after each action

### Step 4: Confirm installation complete

Report:
- What was installed
- Files created or modified
- Any steps that were skipped (e.g., already configured)
- What the user should do next