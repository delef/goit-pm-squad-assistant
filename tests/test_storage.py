import pytest
from models import AddressBook, NoteBook, Record
import storage


@pytest.fixture
def temp_file(tmp_path, monkeypatch):
    filepath = tmp_path / "assistant_data.pkl"
    monkeypatch.setattr(storage, "FILENAME", filepath)
    return filepath


class TestSaveData:
    def test_save_and_load(self, temp_file):
        book = AddressBook()
        r = Record("John")
        r.add_phone("1234567890")
        book.add_record(r)

        notebook = NoteBook()
        notebook.add_note("Test", "Some text")

        storage.save_data(book, notebook)
        assert temp_file.exists()

        loaded_book, loaded_notebook = storage.load_data()
        assert loaded_book.find("John") is not None
        assert loaded_book.find("John").phones[0].value == "1234567890"
        assert loaded_notebook.find(1) is not None
        assert loaded_notebook.find(1).title == "Test"

    def test_load_no_file(self, temp_file):
        book, notebook = storage.load_data()
        assert isinstance(book, AddressBook)
        assert isinstance(notebook, NoteBook)
        assert len(book.data) == 0
        assert len(notebook.notes) == 0

    def test_save_overwrites(self, temp_file):
        book = AddressBook()
        notebook = NoteBook()

        r1 = Record("Alice")
        book.add_record(r1)
        storage.save_data(book, notebook)

        book2 = AddressBook()
        r2 = Record("Bob")
        book2.add_record(r2)
        storage.save_data(book2, notebook)

        loaded_book, _ = storage.load_data()
        assert loaded_book.find("Alice") is None
        assert loaded_book.find("Bob") is not None
