from handlers_contacts import (
    add_contact, change_contact, show_phone, delete_contact,
    add_birthday, show_birthday, birthdays, add_email, add_address,
    search_contacts,
)
from models import AddressBook


class TestAddContact:
    def test_add_new(self):
        book = AddressBook()
        assert add_contact(["John", "1234567890"], book) == "Contact added."
        assert book.find("John") is not None

    def test_add_phone_to_existing(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        assert add_contact(["John", "0987654321"], book) == "Contact updated."
        record = book.find("John")
        assert record is not None
        assert len(record.phones) == 2

    def test_add_invalid_phone(self):
        book = AddressBook()
        result = add_contact(["John", "abc"], book)
        assert "10 digits" in result

    def test_add_not_enough_args(self):
        book = AddressBook()
        result = add_contact([], book)
        assert "not enough" in result.lower()


class TestChangeContact:
    def test_change_phone(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        assert change_contact(["John", "1234567890", "1112223333"], book) == "Contact updated."
        record = book.find("John")
        assert record is not None
        assert record.phones[0].value == "1112223333"

    def test_change_contact_not_found(self):
        book = AddressBook()
        assert change_contact(["Nobody", "1234567890", "1112223333"], book) == "Contact not found."

    def test_change_phone_not_found(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        result = change_contact(["John", "9999999999", "1112223333"], book)
        assert "not found" in result


class TestShowPhone:
    def test_show(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        assert show_phone(["John"], book) == "1234567890"

    def test_show_multiple(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        add_contact(["John", "0987654321"], book)
        assert show_phone(["John"], book) == "1234567890; 0987654321"

    def test_show_not_found(self):
        book = AddressBook()
        assert show_phone(["Nobody"], book) == "Contact not found."


class TestDeleteContact:
    def test_delete(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        assert delete_contact(["John"], book) == "Contact deleted."
        assert book.find("John") is None

    def test_delete_not_found(self):
        book = AddressBook()
        assert delete_contact(["Nobody"], book) == "Contact not found."


class TestAddBirthday:
    def test_add_birthday(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        assert add_birthday(["John", "24.08.1983"], book) == "Birthday added."

    def test_add_birthday_invalid_format(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        result = add_birthday(["John", "1983-08-24"], book)
        assert "Invalid date format" in result

    def test_add_birthday_not_found(self):
        book = AddressBook()
        assert add_birthday(["Nobody", "24.08.1983"], book) == "Contact not found."


class TestShowBirthday:
    def test_show_birthday(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        add_birthday(["John", "24.08.1983"], book)
        assert show_birthday(["John"], book) == "24.08.1983"

    def test_show_birthday_not_set(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        assert show_birthday(["John"], book) == "Birthday not set."

    def test_show_birthday_not_found(self):
        book = AddressBook()
        assert show_birthday(["Nobody"], book) == "Contact not found."


class TestBirthdays:
    def test_no_upcoming(self):
        book = AddressBook()
        assert birthdays([], book) == "No upcoming birthdays."

    def test_with_days_arg(self):
        book = AddressBook()
        result = birthdays(["14"], book)
        assert result == "No upcoming birthdays."


class TestAddEmail:
    def test_add_email(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        assert add_email(["John", "john@mail.com"], book) == "Email added."

    def test_add_invalid_email(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        result = add_email(["John", "invalid"], book)
        assert "Invalid email" in result

    def test_add_email_not_found(self):
        book = AddressBook()
        assert add_email(["Nobody", "a@b.com"], book) == "Contact not found."


class TestAddAddress:
    def test_add_address(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        result = add_address(["John", "Kyiv", "Main", "St", "1"], book)
        assert result == "Address added."
        record = book.find("John")
        assert record.address.value == "Kyiv Main St 1"

    def test_add_address_not_found(self):
        book = AddressBook()
        assert add_address(["Nobody", "Kyiv"], book) == "Contact not found."


class TestSearchContacts:
    def test_search_found(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        result = search_contacts(["john"], book)
        assert "John" in result

    def test_search_not_found(self):
        book = AddressBook()
        add_contact(["John", "1234567890"], book)
        assert search_contacts(["nobody"], book) == "No contacts found."

    def test_search_no_args(self):
        book = AddressBook()
        result = search_contacts([], book)
        assert "not enough" in result.lower()
