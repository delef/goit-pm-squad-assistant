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
pip install -r requirements.txt
python main.py
```

> **Note (Windows):** If you get `ModuleNotFoundError: No module named 'readline'`, install the Windows replacement: `pip install pyreadline3`

## Features

- **Contact management** — phones, emails, birthdays, addresses with validation
- **Notes with tags** — create, edit, search, and organize notes by tags
- **Tab completion** — press `Tab` to autocomplete command names
- **Command suggestions** — typo detection with "Did you mean?" hints
- **Persistent storage** — data is saved automatically to `~/assistant_data.pkl`
- **Colored terminal UI** — formatted tables, colored output, welcome and help screens

## Project Structure

| File | Description |
|------|-------------|
| `main.py` | Entry point — command loop, input parsing, dispatches to handlers |
| `models.py` | Data classes: `Field`, `Name`, `Phone`, `Email`, `Birthday`, `Address`, `Record`, `AddressBook`, `Note`, `NoteBook` |
| `handlers_contacts.py` | Contact command handlers (add, change, delete, search, birthday, email, address) |
| `handlers_notes.py` | Note command handlers (add, edit, delete, find, tags) |
| `decorators.py` | `@input_error` decorator — catches and formats handler errors |
| `storage.py` | `save_data()` / `load_data()` — persists AddressBook and NoteBook to a `.pkl` file |
| `ui.py` | Colored terminal output, tables, tab-completion, command suggestions, welcome/help screens |

## Available Commands

### Contacts

| Command | Description |
|---------|-------------|
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

### Notes

| Command | Description |
|---------|-------------|
| `add-note [title] [body]` | Add a new note |
| `show-notes` | Show all notes |
| `edit-note [id] [body]` | Edit a note |
| `delete-note [id]` | Delete a note |
| `find-note [query]` | Search notes by title or body |
| `add-tag [id] [tag]` | Add a tag to a note |
| `find-by-tag [tag]` | Find notes by tag |
| `sort-by-tag` | Show notes sorted by tags |

### General

| Command | Description |
|---------|-------------|
| `hello` | Greeting |
| `help` | Show available commands |
| `close` / `exit` | Save and exit |

## Tests

Tests are located in the `tests/` directory and run with [pytest](https://docs.pytest.org/):

```bash
pytest tests/ -v
```

Tests run automatically on every pull request via GitHub Actions (Python 3.12).

| Test file | Coverage |
|-----------|----------|
| `test_models.py` | Data classes: Field, Name, Phone, Birthday, Email, Address, Record, AddressBook, Note, NoteBook |
| `test_handlers_contacts.py` | Contact command handlers |
| `test_handlers_notes.py` | Note command handlers |
| `test_storage.py` | Data persistence (save/load) |
| `test_suggest_command.py` | Command suggestion and typo detection |

## GitHub Workflow

1. Each person works in their own **feature branch** (e.g., `feature/contacts`, `feature/notes`).
2. When the work is ready, create a **Pull Request** to `main`.
3. At least **1 teammate reviews** the PR before merging.
4. Before creating a PR, run `git pull origin main` to get the latest changes.
5. **Never commit directly to `main`** — always use Pull Requests.
