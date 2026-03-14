from handlers_contacts import (
    add_contact, change_contact, delete_contact, show_phone,
    add_birthday, show_birthday, birthdays, add_email, add_address,
    search_contacts,
)

from handlers_notes import (
    add_note, delete_note, edit_note, show_notes,
    find_note, add_tag, find_by_tag, sort_by_tag,
)
from storage import load_data, save_data
from ui import (
    print_welcome, print_goodbye, print_result, get_input,
    print_contacts_table, print_notes_table, print_birthdays, print_help,
)


# Parse user input into command and arguments
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Main bot loop: read commands and dispatch to handlers
def main():
    book, notebook = load_data()
    print_welcome()
    while True:
        try:
            user_input = get_input()
        except (KeyboardInterrupt, EOFError):
            print()
            save_data(book, notebook)
            print_goodbye()
            break
        if not user_input.strip():
            continue
        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                save_data(book, notebook)
                print_goodbye()
                break
            case "hello":
                print_result("How can I help you?")
            case "help":
                print_help()
            # Contacts commands
            case "add":
                print_result(add_contact(args, book))
            case "change":
                print_result(change_contact(args, book))
            case "phone":
                print_result(show_phone(args, book))
            case "all":
                print_contacts_table(book.data.values())
            case "delete":
                print_result(delete_contact(args, book))
            case "add-birthday":
                print_result(add_birthday(args, book))
            case "show-birthday":
                print_result(show_birthday(args, book))
            case "birthdays":
                try:
                    days = int(args[0]) if args else 7
                except ValueError:
                    print_result("Please provide a valid number of days.")
                    continue
                print_birthdays(book.get_upcoming_birthdays(days))
            case "add-email":
                print_result(add_email(args, book))
            case "add-address":
                print_result(add_address(args, book))
            case "search":
                results = book.search(args[0]) if args else []
                if results:
                    print_contacts_table(results)
                else:
                    print_result("No contacts found." if args else "Not enough arguments provided.")
            # Notes commands
            case "add-note":
                print_result(add_note(args, notebook))
            case "show-notes":
                print_notes_table(notebook.notes.values())
            case "edit-note":
                print_result(edit_note(args, notebook))
            case "delete-note":
                print_result(delete_note(args, notebook))
            # New note commands
            case "find-note":
                print_result(find_note(args, notebook))
            case "add-tag":
                print_result(add_tag(args, notebook))
            case "find-by-tag":
                print_result(find_by_tag(args, notebook))
            case "sort-by-tag":
                print_result(sort_by_tag(args, notebook))
            case _:
                print_result("Invalid command.")


if __name__ == "__main__":
    main()