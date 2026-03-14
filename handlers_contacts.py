from decorators import input_error
from models import AddressBook, Record


# Add a new contact or add a phone to an existing one
@input_error("Contact")
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


# Change an existing phone number for a contact
@input_error("Contact")
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


# Show all phone numbers for a contact
@input_error("Contact")
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    return "; ".join(p.value for p in record.phones)


# Delete a contact from the address book
@input_error("Contact")
def delete_contact(args, book: AddressBook):
    name, *_ = args
    book.delete(name)
    return "Contact deleted."


# Add birthday to a contact
@input_error("Contact")
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return "Birthday added."


# Show birthday for a contact
@input_error("Contact")
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return "Birthday not set."
    return record.birthday.value.strftime("%d.%m.%Y")


# Show upcoming birthdays in the next N days
@input_error("Contact")
def birthdays(args, book: AddressBook):
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming
    )


# Add email to a contact
@input_error("Contact")
def add_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_email(email)
    return "Email added."


# Add address to a contact
@input_error("Contact")
def add_address(args, book: AddressBook):
    name, *address_parts = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_address(" ".join(address_parts))
    return "Address added."


# Search contacts by name, phone or email
@input_error("Contact")
def search_contacts(args, book: AddressBook):
    query, *_ = args
    results = book.search(query)
    if not results:
        return "No contacts found."
    return "\n".join(str(r) for r in results)
