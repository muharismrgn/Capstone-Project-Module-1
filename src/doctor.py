import os, csv
import pyinputplus as pyip
import tabulate as tabl
from datetime import date, timedelta, time

def clear_screen():
    """
    Function to clear the screen
    """   
    os.system('cls' if os.name == 'nt' else 'clear')

def add_doctor(database):
    """Function to add new doctor to database

    Args:
        database (dict): Doctors database

    Returns:
        dict: Lastest update database
    """
    # Input new data
    idx = len(database) # Assign index by length of database
    # NIP length must be 5
    nip = ''
    while len(str(nip)) != 5:
        # Input patient NIP
        nip = pyip.inputInt(prompt='Masukan Nomor Induk Pegawai(NIP) Dokter: ')
        if len(str(nip)) != 5: print('Panjang Nomor Induk Pegawai(NIP) harus 5 digit!')
    # Duplication check in database as primary 
    if nip in database:
        print('NIP sudah terdaftar!')
    # If data not exist, continue input data
    else:
        # Input doctor's name
        name = 'dr. ' + pyip.inputStr(prompt='Masukan Nama Lengkap: ', applyFunc=lambda x: x.title(), blockRegexes=[r'[0-9]'])
        # Input doctor's spesialist
        specialization = 'Dokter ' + pyip.inputStr(prompt='Masukan Spesialisasi: ', applyFunc=lambda x: x.title(), blockRegexes=[r'[0-9]'])
        # Init variable to store practice days
        practice_day =[]
        # Practice day must be less than or equal to 2
        while len(practice_day) < 2:
            # Choice practice day
            choice = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
            # Input practice day
            day = pyip.inputChoice(prompt='Masukan Hari Praktik Maks 2: ', choices=choice)
            # Check day input in variable practice days
            if day in practice_day:
                # If day in practice day already exist
                print('Hari praktik sudah dimasukan!')
                continue
            else:
                # Append to variable practice days
                practice_day.append(day)
            # When practice day reaches max limit
            if len(practice_day) == 2:
                break
            # Ask to add another practice days
            more = pyip.inputYesNo(prompt='Apakah ingin memasukan hari praktik lagi (y/n)?')
            if more == 'no':
                break
        # Formating practice days for table display
        practice_day = ', '.join(practice_day)
        # Input paractice hours start
        while True:
            practice_hours_start = pyip.inputDatetime(prompt='Masukkan Jam Mulai Praktik (contoh 08:00): ', formats=['%H:%M']).time()
            if practice_hours_start < time(7,0):
                print('Jam kerja mulai pukul 07:00 WIB')
            else:
                break
        # Input paractice hours End
        while True:
            practice_hours_end = pyip.inputDatetime(prompt='Masukkan Jam Praktik Selesai (contoh 14:00): ', formats=['%H:%M']).time()
            if practice_hours_end > time(15, 0):
                print('Jam kerja berakhir pukul 15:00 WIB')
            else:
                break
        # Practice hours formatting for table display
        practice_hours = f"{practice_hours_start.strftime('%H:%M')} s/d {practice_hours_end.strftime('%H:%M')} WIB"
        # Input new doctor price
        price = pyip.inputInt(prompt='Masukan Biaya Penanganan: ')
        # Confirm to save new data
        save = pyip.inputYesNo(prompt='Apakah anda ingin menyimpan data ini (yes/no)?: ')
        # Clear screen after response
        clear_screen()       
        if save == 'yes':
            # Database update after confirmation is yes
            database.update({nip: [idx, nip, name, specialization, practice_day, practice_hours, price]})
            print('Data berhasil disimpan!')
    return database

def show_doctor(database):
    # Title
    print('\nDAFTAR SELURUH DOKTER')
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

def search_doctor(database, col):
    """Function to search doctor data by a key or column

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
    # Input primay key to search for data
    if col == 'NIP':
        key=''
        while len(str(key)) != 5:
            # Input NIP as primary key
            key = pyip.inputInt(prompt=f'Masukan {col} yang dicari: ')
            if len(str(key)) != 5: print('Panjang Nomor Induk Kependudukan (NIK) harus 5 digit!')  
        # Search data in database
        if key in database:
            # If data found, append into data found variable
            data_found.append(database[key])
    # Search for data with name or phone number
    elif col == 'Nama Dokter' or col == 'Spesialisasi':
        index = 2 # Indexing for name
        if col == 'Spesialisasi':
            index = 3 # Indexing for spesialist
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

def update_doctor(database):
    """Function to change/update data doctor in the database

    Args:
        database (dict): Doctors database

    Returns:
        dict: Lastest update database
    """
    nip=''
    while len(str(nip)) != 5:
        # Search NIK as primary key for update data
        nip = pyip.inputInt(prompt='Masukan Nomor Induk Pegawai(NIP): ')
        if len(str(nip)) != 5: print('Panjang Nomor Induk Kependudukan (NIP) harus 5 digit!')
    if nip in database:
        # Show found data
        print(tabl.tabulate([database[nip]], database["column"], tablefmt='psql'), '\n')
        # Confirm to continue update
        continue_update = pyip.inputYesNo(prompt='Apakah anda ingin mengubah data ini (yes/no)?: ')
        # Clear screen after response
        clear_screen()
        if continue_update == 'yes':
            # Displays the data column you want to change
            choice = list(database.values())[0][1:]
            response = pyip.inputMenu(prompt=f'Pilih data yang ingin diubah:\n[1-{len(choice)}]\n', choices=choice, numbered=True)
            if response == 'NIP':
                while True:
                    # Iput new NIP
                    new = pyip.inputInt(prompt='Masukan Nomor Induk Pegawai(NIP) Dokter yang Baru: ')
                    if new in database: print('NIP sudah terdaftar!') # Duplicate primary key
                    elif len(str(new)) != 5: print('Panjang Nomor Induk Pegawai (NIP) harus 5 digit!') # Length NIK must be 5
                    else: break
            elif response == 'Nama Dokter':
                # Input doctor's name
                new = 'dr. ' + pyip.inputStr(prompt='Masukan Nama Lengkap: ', applyFunc=lambda x: x.title(), blockRegexes=[r'[0-9]'])
            elif response == 'Spesialisasi':
                # Input doctor's specialist
                new = 'Dokter ' + pyip.inputStr(prompt='Masukan Spesialisasi: ', applyFunc=lambda x: x.title(), blockRegexes=[r'[0-9]'])
            elif response == 'Hari Praktik':
                # Init variable to store practice days
                practice_day =[]
                # Practice day must be less than or equal to 2
                while len(practice_day) < 2:
                    # Choice practice day
                    day_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
                    # Input practice day
                    day = pyip.inputChoice(prompt='Masukan Hari Praktik (Maks 2): ', choices=day_list)
                    # Check day input in variable practice days
                    if day in practice_day:
                        # If day in practice day already exist
                        print('Hari praktik sudah dimasukan!')
                    else:
                        # Append to variable practice days
                        practice_day.append(day)
                    # When practice day reaches max limit
                    if len(practice_day) == 2:
                        break
                    # Ask to add another practice days
                    more = pyip.inputYesNo(prompt='Apakah ingin memasukan hari praktik lagi (y/n)?')
                    if more == 'no':
                        break
                # Formating practice days for table display
                new = ', '.join(practice_day)
            # Input new practice hours
            elif response == 'Jam Praktik':
                # Input paractice hours start
                while True:
                    practice_hours_start = pyip.inputDatetime(prompt='Masukkan Jam Mulai Praktik (contoh 08:00): ', formats=['%H:%M']).time()
                    if practice_hours_start < time(7,0):
                        print('Jam kerja mulai pukul 07:00 WIB')
                    else:
                        break
                # Input paractice hours End
                while True:
                    practice_hours_end = pyip.inputDatetime(prompt='Masukkan Jam Praktik Selesai (contoh 14:00): ', formats=['%H:%M']).time()
                    if practice_hours_end > time(15, 0):
                        print('Jam kerja berakhir pukul 15:00 WIB')
                    else:
                        break
                # Practice hours formatting for table display
                new = f"{practice_hours_start.strftime('%H:%M')} s/d {practice_hours_end.strftime('%H:%M')} WIB"
            elif response == 'Biaya':
                # Input new doctor price
                new = pyip.inputInt(prompt='Masukan Biaya Penanganan: ')
            # Confirm to save new change
            confirm = pyip.inputYesNo(prompt='Apakah anda ingin menyimpan data ini (yes/no)?: ')
            # Clear screen after response
            clear_screen()
            if confirm == 'yes':
                database[nip][choice.index(response)+1] = new
                # Change key in dict database
                # print(f'before database change : \n{database}')
                if response == 'NIK':
                   # Store database keys dan values into list
                    keys = list(database.keys())
                    vals = list(database.values())
                    # Get NIP index in keys list
                    index = keys.index(nip)
                     # Change old NIP value to new value
                    keys[index]=new
                     # Recreate dict database from keys list as keys and vals list as values
                    database = {keys[i]: vals[i] for i in range(len(keys))}
                    # print(f'latest database change : \n{database}')
                print('Data berhasil diubah')
                # Ask to change another one
                again = pyip.inputYesNo(prompt='Apakah anda ingin mengubah data lagi (y/n)?: ')
                if again == 'yes':
                    # Call self function with new database args
                    return update_doctor(database)
                return database
    else:
        # print(f'database change on else: \n{database}') #bug report
        print('NIP belum terdaftar!')
        return database

def delete_doctor(database):
    """Function to remove data doctor from the database

    Args:
        database (dict): Doctors database

    Returns:
        dict: Latest database
    """   
    while True:
        nip = pyip.inputInt(prompt='Masukan NIP yang ingin dihapus: ')
        # Input NIK's as primary key must be 5 digits
        if len(str(nip)) != 5: print('Panjang Nomor Induk Pegawai (NIP) Dokter harus 5 digit!')
        else : break
    # Checking NIK as 
    if nip in database:
        print(tabl.tabulate([database[nip]], database['column'], tablefmt='psql'), '\n')
        # Confirm to delete
        confirm = pyip.inputYesNo(prompt='Apakah anda ingin menghapus data ini (yes/no)?: ')
        clear_screen()
        if confirm == 'yes':
            # Delete NIP's entry from database
            del database[nip]
            print('Data berhasil dihapus!')
            # Update or new assign numbering/indexing column after remove
            for i, val in enumerate (database.values()):
                if val[0] == 'No': # Continue when condition i in column name/header not data
                    continue
                val[0] = i # Assign i to every val[0]
    else:
        # Data not found
        print('NIP belum terdaftar!')
    return database

def doctor_list(database):
    while True:
        # Choice in show doctor data menu
        choice = ['Lihat Seluruh Daftar Dokter', 'Cari Dokter Dengan NIP', 'Cari Dokter Dengan Nama', 'Cari Dokter Dengan Spesialisasi', 'Kembali ke Menu Kelola Dokter']
        # Display in show doctor data menu
        prompt = f'''
-------------------
-- Daftar Dokter --
-------------------
Pilih [1-{len(choice)}]
'''
        # Input for show doctor data menu you want display
        response = pyip.inputMenu(prompt=prompt, choices=choice, numbered=True)
        clear_screen()
        # Show entire list of doctor
        if response == 'Lihat Seluruh Daftar Dokter':
            show_doctor(database)
        # Search/show doctor by NIP as primay key
        elif response == 'Cari Dokter Dengan NIP':
            search_doctor(database, 'NIP')
        # Search/show doctor by name
        elif response == 'Cari Dokter Dengan Nama':
            search_doctor(database, 'Nama Dokter')
        # Search/show doctor by specialization
        elif response == 'Cari Dokter Dengan Spesialisasi':
            search_doctor(database, 'Spesialisasi')
        # Back to previous menu
        else :
            back = pyip.inputYesNo(prompt='Apakah anda ingin kembali ke menu kelola dokter (y/n)?')
            clear_screen()
            if back == 'yes':
                break