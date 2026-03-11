import pickle

from models import AddressBook, NoteBook


# Save all data (address book + notebook) to a file using pickle
def save_data(book, notebook, filename="assistant_data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump({"book": book, "notebook": notebook}, f)


# Load all data from file, or return new instances if file doesn't exist
def load_data(filename="assistant_data.pkl"):
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            # Support old format where only book was saved
            if isinstance(data, AddressBook):
                return data, NoteBook()
            return data["book"], data["notebook"]
    except FileNotFoundError:
        return AddressBook(), NoteBook()
