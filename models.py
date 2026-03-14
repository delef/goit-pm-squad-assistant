from collections import UserDict
from datetime import datetime, timedelta


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


# Stores birthday, validates DD.MM.YYYY format
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


# Stores email, validates that it contains @ and . after @
class Email(Field):
    def __init__(self, value):
        at_pos = value.find("@")
        if at_pos < 1 or "." not in value[at_pos:]:
            raise ValueError("Invalid email format.")
        super().__init__(value)


# Stores address as free text
class Address(Field):
    pass


# Represents a single contact with a name and list of phones
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

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

    # Add birthday to the contact
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # Add email to the contact
    def add_email(self, email):
        self.email = Email(email)

    # Add address to the contact
    def add_address(self, address):
        self.address = Address(address)

    def __str__(self):
        phones = "; ".join(str(p) for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "not set"
        email = str(self.email) if self.email else "not set"
        address = str(self.address) if self.address else "not set"
        return (
            f"Contact name: {self.name}, phones: {phones}, "
            f"birthday: {birthday}, email: {email}, address: {address}"
        )


# Address book that stores all contacts by name
class AddressBook(UserDict[str, "Record"]):
    # Add a record to the book
    def add_record(self, record):
        self.data[record.name.value.lower()] = record

    # Find a record by name, returns None if not found
    def find(self, name):
        return self.data.get(name.lower())

    # Delete a record by name, raises KeyError if not found
    def delete(self, name):
        key = name.lower()
        if key not in self.data:
            raise KeyError
        del self.data[key]

    # Search contacts by name, phone or email (case-insensitive)
    def search(self, query):
        query = query.lower()
        results = []
        for record in self.data.values():
            if query in record.name.value.lower():
                results.append(record)
            elif any(query in p.value for p in record.phones):
                results.append(record)
            elif record.email and query in record.email.value.lower():
                results.append(record)
        return results

    # Get contacts with birthdays in the next N days
    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday is None:
                continue
            bday = record.birthday.value.date().replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)
            if (bday - today).days <= days:
                congrats = bday
                if congrats.weekday() == 5:
                    congrats += timedelta(days=2)
                elif congrats.weekday() == 6:
                    congrats += timedelta(days=1)
                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congrats.strftime("%d.%m.%Y")
                })
        return upcoming


# Represents a single note with id, title, body, tags and creation date
class Note:
    def __init__(self, note_id, title, body):
        self.id = note_id
        self.title = title
        self.body = body
        self.tags = []
        self.created_at = datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        tags = ", ".join(self.tags) if self.tags else "—"
        return (
            f"[{self.id}] {self.title}\n"
            f"  Body: {self.body}\n"
            f"  Tags: {tags}\n"
            f"  Created: {self.created_at}"
        )


# Stores all notes, auto-increments IDs
class NoteBook:
    def __init__(self):
        self.notes = {}
        self.next_id = 1

    # Add a new note, returns the created note
    def add_note(self, title, body):
        note = Note(self.next_id, title, body)
        self.notes[self.next_id] = note
        self.next_id += 1
        return note

    # Find a note by ID, returns None if not found
    def find(self, note_id):
        return self.notes.get(note_id)

    # Delete a note by ID, raises KeyError if not found
    def delete(self, note_id):
        if note_id not in self.notes:
            raise KeyError
        del self.notes[note_id]
