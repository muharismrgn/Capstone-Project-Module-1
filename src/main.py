import os, csv, keyboard
import doctor, patient, consultation
import pyinputplus as pyip

def clear_screen():
    """
    Function to clear the screen
    """    
    os.system('cls' if os.name == 'nt' else 'clear')

def latest_version(path, database):
    """
    Function for database keep up to date
    """    
    # Keep data up to date
    with open(path, 'w') as file:
        dataWriter = csv.writer(file, delimiter=';', lineterminator='\n')
        dataWriter.writerows(database.values())

def get_db(path):
    """function to get database from path

    Args:
        path (str): path of database file

    Returns:
        (dict): return all dictionary database
                - patient database
                - doctor database
                - consultation database
    """
    # Initialize empty database    
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
            if path == patient_path:
                # Extract row into variables
                idx, nik, name, birth, gender, address, phone = row
                # Updating database
                database.update({int(nik): [int(idx), int(nik), name, birth, gender,  address, phone]})
            elif path == doctor_path:
                # Extract row into variables
                idx, nip, name, specialization, poli_id, practice_day, practice_hours = row
                # Updating database
                database.update({int(nip): [int(idx), int(nip), name, specialization, poli_id,  practice_day, practice_hours]})
            elif path == consultation_path:
                # Extract row into variables
                idx, consult_id, nik, patient_name, age, nip, doctor_name, specialization, consult_day, consult_time, consult_status, price, queue= row
                # Updating database
                database.update({consult_id: [int(idx), consult_id, int(nik), patient_name, int(age), int(nip), doctor_name, specialization, consult_day, consult_time, consult_status, int(price), queue]})
    return database

def manage_data(title, file, path):
    """Function to manage data for a given

    Args:
        title (str): title for user display
        file (str): call function name from another file
        path (str): path of database file
    """    
    prompt = f'''
---------{'-'*(len(title)+4)}
-- Kelola {title} --
---------{'-'*(len(title)+4)}
Pilih [1-5]
'''
    while True:
        # To get database
        database = get_db(path)
        # Show main menu of features
        choices = [f'Tambah {title} Baru', f'Lihat Daftar {title}', f'Update Info {title}', f'Hapus {title}', 'Kembali ke Menu Utama']
        response = pyip.inputMenu(prompt=prompt, choices=choices, numbered=True)
        clear_screen()
        # Add new data entry
        if response == f'Tambah {title} Baru':
            while True:
                # Keep data up to date
                latest_version(path, database)
                # Add data menu
                response = pyip.inputMenu(prompt=f'\n---- Tambah {title} Baru ----\nPilih [1-2]\n', choices=[f'Tambah {title} Baru', f'Kembali ke Menu Kelola {title}'], numbered=True)
                # Clear screen
                clear_screen()
                if response == f'Tambah {title} Baru':
                    # Call add function from module
                    eval(f'{file}.add_{file}')(database)
                else:
                    back = pyip.inputYesNo(prompt=f'Apakah anda ingin kembali ke menu kelola {title.lower()} (yes/no)?')
                    # Clear screen
                    clear_screen()
                    if back == 'yes':
                        break
        # Show entire data or certain data
        elif response == f'Lihat Daftar {title}':
            # Call view list function from module
            eval(f'{file}.{file}_list')(database)
        # Update data
        elif response == f'Update Info {title}':
            while True: 
                # Update data menu
                response = pyip.inputMenu(prompt=f'\n---- Update Info {title} ----\nPilih [1-2]\n', choices=[f'Update Info {title}', f'Kembali ke Menu Kelola {title}'], numbered=True)
                # Clear screen
                clear_screen()
                if response == f'Update Info {title}':
                    # Call update function from module
                    database = eval(f'{file}.update_{file}')(database)
                    # Keep up to date data
                    latest_version(path, database)
                else:
                    # Back to previous menu
                    back = pyip.inputYesNo(prompt=f'Apakah anda ingin kembali ke menu kelola {title.lower()} (yes/no)?')
                     # Clear screen
                    clear_screen()
                    if back == 'yes':
                        break
        # Delete data
        elif response == f'Hapus {title}':
            while True:
                # Keep up to date data
                latest_version(path, database)
                # Delete data menu
                response = pyip.inputMenu(prompt=f'\n---- Hapus {title} ----\nPilih [1-2]\n', choices=[f'Hapus {title}', f'Kembali ke Menu Kelola {title}'], numbered=True)
                # Clear screen
                clear_screen()
                if response == f'Hapus {title}':
                    # Call delete function from module
                    eval(f'{file}.delete_{file}')(database)
                else:
                    # Back to previous menu
                    back = pyip.inputYesNo(prompt=f'Apakah anda ingin kembali ke menu kelola {title.lower()}(yes/no)?')
                     # Clear screen
                    clear_screen()
                    if back == 'yes':
                        break
        # Back to main menu
        else:
            # Confirm back to main menu
            back = pyip.inputYesNo(prompt='Apakah anda ingin kembali ke main menu (yes/no)?')
             # Clear screen
            clear_screen()
            if back == 'yes':
                break

def login():
    """Login function to access all features or some parts

    Returns:
        str: User type
    """    
    print('\n-- LOGIN  --')
    while True:
        # Input username and password
        username = pyip.inputStr(prompt="Username: ")
        password = pyip.inputPassword(prompt="Password: ")
        # Clear screen
        clear_screen()
        # Checking username and password to database
        if username in users_db and users_db[username][0] == password:
            # Welcoming
            print(f"\nSelamat datang, {username.upper()}!")
            print("Tekan 'space' untuk melanjutkan...")
            while not keyboard.is_pressed('space'):  # Tunggu sampai pengguna menekan 'space'
                pass
            return users_db[username][1]
        else:
            # Username or password not exist in database
            print("Login gagal!")
            return None

def main():
    """Main Function
    """    
    # Clear screen
    clear_screen()
    # Define user type
    userType = None
    # Calling login function
    while not userType: 
        userType = login()

    # Based on userType, Show differemt menu and features
    if userType == "superuser":
        # CLear screen
        clear_screen()
        # Admin display menu
        admin_prompt = '''
===============================================
-- Sistem Manajemen dan Jadwal Konsultasi RS --
===============================================
Pilih [1-4]
'''
        while True:
            # Admin choice or feature
            main_choice = ['Kelola Pasien', 'Kelola Dokter', 'Kelola Jadwal Konsultasi', 'Keluar']
            # Input menu
            response = pyip.inputMenu(prompt=admin_prompt, choices=main_choice, numbered=True)
            # Clear screen
            clear_screen()
            # Manage Patient
            if response == 'Kelola Pasien':
                manage_data('Pasien', 'patient', patient_path)
             # Manage Doctor
            elif response == 'Kelola Dokter':
                manage_data('Dokter', 'doctor', doctor_path)
            # Manage consultation schedule
            elif response == 'Kelola Jadwal Konsultasi':
                manage_data('Jadwal Konsultasi', 'consultation', consultation_path)
            # Exit program
            else :
                # Confirm to exit program
                exit = pyip.inputYesNo(prompt='Apakah anda ingin keluar (yes/no)?')
                # Clear screen
                clear_screen()
                if exit == 'yes':
                    print('Thank you, Have a nice day...')
                    # Logout
                    userType = None
                    break

    elif userType == "user":
        # Clear screen
        clear_screen()
        # Get all database
        patient_db = get_db(patient_path)
        doctor_db = get_db(doctor_path)
        consultation_db = get_db(consultation_path)
        # User display menu
        user_prompt = '''
===============================================
-- Sistem Informasi dan Jadwal Konsultasi RS --
===============================================
Pilih [1-4]
'''
        while True:
            # User choice or feature
            user_choice = ['Lihat Daftar Pasien', 'Lihat Daftar Dokter', 'Lihat Daftar Jadwal Konsultasi', 'Keluar']
            # Input Menu
            response = pyip.inputMenu(prompt=user_prompt, choices=user_choice, numbered=True)
            # Clear screem
            clear_screen()
            # List of entire patients data or some parts
            if response == 'Lihat Daftar Pasien':
                patient.patient_list(patient_db)
            # List of entire doctors data or some parts
            elif response == 'Lihat Daftar Dokter':
                doctor.doctor_list(doctor_db)
            # List of entire consultation schedule or some parts
            elif response == 'Lihat Daftar Jadwal Konsultasi':
                consultation.consultation_list(consultation_db)
            # Exit program
            else :
                # Confirm to exit program
                exit = pyip.inputYesNo(prompt='Apakah anda ingin keluar (yes/no)?')
                # Clear screen
                clear_screen()
                if exit == 'yes':
                    print('Thank you, Have a nice day...')
                    userType = None
                    break

# All file path
patient_path = 'data\patient.csv'
doctor_path = 'data\doctor.csv'
consultation_path = 'data\consultation.csv'

# Database user
users_db = {
    'admin': ['admin', 'superuser'], 
    'user': ['user', 'user']
}

main()