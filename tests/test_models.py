import pytest
from datetime import datetime
from models import Field, Name, Phone, Record, AddressBook, Note, NoteBook


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

    def test_str(self):
        r = Record("John")
        r.add_phone("1234567890")
        assert "John" in str(r)
        assert "1234567890" in str(r)


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
