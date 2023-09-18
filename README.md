# Hospital Management and Schedulling System
Capstone Project 1 - Purwadhika Digital Technology School

The Hospital Management and Scheduling System is a digital platform designed to maximize efficiency and organization in managing patient data, doctor details, and consultation schedules within a hospital setting. With this system in place, it is hoped that communication and coordination between patients, doctors, and hospital administrators become more streamlined. Patients can easily access the information they need regarding consultation schedules, while admins have a tool that simplifies data and schedule management effectively and efficiently. Furthermore, this system enhances information transparency, reduces the risk of human error in scheduling, and overall improves the quality of service the hospital offers to its patients.

# Features
- **Create**: Allows administrators to input new data entries, be it patient records, doctor profiles, or consultation schedules, ensuring the database remains up-to-date with the latest information.
- **Read**: Facilitates access to the stored information. Users can view patient details, doctor profiles, and consultation schedules, ensuring transparency and aiding in informed decision-making.
- **Update**: Provides the capability to make modifications to existing records. If there's a change in a patient's health details, a doctor's schedule, or any other pertinent data, it can be quickly amended to reflect the most current information.
**- Delete**: Enables administrators to remove any outdated or irrelevant data. This ensures that the database remains streamlined, holding only the most pertinent and up-to-date information.

# Usage
This system caters to two distinct user types:
- **Admin**: Possesses full access to data management. The admin has the capability to:
  - Add, modify, delete, and view patient records.
  - Add, modify, delete, and view doctor details.
  - Arrange consultation schedules between patients and doctors, making modifications as necessary.
- **Regular Users (Patients)**: Have more limited access, focusing on information relevant to their needs. Patients can:
  - View their personal information.
  - Check profiles and specializations of doctors.
  - View the scheduled consultations set between them and their doctors.
    
# Installation
User
To get this project, you can clone it by running the following code:
```bash
git@github.com:muharismrgn/Capstone-Project-Module-1.git
```
Then install some additional tools by running the following code:
```bash
make install
make build
```
Now you can run it through the following command:
```bash
make run
```
# Project Organization

The directory structure of IndoMarket project looks like this:
```bash
├── README.md          <- The top-level README for developers using this project.
│
├── data               <- Patient, doctor, consultation schedulling database
│
├── docs               <- The document will consist of a detailed presentation.
│
├── src                <- Source code for use in this project.
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
```
# Contribute
If you'd like to contribute to the apps, check out https://github.com/muharismrgn/Capstone-Project-Module-1, or feel free to contact me.
