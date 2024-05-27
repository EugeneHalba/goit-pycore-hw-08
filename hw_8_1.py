import pickle
from collections import UserDict
from datetime import datetime, timedelta
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
# create decorator
def input_error (func):
    def inner(*args,**kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError,TypeError):
            return "Enter the argument for the command"
        
    return inner
# create decorator

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
        def __init__(self, value):
            if not value.isalpha():
                raise ValueError('The name must contain only letters')
            super().__init__(value)
   

class Phone(Field):
        def __init__(self, value):
            if not value.isdigit() or len(value) != 10:
                raise ValueError ('Phone mast contain only numbers and 10 digits')
            super().__init__(value)
		
class Birthday(Field):
    def __init__(self,value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y" ).date()
            self.value = value
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthdays = []
        
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def add_birthday (self, birthday):
        self.birthdays.append(Birthday(birthday))

    def edit_phone(self, old_phone, new_phone):
        found = False
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone:
                try:
                    # Create a new Phone object and assign its value
                    self.phones[idx] = Phone(new_phone)
                    found = True
                    break
                except ValueError as e:
                    # Raise the ValueError from the Phone constructor
                    raise ValueError(str(e))
        if not found:
            raise ValueError('Old number not found')
    
    def find_phone (self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return "Number is not exist"
                
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {'; '.join(b.value for b in self.birthdays)}"


class AddressBook(UserDict):
   
   

    def add_record(self, record):
        if record.name.value in self.data:
            self.data[record.name.value].pnone.extend(record.phones)
        else:
            self.data[record.name.value] = record

    def find (self, name):
        return self.data.get(name)
    
    
    
    def delete (self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError ('Record is not found')        

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, new_phone, *_ = args
    record = book.find(name)
    if record:
        old_phone = record.phones[0].value if record.phones else None
        if old_phone:
            record.edit_phone(old_phone, new_phone)
            return "Contact updated."
        else:
            return "No phone number to update."
    else:
        return "Contact not found"

@input_error
def find_contact (args, book:AddressBook):
    name = args [0]
    if name in book:
        return book[name]
    else:
        return "contact does not exist"
@input_error
def show_all (args, book: AddressBook): 
    all_contacts = []
    for name, record in book.items():
        all_contacts.append(str(record))
    return '\n'.join(all_contacts)

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if birthday:
        record.add_birthday(birthday)
    return message

@input_error
def show_birthday (args, book:AddressBook):
    name = args [0]
    if name in book:
        return book[name]
    else:
        return "contact does not exist"

@input_error
def show_birthdays (book: AddressBook, days = 7): 
    all_birthdays = []
    today = datetime.today().date()

    for name, record in book.items():
        for birthday_field in record.birthdays:
            
            birthday_date = datetime.strptime(birthday_field.value, "%d.%m.%Y").date()    
            birthday_this_year = birthday_date.replace(year=today.year)  
            delta_days = (birthday_this_year - today).days
            
            if 0 <= delta_days <= days:
                all_birthdays.append(f"{name} has a birthday on {birthday_this_year.strftime('%d.%m.%Y')}")
    
    return '\n'.join(all_birthdays)

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 

def main():
    book = load_data()

    # book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Adress Book was saved. Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            message = add_contact(args, book)
            print (message) 
       
        elif command == "change":
            message = change_contact(args, book)
            print (message)
        
        elif command == "phone":
            message = find_contact(args, book)
            print (message)
        
        elif command == "all":
            message = show_all (args, book)
            print (message)

        elif command == "add-birthday":
            message = add_birthday (args, book)
            print (message)
        

        elif command == "show-birthday":
            message = show_birthday(args,book)
            print (message)

        elif command == "birthdays":
            message = show_birthdays(book)
            print (message)

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
