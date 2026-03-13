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


# Parse user input into command and arguments
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Main bot loop: read commands and dispatch to handlers
def main():
    book, notebook = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                save_data(book, notebook)
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            # Contacts commands
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                for record in book.data.values():
                    print(record)
            case "delete":
                print(delete_contact(args, book))
            # Notes commands
            case "add-note":
                print(add_note(args, notebook))
            case "show-notes":
                print(show_notes(notebook))
            case "edit-note":
                print(edit_note(args, notebook))
            case "delete-note":
                print(delete_note(args, notebook))
            # New note commands
            case "find-note":
                print(find_note(args, notebook))
            case "add-tag":
                print(add_tag(args, notebook))
            case "find-by-tag":
                print(find_by_tag(args, notebook))
            case "sort-by-tag":
                print(sort_by_tag(args, notebook))
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()