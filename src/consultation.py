import os, csv
import pyinputplus as pyip
import tabulate as tabl
from datetime import datetime, timedelta

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_patient_db():
    """Function to get the patients database

    Returns:
        dict: Patients database
    """    
    path = 'data\patient.csv'
    # Init database
    database = {}
    with open(path, 'r') as file:
        # Read the data from csv file
        dataReader = csv.reader(file, delimiter=";")
        # Input row into dictionary
        for i, row in enumerate(dataReader):
            # For header
            if i == 0:
                header = row
                database.update({"column": header})
                continue
            # For data
            idx, nik, name, birth, sex, address, phone = row
            database.update({int(nik): [int(idx), int(nik), name, birth, sex,  address, phone]})
    return database

def get_doctor_db():
    """Function to get the doctor database

    Returns:
        dict: Doctors database
    """    
    path = 'data\doctor.csv'
    database = {}
    with open(path, 'r') as file:
        # Read the data from csv file
        dataReader = csv.reader(file, delimiter=";")
        # Input row into dictionary
        for i, row in enumerate(dataReader):
            # For header
            if i == 0:
                header = row
                database.update({"column": header})
                continue
            # For data
            idx, nip, name, specialization, practice_day, practice_hours, price = row
            database.update({int(nip): [int(idx), int(nip), name, specialization,  practice_day, practice_hours, int(price)]})
    return database

def get_idn_dayname(date):
    """Function to get indonesia day name

    Args:
        date(date): Consult day

    Returns:
        string: Indonesia dayname
    """   
    # Mapping for translating
    day_mapping = {
        'Monday': 'Senin',
        'Tuesday': 'Selasa',
        'Wednesday': 'Rabu',
        'Thursday': 'Kamis',
        'Friday': 'Jumat',
        'Saturday': 'Sabtu',
        'Sunday': 'Minggu',
    }
    # Get dayname
    dayname = date.strftime("%A")
    return day_mapping.get(dayname, '')

def get_queue(db, doctor_nip, consult_day):
    """Function to get/generate queue

    Args:
        db (dict): Consultation database
        doctor_nip (int): Doctor's nip
        consult_day (string): Consultation day

    Returns:
        int: consult's queue number
    """
    # Init queue value    
    queue = 1
    # Database's column names
    columns = list(db.values())[0]
    # Value's database
    vals = list(db.values())[1:]
    # Looping to check data that has the same consulting doctor and schedule
    for val in vals:
        # Find the same one, queue+1
        if doctor_nip == val[columns.index('NIP')] and consult_day == val[columns.index('Hari, Tanggal Konsultasi')]:
            queue += 1
    return queue

def add_consultation(database):
    """Function to add new consultation schedule

    Args:
        database (dict): Consultation database

    Returns:
        dict: Latest database
    """    
    # Get patient and doctor databases
    patient_db = get_patient_db()
    doctor_db = get_doctor_db()
    # Get index for the new consultation entry
    idx = len(database)
    while True:
        # Input NIK as primary key for delete operation
        while True:
            nik = pyip.inputInt(prompt='Masukan Nomor Induk Kependudukan(NIK) Pasien: ')
            # Input NIK's as primary key must be 5 digits
            if len(str(nik)) != 5: print('Panjang Nomor Induk Kependudukan (NIK) harus 5 digit!')
            else : break
        # Check if patient in patient database
        if nik in patient_db:
            # Get patient's name from NIK in patient database
            patient_name = list(patient_db[nik])[2]
            # Calculate patient's age from birth date
            birth = datetime.strptime((list(patient_db[nik])[3]), '%Y-%m-%d')
            today = datetime.today()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.month))
            print(f'{patient_name} - {age} Tahun')
            break
        else:
            # NIK is not found
            print('NIK belum terdaftar!')
    # Input and validate doctor's NIP
    while True:
        while True:
            nip = pyip.inputInt(prompt='Masukan Nomor Induk Pegawai(NIP) Dokter: ')
            # Input NIK's as primary key must be 5 digits
            if len(str(nip)) != 5: print('Panjang Nomor Induk Kependudukan (NIK) harus 5 digit!')
            else : break
        if nip in doctor_db:
            # Get doctor's name from NIP in doctor database
            doctor_name = list(doctor_db[nip])[2]
            # Get doctor's specialist from NIP in doctor database
            specialization = list(doctor_db[nip])[3]
            # Generate code for part of consultation id
            code_spes = ''.join(char[0] for char in specialization.split())
            print(f'{doctor_name} - {specialization}')
            print(f'Jadwal Praktik : {list(doctor_db[nip])[4]}')
            break
        else:
            # NIP is not found
            print('NIP belum terdaftar!')
    # Input and validate consultation date
    while True:
        date = pyip.inputDate(prompt='Masukan Tanggal Konsultasi (contoh :01-01-2023): ', formats = ('%d-%m-%Y',))
        # Function to get indonesia dayname
        dayname = get_idn_dayname(date)
        # Check if date is within the allowed range
        if date < (date.today() - timedelta(days=30)) or date > (date.today() + timedelta(days=30)):
            print('Tanggal konsultasi tidak bisa lebih dari 30 hari sebelum/setelah dari hari ini!')
        # Check if date matches doctor's schedule
        elif dayname not in list(doctor_db[nip])[4].split(', '):
            print('Tanggal konsultasi tidak sesuai dengan jadwal dokter!')
        else:
            date_format = date.strftime('%d-%m-%Y')
            # Consult date format
            consult_day = f'{dayname}, {date_format}'
            print(consult_day)
            break
    # Get the doctor's consultation time from the doctor database
    consult_time = list(doctor_db[nip])[5]
    # Input consultation status and determine the queue number
    if date < date.today():
        consult_status = pyip.inputMenu(prompt='Masukan Status Konsultasi: \n', choices=['Dibatalkan', 'Selesai'], numbered=True)
        queue = None
    elif date > date.today():
        consult_status = pyip.inputMenu(prompt='Masukan Status Konsultasi: \n', choices=['Menunggu Konfirmasi', 'Terjadwalkan', 'Dibatalkan'], numbered=True)
        queue = get_queue(database, nip, consult_day)
    else:
        consult_status = pyip.inputMenu(prompt='Masukan Status Konsultasi: \n', choices=['Terjadwalkan', 'Dibatalkan', 'Selesai'], numbered=True)
        queue = get_queue(database, nip, consult_day)
    # Get consultation price from the doctor database
    price = list(doctor_db[nip])[6]
    # Generate a unique consultation ID based on details as primary key
    consult_id = f'{code_spes}{doctor_name[4:6].upper()}{patient_name[:2].upper()}{str(nip)[-2:]}{str(nik)[-2:]}'
    # Confirm if user wants to save the consultation details
    save = pyip.inputYesNo(prompt='Apakah anda ingin menyimpan data ini (yes/no)?: ')
    # Clear screen after response
    clear_screen()
    if save == 'yes':
         # Add new the consultation details to the consultation database
        database.update({consult_id: [idx, consult_id, nik, patient_name, age, nip, doctor_name, specialization, consult_day, consult_time, consult_status, price, queue]})
        print('Data berhasil disimpan!')
    return database

def show_consultation(database):
    """ Function to display data

    Args:
        database (dict): Consultation database
    """   
    # Title
    print('\nJADWAL KONSULATASI PASIEN/DOKTER')
    # Header for columns
    header = database['column']
    # Data collection
    data = list(database.values())[1:]
    # Print collection of data
    print(tabl.tabulate(data, header, tablefmt='psql'), '\n')

def sort_date(database):
    """Function to sort schedule by date

    Args:
        database (dict): Consultation database

    Returns:
        dict: Sorted database by date
    """    
    # Extract column names (headers) from the database
    header = database['column']
    # Extract data entries (excluding the header) from the databas
    data = list(database.values())[1:]

    # Define a function to convert a data entry into a datetime object for sorting
    def to_datetime(param):
        """Function to convert a data entry into a datetime object

        Args:
            param (str): Consult day, practice time

        Returns:
            datetime: day and practice time
        """        
        # Extract the date and time from the data entry and combine them
        date_str = param[8].split(', ')[1] + ' ' + param[9].split()[0]
        # Convert the combined string into a datetime object
        return datetime.strptime(date_str, '%d-%m-%Y %H:%M')
    
    # Implementing Bubble Sort to sort the data based on datetime
    for i in range(len(data)-1):
        for j in range(i+1, len(data)):
            # Compare the datetime of two entries using the to_datetime function
            if to_datetime(data[i]) > to_datetime(data[j]):
                # Swap the two entries if they are out of order
                data[i], data[j] = data[j], data[i]
    # Display the sorted data using the tabulate 
    print(tabl.tabulate(data, header, tablefmt='psql'), '\n')

def search_consultation(database, col):
    """ Function to search patient data by a keyword

    Args:
        database (dict): Patient database
    """
     # Extract column names
    header = database['column']
    # Extract data entries 
    data = list(database.values())[1:]
    # Initialize a list to store data found
    data_found = []
    
    # Check if the given column is one of the searchable columns
    if col in ['Nama Pasien', 'Nama Dokter', 'Spesialis', 'Hari/Tanggal Konsultasi', 'Status Konsultasi']:
        # Mapping column names to column indexes
        col_idx = {'Nama Pasien': header.index('Nama Pasien'),
                   'Nama Dokter': header.index('Nama Dokter'),
                   'Spesialis': header.index('Spesialis'),
                   'Hari/Tanggal Konsultasi': header.index('Hari, Tanggal Konsultasi'),
                   'Status Konsultasi': header.index('Status Konsultasi')}
        # If searching by consultation status, provide a menu of options
        if col == 'Status Konsultasi':
            key = pyip.inputMenu(prompt=f'Masukan {col} yang dicari: \n', choices=['Menunggu Konfirmasi', 'Terjadwalkan', 'Dibatalkan', 'Selesai'], numbered=True)
        else :
            # Input a key to search for data
            key = pyip.inputStr(prompt=f'Masukan {col} yang dicari: ')
        # Search for data that matches
        for val in data:
            # Name and val into lower
            if key.lower() in val[col_idx[col]].lower():
                # Append data found to temporary variable
                data_found.append(val)

    if data_found:
        # Display data found
        print(tabl.tabulate(data_found, header, tablefmt='psql'), '\n')
    else:
        # Data not found
        print('Data tidak ditemukan!')
    return database

def blank_value(val, new_val):
    """Function to get blank value input

    Args:
        val (any): Previous value
        new_val (any): New Value

    Returns:
        str: New value
    """    
    # Check if value is blank
    if not str(new_val) or not str(new_val).strip():
       # Assign new value from previous value
       new_val = val
    return new_val

def update_consultation(database):
    """Function to change/update schedule data in the database
    Args:
        database (dict): Consultation database

    Returns:
        dict: Lastest update database
    """
    # Get patient and doctor databases  
    patient_db = get_patient_db()
    doctor_db = get_doctor_db()

    # Initialize a variable to store the key for update
    key_update = None

    # Show database
    show_consultation(database)

    # Input the index number they want to update
    num = pyip.inputInt(prompt='Masukan Nomer atau indeks yang ingin diubah: ')

    # Clear screem
    clear_screen()
    
    # Search for the entry with the given index number
    for key, val in database.items():
        if key == 'column':
            continue
        elif val[0] == num:
            # Display the current data of the selected entry
            selected_entry = tabl.tabulate([database[key]], database['column'], tablefmt='psql')
            print(selected_entry, '\n')
            # Assign the key to key_update for update data later
            key_update = key
            # Unpack the current data of the selected entry for get preious value
            idx, consult_id, nik, patient_name, age, nip, doctor_name, specialization, consult_day, consult_time, consult_status, price, queue = database[key]
            # Get first 2 character for spesialist previous spesialist code
            code_spes = consult_id[:2] 
            # Split and get first word in consult day for date
            date = datetime.strptime(consult_day.split()[1], '%d-%m-%Y') 
    # If the key to update exists
    if key_update:
        # Get number/index
        idx = database[key_update][0]
        # Confirm to update
        continue_update = pyip.inputYesNo(prompt='Apakah anda ingin mengubah data ini (yes/no)?: ')
        # Clear screen
        clear_screen()
    
        if continue_update == 'yes':
            print('Lewati atau kosongkan input jika tidak ingin merubah data!\n')
            # Display the current data
            print('Data Sebelumnya')
            print(selected_entry, '\n')
            # Update the patient's NIK
            while True:
                # Input new NIK
                new_nik = pyip.inputInt(prompt='Masukan Nomor Induk Kependudukan(NIK) Pasien yang Baru: ', blank=True)
                # Call function to  get new value
                new_nik = blank_value(nik, new_nik)
                # Check if new value exist in patient database
                if new_nik in patient_db:
                    # Get patient's name from NIK in patient database
                    patient_name = list(patient_db[new_nik])[2]
                    # Calculate patient's age from birth date
                    birth = datetime.strptime((list(patient_db[new_nik])[3]), '%Y-%m-%d')
                    today = datetime.today()
                    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.month))
                    print(f'{patient_name} - {age} Tahun\n')
                    break
                else:
                    # New value not exist in patient database
                    print('NIK belum terdaftar!')
            while True:
                # Input and validate doctor's NIP
                new_nip = pyip.inputInt(prompt='Masukan Nomor Induk Pegawai(NIP) Dokter yang Baru: ', blank=True)
                new_nip = blank_value(nip, new_nip)
                if new_nip in doctor_db:
                    # Get doctor's name from NIP in doctor database
                    doctor_name = list(doctor_db[new_nip])[2]
                    # Get doctor's specialist from NIP in doctor database
                    specialization = list(doctor_db[new_nip])[3]
                    # Generate specialist code
                    code_spes = ''.join(char[0] for char in specialization.split())
                    print(f'{doctor_name} - {specialization}')
                    print(f'Jadwal Praktik : {list(doctor_db[new_nip])[4]}\n')
                    break
                else:
                    print('NIP belum terdaftar!')
            while True:
                # Input and validate consultation date
                new_date = pyip.inputDate(prompt='Masukan Tanggal Konsultasi (contoh :01-01-2023) yang Baru: ', formats = ('%d-%m-%Y',), blank=True)
                # Function to check blank value
                new_date = blank_value(date, new_date)
                # Function to get dayname in bahasa
                dayname = get_idn_dayname(new_date)
                # Check if date is within the allowed range
                if new_date < (new_date.today() - timedelta(days=30)) or new_date > (new_date.today() + timedelta(days=30)):
                    print('Tanggal konsultasi tidak bisa lebih dari 30 hari sebelum/setelah hari ini!')
                # Check if date matches doctor's schedule
                elif dayname not in list(doctor_db[new_nip])[4].split(', '):
                    print('Tanggal konsultasi tidak sesuai dengan jadwal dokter!')
                else:
                    # Consult date format
                    new_date_format = new_date.strftime('%d-%m-%Y')
                    consult_day = f'{dayname}, {new_date_format}'
                    print(f'{consult_day}\n')
                    break
            # Get the doctor's consultation time from the doctor database
            consult_time = list(doctor_db[new_nip])[5]
            # Input consultation status and determine the queue number
            # while True:
            new_consult_status=''
            if new_date < new_date.today():
                choice = ['Dibatalkan', 'Selesai']
                new_consult_status = pyip.inputMenu(prompt='Masukan Status Konsultasi yang Baru: \n', choices=choice, numbered=True, blank=True)
                new_consult_status = blank_value(consult_status, new_consult_status)
                # If consultation date is passed queue is none
                queue = None
            elif new_date > new_date.today():
                choice = ['Menunggu Konfirmasi', 'Terjadwalkan', 'Dibatalkan']
                new_consult_status = pyip.inputMenu(prompt='Masukan Status Konsultasi yang Baru: \n', choices=choice, numbered=True, blank=True)
                new_consult_status = blank_value(consult_status, new_consult_status)
                # Generate queue from function
                queue = get_queue(database, new_nip, consult_day)
            else:
                choice = ['Terjadwalkan', 'Dibatalkan', 'Selesai']
                new_consult_status = pyip.inputMenu(prompt='Masukan Status Konsultasi yang Baru: \n', choices=choice, numbered=True, blank=True)
                new_consult_status = blank_value(consult_status, new_consult_status)
                # Generate queue from function
                queue = get_queue(database, new_nip, consult_day)
            # Get consultation price from the doctor database
            price = list(doctor_db[new_nip])[6]
            # Generate a unique consultation ID based on details as primary key
            consult_id = f'{code_spes}{doctor_name[4:6].upper()}{patient_name[:2].upper()}{str(new_nip)[-2:]}{str(new_nik)[-2:]}'
            # Confirm to save new change
            confirm = pyip.inputYesNo(prompt='Apakah anda ingin menyimpan data ini (yes/no)?: ')
            clear_screen()
            if confirm == 'yes':
                database[key_update] = [idx, consult_id, new_nik, patient_name, age, new_nip, doctor_name, specialization, consult_day, consult_time, new_consult_status, price, queue]
                print('Data berhasil diubah')
    else:
        print('Nomer/indeks tidak ada')
    return database

def delete_consultation(database):
    """Function to remove consultaion schedule data entry from the database

    Args:
        database (dict): Consultation database

    Returns:
        dict: Latest database
    """    
    # Show database
    show_consultation(database)
    # Input number/index for delete operation
    num = pyip.inputInt(prompt='Masukan No. yang ingin dihapus: ')
    # Clear screen
    clear_screen()
    # Init key for delete
    key_del = None
    # Search for the entry with the given index number
    for key, val in database.items():
        if key == 'column':
            continue
        elif val[0] == num:
            # Display NIK's entry as primary key
            print(tabl.tabulate([database[key]], database['column'], tablefmt='psql'), '\n')
            # Assign the key to key_delete for deleting data
            key_del = key
            break
    if key_del:
        # Confirm to delete
        confirm = pyip.inputYesNo(prompt='Apakah anda ingin menghapus data ini (yes/no)?: ')
        # Clear screen after response
        clear_screen()
        if confirm == 'yes':
            # Delete entry from database
            del database[key_del]
            print('Data berhasil dihapus!')
            # Update or new assign numbering/indexing column after remove
            for i, val in enumerate (database.values()):
                if val[0] == 'No': # Continue when condition i in column name/header not data
                    continue
                val[0] = i # Assign i to every val[0]
    else:
        # Data not found
        print('Nomer/indeks tidak ada')
    return database

def consultation_list(database):
    """Function to display a menu that displays list consultation schedule data

    Args:
        database (dict): Consultation database
    """    
    while True:
        # Choice in show patient data menu
        choice = ['Lihat Seluruh Jadwal Konsultasi', 'Filter Jadwal Konsultasi Dengan Nama Pasien', 'Filter Jadwal Konsultasi Dengan Nama Dokter', 'Filter Jadwal Konsultasi Dengan Nama Spesialis', 'Filter Jadwal Konsultasi Dengan Hari/Tanggal Konsultasi', 'Filter Jadwal Konsultasi Dengan Status Konsultasi', 'Urutkan Jadwal Konsultasi Berdasarkan Tanggal', 'Kembali ke Menu Kelola Jadwal Konsultasi']
        # Main display
        prompt = f'''
------------------------------
-- Daftar Jadwal Konsultasi --
------------------------------
Pilih [1-{len(choice)}]]
'''
        # Input for show patient data menu you want display
        response = pyip.inputMenu(prompt=prompt, choices=choice, numbered=True)
        # Clear screen
        clear_screen()
        # Show entire consultation schedule data
        if response == 'Lihat Seluruh Jadwal Konsultasi':
            show_consultation(database)
        # Search/show schedule by patient name
        elif response == 'Filter Jadwal Konsultasi Dengan Nama Pasien':
            search_consultation(database, 'Nama Pasien')
        # Search/show schedule by doctor name
        elif response == 'Filter Jadwal Konsultasi Dengan Nama Dokter':
            search_consultation(database, 'Nama Dokter')
        # Search/show schedule by doctor specialist
        elif response == 'Filter Jadwal Konsultasi Dengan Nama Spesialis':
            search_consultation(database, 'Spesialis')
        # Search/show schedule by consultation date
        elif response == 'Filter Jadwal Konsultasi Dengan Hari/Tanggal Konsultasi':
            search_consultation(database, 'Hari/Tanggal Konsultasi')
        # Search/show schedule by consultation status
        elif response == 'Filter Jadwal Konsultasi Dengan Status Konsultasi':
            search_consultation(database, 'Status Konsultasi')
        # Show schedule by date order
        elif response == 'Urutkan Jadwal Konsultasi Berdasarkan Tanggal':
            sort_date(database)
        # Back to previous menu
        else :
            back = pyip.inputYesNo(prompt='Apakah anda ingin kembali ke menu kelola pasien (yes/no)?')
            clear_screen()
            if back == 'yes':
                break
    return database