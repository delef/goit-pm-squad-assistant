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
