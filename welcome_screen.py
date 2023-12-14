import sqlite3
import PySimpleGUI as sg
import management


# Connect to SQLite database
# The database file will be 'resident_data.db'
conn = sqlite3.connect('resident_data.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS residents
             (name TEXT,
              age INTEGER,
              additional_info TEXT,
              self_care INTEGER)''')

# Create table for ADL charts
c.execute('''CREATE TABLE IF NOT EXISTS adl_chart (
             chart_id INTEGER PRIMARY KEY,
             resident_name TEXT,
             date TEXT,
             first_shift_sp TEXT,
             second_shift_sp TEXT,
             first_shift_activity1 TEXT,
             first_shift_activity2 TEXT,
             first_shift_activity3 TEXT,
             second_shift_activity4 TEXT,
             first_shift_bm TEXT,
             second_shift_bm TEXT,
             shower TEXT,
             shampoo TEXT,
             sponge_bath TEXT,
             peri_care_am TEXT,
             peri_care_pm TEXT,
             oral_care_am TEXT,
             oral_care_pm TEXT,
             nail_care TEXT,
             skin_care TEXT,
             shave TEXT,
             breakfast TEXT,
             lunch TEXT,
             dinner TEXT,
             snack_am TEXT,
             snack_pm TEXT,
             water_intake TEXT,
             FOREIGN KEY(resident_name) REFERENCES residents(name),
             UNIQUE(resident_name, date))''')

conn.commit()

sg.theme('Black')


def check_for_residents():
    """ Check if there are any residents in the database. """
    c.execute('SELECT * FROM residents')
    return c.fetchone() is not None


def insert_resident(name, age, additional_info, self_care):
    """ Insert a new resident into the database. """
    c.execute('INSERT INTO residents VALUES (?, ?, ?, ?)', (name, age, additional_info, self_care))
    conn.commit()


def enter_resident_info():
    """ Display GUI for entering resident information. """
    layout = [
        [sg.Text('Please Enter Resident Information')],
        [sg.Text('Name', size=(15, 1)), sg.InputText(key='Name')],
        [sg.Text('Age', size=(15, 1)), sg.InputText(key='Age')],
        [sg.Text('Additional Info', size=(15, 1)), sg.InputText(key='Additional_Info')],
        [sg.Checkbox('Personal Level of Care', key='Self_Care')],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Enter Resident Info', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        elif event == 'Submit':
            insert_resident(values['Name'], values['Age'], values['Additional_Info'], values['Self_Care'])
            sg.popup('Resident information saved!')
            window.close()
            return True

    window.close()
    return False


def get_resident_count():
    """ Return the number of residents in the database. """
    c.execute('SELECT COUNT(*) FROM residents')
    return c.fetchone()[0]


def display_welcome_window(num_of_residents_local):
    """ Display a welcome window with the number of residents. """
    image_path = 'ct-logo.png'
    layout = [
        [sg.Text(f'Welcome to CareTech ADL Manager', font=("Helvetica", 16),
                 justification='center')],
        [sg.Image(image_path)],
        [sg.Text(f'Your Facility Currently has {num_of_residents_local} Resident(s)',
                 font=("Helvetica", 14), justification='center')],
        [sg.Button('Enter ADL Management'),
         sg.Button('Add Resident')]
    ]

    window = sg.Window('CareTech ADL Manager', layout, element_justification='c')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Add Resident':
            window.close()
            enter_resident_info()
            break

        elif event == 'Enter ADL Management':
            window.close()
            management.create_adl_management_window()
            return

    window.close()
    return event


# Main execution
while True:
    # Check for existing resident data and display the welcome window
    if display_welcome_window(get_resident_count()):
        continue  # If a new resident was added, refresh the welcome window
    else:
        break  # Exit the loop if the window was closed without adding a new resident


# Close DB connection
conn.close()

