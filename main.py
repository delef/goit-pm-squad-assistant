from handlers_contacts import add_contact, change_contact, delete_contact, show_phone
from storage import load_data, save_data


# Parse user input into command and arguments
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Main bot loop: read commands and dispatch to handlers
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                save_data(book)
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
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
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
