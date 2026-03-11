from collections import UserDict


# Base class for all fields (name, phone, etc.)
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Stores contact name, no extra validation needed
class Name(Field):
    pass


# Stores phone number, validates that it is exactly 10 digits
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)


# Represents a single contact with a name and list of phones
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # Add a new phone to the contact
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Remove a phone by value
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    # Replace an existing phone with a new one
    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone {old_phone} not found.")

    # Find a phone object by value, returns None if not found
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join(str(p) for p in self.phones)
        return f"Contact name: {self.name}, phones: {phones}"


# Address book that stores all contacts by name
class AddressBook(UserDict):
    # Add a record to the book
    def add_record(self, record):
        self.data[record.name.value] = record

    # Find a record by name, returns None if not found
    def find(self, name):
        return self.data.get(name)

    # Delete a record by name, raises KeyError if not found
    def delete(self, name):
        if name not in self.data:
            raise KeyError
        del self.data[name]
