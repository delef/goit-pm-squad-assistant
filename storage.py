import pickle

from models import AddressBook


# Save address book to a file using pickle
def save_data(book, filename="assistant_data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


# Load address book from file, or return a new one if file doesn't exist
def load_data(filename="assistant_data.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
