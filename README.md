# Personal Assistant — CLI Bot

A command-line assistant for managing contacts and notes, built with Python.

## Team

| Name | Role |
|------|------|
| Mykhailo | Scrum Master |
| Ivan | Team Lead |
| Shamil | Developer |
| Alexander | Developer |

## How to Run

```bash
git clone https://github.com/delef/goit-pm-squad-assistant.git
cd goit-pm-squad-assistant
python main.py
```

## Project Structure

| File | Description |
|------|-------------|
| `main.py` | Entry point. Starts the bot, runs the command loop, connects all commands to handler functions. On start calls `load_data()`, on exit calls `save_data()`. |
| `models.py` | Contains all data classes: `Field`, `Name`, `Phone`, `Email`, `Birthday`, `Address`, `Record`, `AddressBook`, `Note`, `NoteBook`. |
| `handlers_contacts.py` | Functions that handle contact-related commands. Each function takes `(args, book)` and returns a string. |
| `handlers_notes.py` | Functions that handle note-related commands. Each function takes `(args, notebook)` and returns a string. |
| `decorators.py` | Contains the `@input_error` decorator that wraps handler functions and catches errors. |
| `storage.py` | `save_data()` and `load_data()` functions — saves/loads AddressBook and NoteBook to/from a `.pkl` file. |
| `.gitignore` | Tells Git to ignore: `assistant_data.pkl`, `__pycache__/`, `venv/` |
| `README.md` | Project description and list of all available commands. |

## Available Commands

| Command | Description |
|---------|-------------|
| `hello` | Greeting |
| `add [name] [phone]` | Add a contact or add a phone to an existing contact |
| `change [name] [old phone] [new phone]` | Change a phone number |
| `phone [name]` | Show phone numbers for a contact |
| `all` | Show all contacts |
| `search [query]` | Search contacts by any field |
| `delete [name]` | Delete a contact |
| `add-birthday [name] [DD.MM.YYYY]` | Add birthday to a contact |
| `show-birthday [name]` | Show birthday for a contact |
| `birthdays [days]` | Show upcoming birthdays (default: 7 days) |
| `add-email [name] [email]` | Add email to a contact |
| `add-address [name] [address]` | Add address to a contact |
| `add-note [title] [body]` | Add a new note |
| `show-notes` | Show all notes |
| `find-note [query]` | Search notes by title or body |
| `edit-note [id] [new body]` | Edit a note |
| `delete-note [id]` | Delete a note |
| `add-tag [id] [tag]` | Add a tag to a note |
| `find-by-tag [tag]` | Find notes by tag |
| `sort-by-tag` | Show notes sorted by tags |
| `help` | Show available commands |
| `close` / `exit` | Exit the program |

## GitHub Workflow

1. Each person works in their own **feature branch** (e.g., `feature/contacts`, `feature/notes`).
2. When the work is ready, create a **Pull Request** to `main`.
3. At least **1 teammate reviews** the PR before merging.
4. Before creating a PR, run `git pull origin main` to get the latest changes.
5. **Never commit directly to `main`** — always use Pull Requests.
