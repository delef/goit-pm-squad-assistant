from handlers_notes import add_note, show_notes, edit_note, delete_note
from models import NoteBook


class TestAddNote:
    def test_add(self):
        nb = NoteBook()
        assert add_note(["Shopping", "Buy", "milk"], nb) == "Note added with ID 1."
        note = nb.find(1)
        assert note is not None
        assert note.title == "Shopping"
        assert note.body == "Buy milk"

    def test_add_with_separator(self):
        nb = NoteBook()
        assert add_note(["My", "Cool", "Title", "--", "here", "is", "the", "body"], nb) == "Note added with ID 1."
        note = nb.find(1)
        assert note.title == "My Cool Title"
        assert note.body == "here is the body"

    def test_add_separator_no_body(self):
        nb = NoteBook()
        assert add_note(["Title", "--"], nb) == "Note added with ID 1."
        note = nb.find(1)
        assert note.title == "Title"
        assert note.body == ""

    def test_add_without_separator_backwards_compatible(self):
        nb = NoteBook()
        assert add_note(["Shopping", "Buy", "milk"], nb) == "Note added with ID 1."
        note = nb.find(1)
        assert note.title == "Shopping"
        assert note.body == "Buy milk"

    def test_add_not_enough_args(self):
        nb = NoteBook()
        result = add_note([], nb)
        assert "not enough" in result.lower()


class TestShowNotes:
    def test_empty(self):
        nb = NoteBook()
        assert show_notes(nb) == "No notes saved."

    def test_show_all(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        nb.add_note("Work", "Finish report")
        result = show_notes(nb)
        assert "Shopping" in result
        assert "Work" in result


class TestEditNote:
    def test_edit(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        assert edit_note(["1", "Updated", "text"], nb) == "Note updated."
        note = nb.find(1)
        assert note is not None
        assert note.body == "Updated text"

    def test_edit_not_found(self):
        nb = NoteBook()
        assert edit_note(["99", "nope"], nb) == "Note not found."


class TestDeleteNote:
    def test_delete(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        assert delete_note(["1"], nb) == "Note deleted."
        assert nb.find(1) is None

    def test_delete_not_found(self):
        nb = NoteBook()
        assert delete_note(["99"], nb) == "Note not found."
