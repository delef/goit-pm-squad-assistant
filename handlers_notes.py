from decorators import input_error
from models import NoteBook


# Add a new note with title and body (use -- to separate multi-word title from body)
@input_error("Note")
def add_note(args, notebook: NoteBook):
    if "--" in args:
        sep = args.index("--")
        title = " ".join(args[:sep])
        body = " ".join(args[sep + 1:])
    else:
        title, *body_parts = args
        body = " ".join(body_parts)
    note = notebook.add_note(title, body)
    return f"Note added with ID {note.id}."


# Show all saved notes
def show_notes(notebook: NoteBook):
    if not notebook.notes:
        return "No notes saved."
    return "\n".join(str(note) for note in notebook.notes.values())


# Edit the body of an existing note by ID
@input_error("Note")
def edit_note(args, notebook: NoteBook):
    note_id, *body_parts = args
    note = notebook.find(int(note_id))
    if note is None:
        raise KeyError
    note.body = " ".join(body_parts)
    return "Note updated."


# Delete a note by ID
@input_error("Note")
def delete_note(args, notebook: NoteBook):
    note_id, *_ = args
    notebook.delete(int(note_id))
    return "Note deleted."


# Search notes where title or body contains query (case-insensitive)
@input_error
def find_note(args, notebook: NoteBook):
    query, *_ = args
    matches = [
        note for note in notebook.notes.values()
        if query.lower() in note.title.lower() or query.lower() in note.body.lower()
    ]
    if not matches:
        return "No notes found."
    return "\n".join(str(note) for note in matches)


# Add a tag to a note by ID (no duplicates allowed)
@input_error("Notes")
def add_tag(args, notebook: NoteBook):
    if len(args) < 2:
        raise ValueError("Usage: add-tag [id] [tag]")
    note_id, tag, *_ = args
    note = notebook.find(int(note_id))
    if note is None:
        raise KeyError
    tag = tag.lower()
    if tag in note.tags:                          # fix 1: перевірка дубліката
        return f"Tag '{tag}' already exists on note {note_id}."
    note.tags.append(tag)
    return f"Tag '{tag}' added to note {note_id}."


# Find all notes that contain a given tag (case-insensitive)
@input_error
def find_by_tag(args, notebook: NoteBook):
    tag, *_ = args
    matches = [
        note for note in notebook.notes.values()
        if tag.lower() in [t.lower() for t in note.tags]
    ]
    if not matches:
        return f"No notes found with tag '{tag}'."
    return "\n".join(str(note) for note in matches)


# Show all notes sorted by their first tag alphabetically; untagged notes last
def sort_by_tag(args, notebook: NoteBook):           # fix 2: прибрано @input_error
    if not notebook.notes:
        return "No notes saved."
    tagged = [note for note in notebook.notes.values() if note.tags]
    untagged = [note for note in notebook.notes.values() if not note.tags]
    tagged.sort(key=lambda note: note.tags[0].lower())
    sections = []
    if tagged:
        sections.append("\n".join(str(note) for note in tagged))
    if untagged:
        sections.append("--- No tags ---\n" + "\n".join(str(note) for note in untagged))
    return "\n".join(sections)