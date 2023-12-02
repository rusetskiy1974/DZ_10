from collections import UserDict
from datetime import datetime
from faker import  Factory
import pickle
import os
import re
import msvcrt



fake = Factory.create('uk_UA')
users = []
help_description = {'generate': 'Створення рандомного набору користувачів. \n Формат вводу:   generate n (n - кількість користувачів)',
                    'add entry': 'Добавлення користувача з консолі. \n Формат вводу:  add entry name (може бути тільки Імя або Імя Прізвище)',
                    'add birthday': 'Добавлення до контакту дати народження. \n формат вводу: add birthday name YYYY-dd-mm',
                    'find': 'Пошук контактів по введеній строці. \n Формат вводу:  find string',
                    'add phone': 'Добавлення до контакту номера телефону. \n Формат вводу: add phone name phone (phone - 10 цифр)',
                    'remove phone': 'Видалення з контакту номера телефону. \n Формат вводу: remove phone name phone (phone - 10 цифр)',
                    'show all': 'Виведення всього списку контактів з n записів за одну ітерацію. \n Формат вводу: show all n (n - ціле число)',
                    'exit': 'Завершення роботи , вихід з довідника. \n Формат вводу: exit'} 



class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self,  value):
        self.__value = value
        
    def __str__(self):
        return str(self.value)

class Name(Field):

    @Field.value.setter
    def value(self, value: str):
        if value.startswith('пані') or value.startswith('пан'):
            value = value.replace('пані', '').replace('пан', '').strip()
        if value.replace(' ', '').isalpha():
            self._Field__value = value
        else:
            raise ValueError  ("Ім'я не коректне")  
        
    

class Phone(Field):
    
    @Field.value.setter
    def value(self, value: str):
        if value.isdigit() and len(value) == 10:
            self._Field__value = value
        else: 
            raise  ValueError ('Номер не валідний')
            
    
       
class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        try:
            if datetime.strptime(value, '%Y-%m-%d'):
                self._Field__value = value
        except:
            raise ValueError ('Не правильний формат дати')    
    
                 
class Record:

    def __init__(self, name, birthday: Birthday = None):
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
        raise  IndexError('Номер відсутній')  
    

    def edit_phone(self, phone, new_phone):
        for n, i in enumerate(self.phones):
                if i.__str__() == phone:
                    self.phones[n] = Phone(new_phone)
                    return
        raise IndexError ('Номер відсутній' )   
                
         
    def find_phone(self, phone_number:str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return   

    def days_to_birthday(self):
        if self.birthday:
            self.birthday = datetime.strptime(str(self.birthday) , '%Y-%m-%d').date()
            self.birthday = self.birthday.replace(year = datetime.now().year)
            if self.birthday >= datetime.now().date():
                return   (self.birthday - datetime.now().date()).days
            else:
                return (self.birthday.replace(year=datetime.now().year+1) - datetime.now().date()).days

    def __repr__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return self.data[record.name.value]

    def find(self, name: Name):
        return self.data.get(name, None)

    def delete(self, name: Name):
        self.data.pop(name, None)

    def iterator(self, item_number ):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}\n'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
        yield  result  

    def dump(self, file_name):
        with open(file_name, 'wb' ) as file:
            pickle.dump(self.data, file)

    def load(self, file_name):
        if not os.path.exists(file_name):
            return
        with open(file_name, 'rb') as file:
            self.data = pickle.load(file)
            

#^^^^^^^^^^^^^^^^^ Класи ^^^^^^^^^^^^^^^^^^^^^^^^^^^


def valid_phone(phone_number):
    phone_number =  phone_number.replace('+','').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    if len(phone_number) == 10:
        return phone_number
    else:
        return False
     
def create_users(fake, users: list, n ):   # Генерування рандомного списку користівачів
    for _ in range(n):
        user = {}
        user['name'] = fake.name()
        user['birthday'] = fake.date()
        val = valid_phone(fake.phone_number())
        while True:
            if val:
                user['phone_number'] = val
                break
            else:
                val = valid_phone(fake.phone_number()) 
        users.append(user)
    return users

def create_instans(list_users):             # Створення екземплярів користувачів
    for user in list_users:
        record = Record(user['name'], user['birthday'])
        record.add_phone(user['phone_number'])
        book.add_record(record)

# -----------------------------------------------------------------------------------------------------
        
def input_error(func):    # Функція декоратор приймає функцію із hundlera і  обробляє винятки
     
    def inner(volume):
        try:
            return func(volume)
            
        except ValueError:
            return 'Incorrect data format'
        except KeyError:
            return 'Give me correct value please'
        except IndexError:
            return  'Give me correct name and phone please'
         
    return inner   

# Функціі обробки команд hundlera


@input_error
def add_entry(vol):
    record = Record(vol)
    book.add_record(record)
    return 'Ok'
     
@input_error     
def add_birthday(vol ):
    vol_name, vol_data = parser_operand(vol)
    if  book.data[vol_name]:
        book.data[vol_name].birthday = Birthday(vol_data)
    return 'Ok'  

@input_error    
def add_phone(vol):
    vol_name, vol_data = parser_operand(vol)
    if  book.data[vol_name]:
        book.data[vol_name].add_phone(vol_data)
    return 'Ok'    

@input_error    
def remove_phone(vol):
    vol_name, vol_data = parser_operand(vol)
    if  book.data[vol_name]:
        book.data[vol_name].remove_phone(vol_data)
    return 'Ok'         
       
def find(vol):
    for record in book.data.keys():
        if record.find(vol) != -1:
           print(book.data[record], end = '\n')
        else:
            for phone in book.data[record].phones:
                if str(phone).find(vol) != -1:
                    print(book.data[record], end = '\n')
                    break
    return 'Ok'                

@input_error     
def output_all_entry(vol=1):
    iter = book.iterator(int(vol))
    for rec in iter:
        print(rec)
        msvcrt. getch()
    return 'Ok'    
    
@input_error    
def bye(vol = None):
    if not vol:  
        return "Good bye!"
    raise ValueError


@input_error
def generate(volume):
    if volume.isdigit() and int(volume) > 0:
        create_instans(create_users(fake, users, int(volume)))
        return 'Ok'
    raise ValueError   
 
@input_error
def help(vol = None):
    if not vol:
        print( 'Actual command:')
        for key in hundler:
            print (f'{key}... ', end = ' ')
        return '' 
    else:
        print (help_description[vol])  
        return '' 
    # raise ValueError


     

hundler = {'help': help, 'generate': generate , 'add entry' : add_entry,
            'add birthday' : add_birthday,  'find' : find, 'add phone' : add_phone,
              'remove phone' : remove_phone ,'show all' : output_all_entry, 'exit' : bye}



def parser_hundler(str):        #Функція Парсер команд
    key_hundler = str.lower()
    for key in hundler.keys():
        if key_hundler.startswith(key):
            result = re.search(key, key_hundler)
            second_index = result.span()[1]
            if key_hundler == key or str[second_index] == ' ':
                return [key, str[second_index:].strip()]   
            

def parser_operand(str):         #Функція Парсер операндів
    vol_list = list(str.split())
    
    if len(vol_list) == 3:
        vol_name = ' '.join(vol_list[0:2])
        vol_data = vol_list[2]
    else:
        vol_name = vol_list[0]
        vol_data = vol_list[1]                    
    return [vol_name, vol_data]

# -------------------------------------------------------------------------------------------------------

def main():
    while True:
        print ('>>>', end = '')
        hundler_string = input ()
        
        command_str = parser_hundler(hundler_string)

         
        if command_str:
            command = hundler.get(command_str[0])
            operand = command_str[1]
               
            if command == bye and not operand:
                print (command(operand))
                book.dump('data.bin')
                break
             
            else:
                print(command(operand))
        else:
            print ('Command is missing')            
         

if __name__ == '__main__':
    
    book = AddressBook()
    book.load('data.bin')
    print('Enter help for Help')
    main()

    