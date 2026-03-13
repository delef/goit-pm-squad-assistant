from handlers_notes import add_note, show_notes, edit_note, delete_note, find_note, add_tag, find_by_tag, sort_by_tag
from models import NoteBook


class TestAddNote:
    def test_add(self):
        nb = NoteBook()
        assert add_note(["Shopping", "Buy", "milk"], nb) == "Note added with ID 1."
        note = nb.find(1)
        assert note is not None
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
        assert edit_note(["99", "nope"], nb) == "Contact not found."


class TestDeleteNote:
    def test_delete(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        assert delete_note(["1"], nb) == "Note deleted."
        assert nb.find(1) is None

    def test_delete_not_found(self):
        nb = NoteBook()
        assert delete_note(["99"], nb) == "Contact not found."


class TestFindNote:
    def test_find_by_title(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        nb.add_note("Work", "Finish report")
        result = find_note(["shopping"], nb)
        assert "Shopping" in result
        assert "Work" not in result

    def test_find_by_body(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk and eggs")
        nb.add_note("Work", "Finish report")
        result = find_note(["eggs"], nb)
        assert "Shopping" in result
        assert "Work" not in result

    def test_find_case_insensitive(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy MILK")
        result = find_note(["milk"], nb)
        assert "Shopping" in result

    def test_find_no_match(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        result = find_note(["xyz"], nb)
        assert result == "No notes found."

    def test_find_no_args(self):
        nb = NoteBook()
        result = find_note([], nb)
        assert "not enough" in result.lower()


class TestAddTag:
    def test_add_tag(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        result = add_tag(["1", "groceries"], nb)
        assert result == "Tag 'groceries' added to note 1."
        assert "groceries" in nb.find(1).tags

    def test_add_tag_stored_lowercase(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        add_tag(["1", "Groceries"], nb)
        assert "groceries" in nb.find(1).tags

    def test_add_multiple_tags(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        add_tag(["1", "groceries"], nb)
        add_tag(["1", "personal"], nb)
        assert nb.find(1).tags == ["groceries", "personal"]

    def test_add_tag_note_not_found(self):
        nb = NoteBook()
        result = add_tag(["99", "groceries"], nb)
        assert result == "Contact not found."

    def test_add_tag_no_args(self):
        nb = NoteBook()
        result = add_tag([], nb)
        assert "usage" in result.lower()

    def test_add_tag_missing_tag_arg(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        result = add_tag(["1"], nb)
        assert "usage" in result.lower()


class TestFindByTag:
    def test_find_by_tag(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        nb.add_note("Work", "Finish report")
        nb.find(1).tags.append("groceries")
        nb.find(2).tags.append("work")
        result = find_by_tag(["groceries"], nb)
        assert "Shopping" in result
        assert "Work" not in result

    def test_find_by_tag_case_insensitive(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        nb.find(1).tags.append("Groceries")
        result = find_by_tag(["groceries"], nb)
        assert "Shopping" in result

    def test_find_by_tag_multiple_matches(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        nb.add_note("Errands", "Pick up dry cleaning")
        nb.find(1).tags.append("personal")
        nb.find(2).tags.append("personal")
        result = find_by_tag(["personal"], nb)
        assert "Shopping" in result
        assert "Errands" in result

    def test_find_by_tag_no_match(self):
        nb = NoteBook()
        nb.add_note("Shopping", "Buy milk")
        nb.find(1).tags.append("groceries")
        result = find_by_tag(["work"], nb)
        assert "No notes found with tag 'work'." == result

    def test_find_by_tag_no_args(self):
        nb = NoteBook()
        result = find_by_tag([], nb)
        assert "not enough" in result.lower()


class TestSortByTag:
    def test_sort_by_tag_empty(self):
        nb = NoteBook()
        assert sort_by_tag([], nb) == "No notes saved."

    def test_sort_by_tag_order(self):
        nb = NoteBook()
        nb.add_note("Work", "Finish report")
        nb.add_note("Shopping", "Buy milk")
        nb.add_note("Travel", "Book hotel")
        nb.find(1).tags.append("work")
        nb.find(2).tags.append("groceries")
        nb.find(3).tags.append("adventure")
        result = sort_by_tag([], nb)
        assert result.index("adventure") < result.index("groceries") < result.index("work")

    def test_sort_by_tag_untagged_last(self):
        nb = NoteBook()
        nb.add_note("Tagged", "Has a tag")
        nb.add_note("Untagged", "No tag here")
        nb.find(1).tags.append("alpha")
        result = sort_by_tag([], nb)
        assert result.index("Tagged") < result.index("Untagged")
        assert "--- No tags ---" in result

    def test_sort_by_tag_all_untagged(self):
        nb = NoteBook()
        nb.add_note("First", "No tag")
        nb.add_note("Second", "No tag either")
        result = sort_by_tag([], nb)
        assert "--- No tags ---" in result
        assert "First" in result
        assert "Second" in result

    def test_sort_by_tag_no_untagged_section_when_all_tagged(self):
        nb = NoteBook()
        nb.add_note("Work", "Report")
        nb.add_note("Shopping", "Milk")
        nb.find(1).tags.append("work")
        nb.find(2).tags.append("groceries")
        result = sort_by_tag([], nb)
        assert "--- No tags ---" not in result