from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value.isdigit() or len(value) != 10:
            raise ValueError ('Номер не валідний')
        
             
class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        

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
         
         