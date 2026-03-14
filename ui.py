import os
import readline
from colorama import init, Fore, Style

init()

COMMANDS = [
    "hello", "add", "change", "phone", "all", "delete", "search",
    "add-birthday", "show-birthday", "birthdays",
    "add-email", "add-address",
    "add-note", "show-notes", "edit-note", "delete-note",
    "find-note", "add-tag", "find-by-tag", "sort-by-tag",
    "help", "close", "exit",
]


def _completer(text, state):
    matches = [c for c in COMMANDS if c.startswith(text)]
    return matches[state] if state < len(matches) else None


readline.set_completer(_completer)
readline.set_completer_delims(readline.get_completer_delims().replace("-", ""))
if "libedit" in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

GREEN = Fore.GREEN + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW + Style.BRIGHT
MAGENTA = Fore.MAGENTA + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT
BLUE = Fore.BLUE + Style.BRIGHT
DIM = Style.DIM
R = Style.RESET_ALL

SUCCESS_KEYWORDS = ("added", "updated", "deleted")
ERROR_KEYWORDS = (
    "not found", "not enough", "invalid", "not set",
    "no upcoming", "no contacts", "no notes",
)


def _terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def _build_table(columns, rows, col_styles=None):
    """Build a unicode box table from columns and rows.

    columns: list of header strings
    rows: list of tuples/lists matching columns
    col_styles: optional list of ANSI color codes per column
    """
    num_cols = len(columns)
    col_styles = col_styles or [""] * num_cols

    # calculate column widths
    widths = [len(c) for c in columns]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    # cap total width to terminal
    term_w = _terminal_width()
    padding = 2  # 1 space each side
    border_chars = num_cols + 1  # │ between and at edges
    total = sum(widths) + num_cols * padding + border_chars
    if total > term_w:
        excess = total - term_w
        # shrink the widest column
        widest = widths.index(max(widths))
        widths[widest] = max(widths[widest] - excess, 8)

    def pad(text, width):
        return text[:width].ljust(width)

    # distribute extra space evenly across all columns
    total = sum(widths) + num_cols * padding + border_chars
    if total < term_w:
        extra = term_w - total
        per_col = extra // num_cols
        remainder = extra % num_cols
        for i in range(num_cols):
            widths[i] += per_col + (1 if i < remainder else 0)

    def hline(left, mid, right, fill="─"):
        parts = [fill * (w + padding) for w in widths]
        return left + mid.join(parts) + right

    top = f"{DIM}{hline('┌', '┬', '┐')}{R}"
    mid = f"{DIM}{hline('├', '┼', '┤')}{R}"
    bot = f"{DIM}{hline('└', '┴', '┘')}{R}"

    def data_row(cells, styles=None):
        styles = styles or [""] * num_cols
        parts = []
        for i, cell in enumerate(cells):
            s = styles[i]
            parts.append(f" {s}{pad(cell, widths[i])}{R if s else ''} ")
        return f"{DIM}│{R}" + f"{DIM}│{R}".join(parts) + f"{DIM}│{R}"

    lines = [top]
    header_styles = [WHITE] * num_cols
    lines.append(data_row(columns, header_styles))
    lines.append(mid)
    for row in rows:
        lines.append(data_row(row, col_styles))
    lines.append(bot)
    return "\n".join(lines)


def _visible_len(text):
    """Length of text without ANSI escape sequences."""
    import re
    return len(re.sub(r"\x1b\[[0-9;]*m", "", text))


def _panel(text, border_color=YELLOW):
    w = _terminal_width()
    vis_len = _visible_len(text)
    pad_needed = w - 4 - vis_len
    top = f"{border_color}╭{'─' * (w - 2)}╮{R}"
    bot = f"{border_color}╰{'─' * (w - 2)}╯{R}"
    line = f"{border_color}│{R} {text}{' ' * max(pad_needed, 0)} {border_color}│{R}"
    return f"{top}\n{line}\n{bot}"


TEAM = [
    ("Ivan", "Team Lead"),
    ("Mykhailo", "Scrum Master"),
    ("Shamil", "Developer"),
    ("Alexander", "Developer"),
]


def print_welcome():
    print(_panel(f"{YELLOW}Assistant Bot{R}"))
    print(f"  {DIM}Your personal contacts & notes manager{R}\n")
    print(f"  {DIM}by PM Squad team:{R}")
    for name, role in TEAM:
        print(f"    {CYAN}{name:<14}{DIM}{role}{R}")
    print()
    print_help()


def print_goodbye():
    print(_panel(f"{YELLOW}See you next time!{R}"))


def print_help():
    commands = [
        ("hello", "Greeting"),
        ("add [name] [phone]", "Add contact or phone"),
        ("change [name] [old] [new]", "Change phone number"),
        ("phone [name]", "Show phones"),
        ("all", "Show all contacts"),
        ("delete [name]", "Delete contact"),
        ("search [query]", "Search contacts"),
        ("add-birthday [name] [date]", "Add birthday (DD.MM.YYYY)"),
        ("show-birthday [name]", "Show birthday"),
        ("birthdays [days]", "Upcoming birthdays"),
        ("add-email [name] [email]", "Add email"),
        ("add-address [name] [addr]", "Add address"),
        ("add-note [title] [body]", "Add a note"),
        ("show-notes", "Show all notes"),
        ("edit-note [id] [body]", "Edit note body"),
        ("delete-note [id]", "Delete a note"),
        ("find-note [query]", "Search notes"),
        ("add-tag [id] [tag]", "Add tag to a note"),
        ("find-by-tag [tag]", "Find notes by tag"),
        ("sort-by-tag", "Show notes sorted by tag"),
        ("help", "Show this help"),
        ("close / exit", "Save and quit"),
    ]
    print(_build_table(
        ["Command", "Description"],
        commands,
        col_styles=[MAGENTA, CYAN],
    ))


def get_input():
    prompt = f"\x01{BLUE}\x02> \x01{R}\x02"
    return input(prompt)


def print_result(message):
    lower = message.lower()
    if any(kw in lower for kw in ERROR_KEYWORDS):
        print(f"{RED}✖ {message}{R}")
    elif any(kw in lower for kw in SUCCESS_KEYWORDS):
        print(f"{GREEN}✔ {message}{R}")
    else:
        print(f"{CYAN}{message}{R}")


def print_contacts_table(records):
    records = list(records)
    if not records:
        print(f"{RED}✖ No contacts saved.{R}")
        return

    rows = []
    for r in records:
        phones = "; ".join(str(p) for p in r.phones) or "—"
        birthday = r.birthday.value.strftime("%d.%m.%Y") if r.birthday else "—"
        email = str(r.email) if r.email else "—"
        address = str(r.address) if r.address else "—"
        rows.append((r.name.value, phones, birthday, email, address))

    print(_build_table(
        ["Name", "Phones", "Birthday", "Email", "Address"],
        rows,
        col_styles=[WHITE, CYAN, CYAN, CYAN, CYAN],
    ))


def print_notes_table(notes):
    notes = list(notes)
    if not notes:
        print(f"{RED}✖ No notes saved.{R}")
        return

    rows = []
    for note in notes:
        tags = ", ".join(note.tags) if note.tags else "—"
        rows.append((str(note.id), note.title, note.body, tags, note.created_at))

    print(_build_table(
        ["ID", "Title", "Body", "Tags", "Created"],
        rows,
        col_styles=[WHITE, WHITE, CYAN, CYAN, CYAN],
    ))


def print_birthdays(upcoming):
    if not upcoming:
        print(f"{RED}✖ No upcoming birthdays.{R}")
        return

    rows = [(item["name"], item["congratulation_date"]) for item in upcoming]
    print(_build_table(
        ["Name", "Congratulation Date"],
        rows,
        col_styles=[WHITE, CYAN],
    ))
