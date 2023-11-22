from collections import UserDict

from datetime import datetime, timedelta




class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if isinstance(value, str):
            self.__value = value
        else:
            raise Exception ('Wrong value')    
        
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value.isdigit() or len(value) != 10:
            raise ValueError ('Номер не валідний')
        
class Birthday(Field):
    pass
                 
class Record:

    def __init__(self, name, birthday : Birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday
        

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)
        
           

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.__str__() == phone_number:
                return self.phones.remove(phone)
        raise  ValueError('Номер відсутній')  
    

    def edit_phone(self, phone, new_phone):
        for n, i in enumerate(self.phones):
                if i.__str__() == phone:
                    self.phones[n] = Phone(new_phone)
                    return
        raise ValueError ('Номер відсутній' )   
                
         
    def find_phone(self, phone_number:str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return   

    def days_to_birthday(self):
        if self.birthday:
            self.birthday = datetime.strptime(str(self.birthday) , '%Y.%m.%d').date()
            self.birthday = self.birthday.replace(year = datetime.now().year)
            if self.birthday >= datetime.now().date():
                return   (self.birthday - datetime.now().date()).days
            else:
                return (self.birthday.replace(year=datetime.now().year+1) - datetime.now().date()).days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return self.data[record.name.value]

    def find(self, name: Name):
        return self.data.get(name, None)

    def delete(self, name: Name):
        self.data.pop(name, None)

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record} '
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''    
         

d = '2023.11.10'
bd = Birthday(d)

# print (bd)
book = AddressBook()

# Створення запису для John
john_record = Record("John", bd)
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
print(john_record.days_to_birthday())

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

