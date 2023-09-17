import os, csv
import pyinputplus as pyip
import tabulate as tabl
from datetime import date, timedelta

def clear_screen():
    """
    Function to clear the screen
    """    
    os.system('cls' if os.name == 'nt' else 'clear')

def add_patient(database):
    """Function to add new patient to database

    Args:
        database (dict): Patients database

    Returns:
        dict: Lastest update database
    """
    # Input new data
    idx = len(database) # Assign index by length of database
    # NIK length must be 5
    nik = ''
    while len(str(nik)) != 5:
        # Input patient NIK
        nik = pyip.inputInt(prompt='Masukan Nomor Induk Kependudukan(NIK): ')
        if len(str(nik)) != 5: print('Panjang Nomor Induk Kependudukan(NIK) harus 5 digit!')
    # Duplication check in database as primary key
    if nik in database:
        print('NIK sudah terdaftar!')
    # If data not exist, continue input data
    else:
        # Input patient name
        name = pyip.inputStr(prompt='Masukan Nama Lengkap: ', applyFunc=lambda x: x.title(), blockRegexes=[r'[0-9]'])
        while True:
            # Input patient birthday
            birth = pyip.inputDate(prompt='Masukan Tanggal Lahir (contoh :01-01-1990): ', formats = ('%d-%m-%Y',))
            # Validation for input patient birthday, the date of birth cannot be later than today or more than 80 years earlier
            if birth > date.today() or birth < date.today() - timedelta(days=365*80): 
                print('Tanggal yang dimasukan tidak valid!')
            else: break
        # Input patient gender
        gender = pyip.inputChoice(prompt='Masukan Jenis Kelamin (L/P): ', choices=['L', 'P'])
        # Input patient address
        address = pyip.inputStr(prompt='Masukan Alamat: ', applyFunc=lambda x: x.title())
        # Length of phone number must be between 11 and 13
        phone=''
        while len(phone) not in [11,12,13]:
            # Input patient phone number
            phone = '0' + str(pyip.inputInt(prompt='Masukan Nomor Telepon: '))
            if len(phone) > 13: print('Panjang No. Telepon tidak bisa lebih dari 13!')
            elif len(phone) < 11: print('Panjang No. Telepon tidak bisa kurang dari 11!')
        # Confirmation to save
        save = pyip.inputYesNo(prompt='Apakah anda ingin menyimpan data ini (yes/no)?: ')
        # Clear the screen after response
        clear_screen()
        if save == 'yes':
            # Database update after confirmation is yes
            database.update({nik: [idx, nik, name, birth, gender, address, phone]})
            print('Data berhasil disimpan!')
    return database

def show_patient(database):
    """ Function to display all data

    Args:
        database (dict): Patient database
    """   
    # Title
    print('\nDAFTAR SELURUH PASIEN')
    # Header for columns
    header = database['column']
    # Data collection
    data = list(database.values())[1:]
    # Check data exists
    if data:
        # Display the data
        print(tabl.tabulate(data, header, tablefmt='psql'), '\n') 
    else:
        # Not found or empty
        print('Data masih kosong!')
    return database

def search_patient(database, col):    
    """Function to search patient data by a key or column

    Args:
        database (dict): Patient database
        col (str): keyword or column searched
    """    
    # Header for columns   
    header = database['column']
    # Data collection
    data = list(database.values())[1:]
    # Init variable for found data
    data_found = []
    # Search for data with primary key
    if col == 'NIK':
        key = ''
        # Length of NIK must be 5
        while len(str(key)) != 5:
            # Input NIK as primary key
            key = pyip.inputInt(prompt=f'Masukan {col} yang dicari: ')
            if len(str(key)) != 5: print('Panjang Nomor Induk Kependudukan (NIK) harus 5 digit!')
        # Search data in database
        if key in database:
            # If data found, append into data found variable
            data_found.append(database[key])
    # Search for data with name or phone number
    elif col == 'Nama' or col == 'No. Telepon':
        index = 2 # Indexing for name
        if col == 'No. Telepon':
            index = 6 # Indexing for phone number
        # Input keyword you are looking for
        key = pyip.inputStr(prompt=f'Masukan {col} yang dicari: ')
        # Search for data
        for val in data:
            # Name and val into lower
            if key.lower() in val[index].lower():
                # If data found, append into data found variable
                data_found.append(val)

    if data_found:
        # Display results
        print(tabl.tabulate(data_found, header, tablefmt='psql'), '\n')
    else:
        # Data not found
        print('Data tidak ditemukan!')

def update_patient(database):
    """Function to change/update data patient in the database

    Args:
        database (dict): Patients database

    Returns:
        dict: Lastest update database
    """
    nik =''
    # NIK length must be 5
    while len(str(nik)) != 5:
        # Search NIK as primary key for update data
        nik = pyip.inputInt(prompt='Masukan Nomor Induk Kependudukan(NIK) yang ingin diubah: ')
        if len(str(nik)) != 5: print('Panjang Nomor Induk Kependudukan (NIK) harus 5 digit!')
    if nik in database:
        print(database)
        # Show found data
        print(tabl.tabulate([database[nik]], database["column"], tablefmt='psql'), '\n')
        # Confirm to continue update
        continue_update = pyip.inputYesNo(prompt='Apakah anda ingin mengubah data ini (yes/no)?: ')
        # Clear screen after response
        clear_screen()
        if continue_update == 'yes':
            # Displays the data column you want to change
            choice = list(database.values())[0][1:]
            response = pyip.inputMenu(prompt=f'Pilih data yang ingin diubah:\nPilih [1-{len(choice)}]\n', choices=choice, numbered=True)
            if response == 'NIK':
                while True:
                    # Iput new NIK
                    new = pyip.inputInt(prompt='Masukan Nomor Induk Kependudukan(NIK) Baru: ')
                    if new in database: print('NIK sudah terdaftar!') # Duplicate primary key
                    elif len(str(new)) != 5: print('Panjang Nomor Induk Kependudukan (NIK) harus 5 digit!') # Length NIK must be 5
                    else: break
            elif response == 'Nama':
                # Input new name
                new = pyip.inputStr(prompt='Masukan Nama Lengkap: ', applyFunc=lambda x: x.title(), blockRegexes=[r'[0-9]'])
            elif response == 'Tanggal Lahir':
                while True:
                    # Input new birth date
                    new = pyip.inputDate(prompt='Masukan Tanggal Lahir (contoh :01-01-1990): ', formats = ('%d-%m-%Y',))
                    # Validation for input patient birthday, the date of birth cannot be later than today or more than 80 years earlier
                    if new > date.today() or new < date.today() - timedelta(days=365*80):
                        print('Tanggal yang dimasukan tidak valid!')
                    else:
                        break
            elif response == 'Jenis Kelamin':
                # Input new gender
                new = pyip.inputChoice(prompt='Masukan Jenis Kelamin (L/P): ', choices=['L', 'P'])
            elif response == 'Alamat':
                # Input new address
                new = pyip.inputStr(prompt='Masukan Alamat: ', applyFunc=lambda x: x.title())
            elif response == 'Nomor Telepon':
                new = ''
                # Length of phone number must be between 11-13
                while len(new) not in [11,12,13]:
                    # Input new phone number
                    new = '0' + str(pyip.inputInt(prompt='Masukan Nomor Telepon: '))
                    if len(new) > 13: print('Panjang No. Telepon tidak bisa lebih dari 13!')
                    elif len(new) < 11: print('Panjang No. Telepon tidak bisa kurang dari 11!')
            # Confirm to save new change
            confirm = pyip.inputYesNo(prompt='Apakah anda ingin menyimpan data ini (y/n)?: ')
            # Clear screen after response
            clear_screen()
            if confirm == 'yes':
                # Update new change 
                database[nik][choice.index(response)+1] = new
                # Change key in dict database
                print(f'before database change : \n{database}')
                if response == 'NIK':
                    # Store database keys dan values into list
                    keys = list(database.keys())
                    vals = list(database.values())
                    # Get NIK index in keys list
                    index = keys.index(nik)
                    # Change old NIK value to new vale
                    keys[index]=new
                    # Recreate dict database from keys list as keys and vals list as values
                    database = {keys[i]: vals[i] for i in range(len(keys))}
                print(f'latest database change : \n{database}')
                print('Data berhasil diubah')
            # Ask to change another one
            again = pyip.inputYesNo(prompt='Apakah anda ingin mengubah data lagi (y/n)?: ')
            if again == 'yes':
                # Call self function with new database args
                update_patient(database)
    else:
        print(f'database change on else: \n{database}') #bug report
        print('NIK belum terdaftar!') 
    return database
    
def delete_patient(database):
    """Function to remove patient data entry from the database

    Args:
        database (dict): Patients database

    Returns:
        dict: Latest database
    """    
    # Input NIK as primary key for delete operation
    while True:
        nik = pyip.inputInt(prompt='Masukan NIK yang ingin dihapus: ')
        # Input NIK's as primary key must be 5 digits
        if len(str(nik)) != 5: print('Panjang Nomor Induk Kependudukan (NIK) harus 5 digit!')
        else : break
    # Checking NIK as primary key in database
    if nik in database:
        # Display NIK's entry as primary key
        print(tabl.tabulate([database[nik]], database['column'], tablefmt='psql'), '\n')
        # Confirm to delete
        confirm = pyip.inputYesNo(prompt='Apakah anda ingin menghapus data ini (yes/no)?: ')
        # Clear screen after response
        clear_screen()
        if confirm == 'yes':
            # Delete NIK's entry from database
            del database[nik]
            print('Data berhasil dihapus!')
            # Update or new assign numbering/indexing column after remove
            for i, val in enumerate (database.values()):
                if val[0] == 'No': # Continue when condition i in column name/header not data
                    continue
                val[0] = i # Assign i to every val[0]
    else:
        # Data not found
        print('NIK belum terdaftar!')   
    return database

def patient_list(database):
    """Function to display a menu that displays list patient data

    Args:
        database (dict): Patient database
    """    
    while True:
        # Choice in show patient data menu
        choice = ['Lihat Seluruh Daftar Pasien', 'Cari Pasien Dengan NIK', 'Cari Pasien Dengan Nama', 'Cari Pasien Dengan Nomor Telepon', 'Kembali ke Menu Kelola Pasien']
        # Display in show patient data menu
        prompt = f'''
-------------------
-- Daftar Pasien --
-------------------
Pilih [1-{len(choice)}]
'''
        # Input for show patient data menu you want display
        response = pyip.inputMenu(prompt=prompt, choices=choice, numbered=True)
        # Clear screen
        clear_screen()
        # Show entire list of patient
        if response == 'Lihat Seluruh Daftar Pasien':
            show_patient(database)
        # Search/show patient by NIK as primary key
        elif response == 'Cari Pasien Dengan NIK':
            search_patient(database, 'NIK')
        # Search/show patient by name
        elif response == 'Cari Pasien Dengan Nama':
            search_patient(database, 'Nama')
        # Search/show patient by phone number
        elif response == 'Cari Pasien Dengan Nomor Telepon':
            search_patient(database, 'No. Telepon')
        # Back to previous menu
        else :
            back = pyip.inputYesNo(prompt='Apakah anda ingin kembali ke menu kelola pasien (y/n)?')
            clear_screen()
            if back == 'yes':
                break