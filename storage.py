import pickle
from pathlib import Path

from models import AddressBook, NoteBook

FILENAME = Path.home() / "assistant_data.pkl"


# Save all data to a file using pickle
def save_data(book, notebook):
    with open(FILENAME, "wb") as f:
        pickle.dump({"book": book, "notebook": notebook}, f)


# Load all data from file, or return new instances if file doesn't exist
def load_data():
    try:
        with open(FILENAME, "rb") as f:
            data = pickle.load(f)
            return data["book"], data["notebook"]
    except FileNotFoundError:
        return AddressBook(), NoteBook()
