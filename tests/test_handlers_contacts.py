from handlers_contacts import add_contact, change_contact, show_phone, delete_contact
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
