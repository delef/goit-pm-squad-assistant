import pytest
from datetime import datetime, timedelta
from models import (
    Field, Name, Phone, Birthday, Email, Address,
    Record, AddressBook, Note, NoteBook,
)


# --- Field ---

class TestField:
    def test_str(self):
        assert str(Field("hello")) == "hello"


# --- Name ---

class TestName:
    def test_str(self):
        assert str(Name("John")) == "John"


# --- Phone ---

class TestPhone:
    def test_valid_phone(self):
        p = Phone("1234567890")
        assert p.value == "1234567890"

    def test_short_phone(self):
        with pytest.raises(ValueError):
            Phone("12345")

    def test_letters_phone(self):
        with pytest.raises(ValueError):
            Phone("abcdefghij")

    def test_long_phone(self):
        with pytest.raises(ValueError):
            Phone("12345678901")


# --- Birthday ---

class TestBirthday:
    def test_valid_birthday(self):
        b = Birthday("24.08.1983")
        assert b.value == datetime.strptime("24.08.1983", "%d.%m.%Y")

    def test_invalid_format(self):
        with pytest.raises(ValueError):
            Birthday("1983-08-24")

    def test_invalid_date(self):
        with pytest.raises(ValueError):
            Birthday("not-a-date")


# --- Email ---

class TestEmail:
    def test_valid_email(self):
        e = Email("test@mail.com")
        assert e.value == "test@mail.com"

    def test_no_at(self):
        with pytest.raises(ValueError):
            Email("testmail.com")

    def test_no_dot_after_at(self):
        with pytest.raises(ValueError):
            Email("test@mailcom")

    def test_at_at_start(self):
        with pytest.raises(ValueError):
            Email("@mail.com")


# --- Address ---

class TestAddress:
    def test_stores_value(self):
        a = Address("Kyiv, Main St 1")
        assert a.value == "Kyiv, Main St 1"


# --- Record ---

class TestRecord:
    def test_add_phone(self):
        r = Record("John")
        r.add_phone("1234567890")
        assert len(r.phones) == 1
        assert r.phones[0].value == "1234567890"

    def test_add_multiple_phones(self):
        r = Record("John")
        r.add_phone("1234567890")
        r.add_phone("0987654321")
        assert len(r.phones) == 2

    def test_remove_phone(self):
        r = Record("John")
        r.add_phone("1234567890")
        r.remove_phone("1234567890")
        assert len(r.phones) == 0

    def test_edit_phone(self):
        r = Record("John")
        r.add_phone("1234567890")
        r.edit_phone("1234567890", "1112223333")
        assert r.phones[0].value == "1112223333"

    def test_edit_phone_not_found(self):
        r = Record("John")
        r.add_phone("1234567890")
        with pytest.raises(ValueError):
            r.edit_phone("9999999999", "1112223333")

    def test_find_phone(self):
        r = Record("John")
        r.add_phone("1234567890")
        phone = r.find_phone("1234567890")
        assert phone is not None
        assert phone.value == "1234567890"
        assert r.find_phone("0000000000") is None

    def test_add_birthday(self):
        r = Record("John")
        r.add_birthday("24.08.1983")
        assert r.birthday is not None
        assert r.birthday.value.strftime("%d.%m.%Y") == "24.08.1983"

    def test_add_email(self):
        r = Record("John")
        r.add_email("john@mail.com")
        assert r.email is not None
        assert r.email.value == "john@mail.com"

    def test_add_address(self):
        r = Record("John")
        r.add_address("Kyiv Main St 1")
        assert r.address is not None
        assert r.address.value == "Kyiv Main St 1"

    def test_str(self):
        r = Record("John")
        r.add_phone("1234567890")
        assert "John" in str(r)
        assert "1234567890" in str(r)

    def test_str_with_all_fields(self):
        r = Record("John")
        r.add_phone("1234567890")
        r.add_birthday("24.08.1983")
        r.add_email("john@mail.com")
        r.add_address("Kyiv")
        s = str(r)
        assert "24.08.1983" in s
        assert "john@mail.com" in s
        assert "Kyiv" in s


# --- AddressBook ---

class TestAddressBook:
    def test_add_and_find(self):
        book = AddressBook()
        r = Record("John")
        book.add_record(r)
        assert book.find("John") is r

    def test_find_not_found(self):
        book = AddressBook()
        assert book.find("Nobody") is None

    def test_delete(self):
        book = AddressBook()
        r = Record("John")
        book.add_record(r)
        book.delete("John")
        assert book.find("John") is None

    def test_delete_not_found(self):
        book = AddressBook()
        with pytest.raises(KeyError):
            book.delete("Nobody")

    def test_search_by_name(self):
        book = AddressBook()
        r = Record("John")
        book.add_record(r)
        results = book.search("john")
        assert len(results) == 1
        assert results[0].name.value == "John"

    def test_search_by_phone(self):
        book = AddressBook()
        r = Record("John")
        r.add_phone("1234567890")
        book.add_record(r)
        results = book.search("1234")
        assert len(results) == 1

    def test_search_by_email(self):
        book = AddressBook()
        r = Record("John")
        r.add_email("john@mail.com")
        book.add_record(r)
        results = book.search("john@mail")
        assert len(results) == 1

    def test_search_not_found(self):
        book = AddressBook()
        r = Record("John")
        book.add_record(r)
        results = book.search("nobody")
        assert len(results) == 0

    def test_get_upcoming_birthdays(self):
        book = AddressBook()
        r = Record("John")
        # Set birthday to 3 days from now (this year)
        future = datetime.today() + timedelta(days=3)
        bday_str = future.strftime("%d.%m.%Y").replace(
            str(future.year), "1990"
        )
        r.add_birthday(bday_str)
        book.add_record(r)
        upcoming = book.get_upcoming_birthdays(7)
        assert len(upcoming) == 1
        assert upcoming[0]["name"] == "John"

    def test_get_upcoming_birthdays_empty(self):
        book = AddressBook()
        r = Record("John")
        book.add_record(r)
        upcoming = book.get_upcoming_birthdays(7)
        assert len(upcoming) == 0


# --- Note ---

class TestNote:
    def test_creation(self):
        note = Note(1, "Title", "Body text")
        assert note.id == 1
        assert note.title == "Title"
        assert note.body == "Body text"
        assert note.tags == []
        assert note.created_at == datetime.now().strftime("%Y-%m-%d")

    def test_str(self):
        note = Note(1, "Shopping", "Buy milk")
        s = str(note)
        assert "[1] Shopping" in s
        assert "Buy milk" in s


# --- NoteBook ---

class TestNoteBook:
    def test_add_note(self):
        nb = NoteBook()
        note = nb.add_note("Title", "Body")
        assert note.id == 1
        assert nb.find(1) is note

    def test_auto_increment(self):
        nb = NoteBook()
        n1 = nb.add_note("First", "body1")
        n2 = nb.add_note("Second", "body2")
        assert n1.id == 1
        assert n2.id == 2

    def test_find_not_found(self):
        nb = NoteBook()
        assert nb.find(99) is None

    def test_delete(self):
        nb = NoteBook()
        nb.add_note("Title", "Body")
        nb.delete(1)
        assert nb.find(1) is None

    def test_delete_not_found(self):
        nb = NoteBook()
        with pytest.raises(KeyError):
            nb.delete(99)
