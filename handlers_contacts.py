from decorators import input_error
from models import AddressBook, Record


# Add a new contact or add a phone to an existing one
@input_error
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
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


# Show all phone numbers for a contact
@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    return "; ".join(p.value for p in record.phones)


# Delete a contact from the address book
@input_error
def delete_contact(args, book: AddressBook):
    name, *_ = args
    book.delete(name)
    return "Contact deleted."
