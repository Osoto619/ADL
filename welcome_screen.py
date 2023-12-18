import sqlite3
import PySimpleGUI as sg
import management


# Connect to SQLite database
# The database file will be 'resident_data.db'
conn = sqlite3.connect('resident_data.db')
c = conn.cursor()

# Create  Resident table
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

# Create table for user settings
c.execute('''CREATE TABLE IF NOT EXISTS user_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_name TEXT UNIQUE,
    setting_value TEXT)''')

conn.commit()


# Function to get the user's saved theme
def get_user_theme():
    c.execute("SELECT setting_value FROM user_settings WHERE setting_name = 'theme'")
    result = c.fetchone()
    return result[0] if result else 'DarkBlue'  # Replace 'Default1' with your default theme


# Function to save theme choice
def save_user_theme_choice(theme):
    with sqlite3.connect('resident_data.db') as conn:
        cursor = conn.cursor()
        # Check if the theme setting already exists
        cursor.execute('SELECT COUNT(*) FROM user_settings WHERE setting_name = "theme"')
        exists = cursor.fetchone()[0] > 0

        if exists:
            # Update the existing theme setting
            cursor.execute('UPDATE user_settings SET setting_value = ? WHERE setting_name = "theme"', (theme,))
        else:
            # Insert a new theme setting
            cursor.execute('INSERT INTO user_settings (setting_name, setting_value) VALUES ("theme", ?)', (theme,))

        conn.commit()



# Function to load and apply the user's theme
def apply_user_theme():
    user_theme = get_user_theme()
    sg.theme(user_theme)

# Apply user theme at application startup
apply_user_theme()

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


def fetch_residents():
    """ Fetches a list of resident names from the database. """
    with sqlite3.connect('resident_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM residents')
        return [row[0] for row in cursor.fetchall()]

def remove_resident(resident_name):
    """ Removes a resident from the database. """
    with sqlite3.connect('resident_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM residents WHERE name = ?', (resident_name,))
        conn.commit()


def enter_resident_removal():
    # Fetch the list of residents for the dropdown
    residents = fetch_residents()

    # Define the layout for the removal window
    layout = [
        [sg.Text('Warning: Removing a resident is irreversible.', text_color='red')],
        [sg.Text('Please ensure you have saved any required data before proceeding.')],
        [sg.Text('Select a resident to remove:'), sg.Combo(residents, key='-RESIDENT-')],
        [sg.Button('Remove Resident'), sg.Button('Cancel')]
    ]

    # Create the removal window
    window = sg.Window('Remove Resident', layout)

    # Event loop for the removal window
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == 'Remove Resident':
            # Confirm the removal
            resident_to_remove = values['-RESIDENT-']
            if resident_to_remove:  # Proceed only if a resident is selected
                confirm = sg.popup_yes_no('Are you sure you want to remove this resident? This action cannot be undone.')
                if confirm == 'Yes':
                    remove_resident(resident_to_remove)
                    sg.popup(f'Resident {resident_to_remove} has been removed.')
                    window.close()
                    break

    window.close()


def change_theme_window():
    # Define the theme options available
    theme_options = sg.theme_list()

    # Layout for the theme selection window
    layout = [
        [sg.Text('Select Theme')],
        [sg.Combo(theme_options, default_value=sg.theme(), key='-THEME-', readonly=True)],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]

    # Create the theme selection window
    theme_window = sg.Window('Change Theme', layout)

    # Event loop for the theme window
    while True:
        event, values = theme_window.read()
        if event in (None, 'Cancel'):
            break
        elif event == 'Ok':
            selected_theme = values['-THEME-']
            sg.theme(values['-THEME-'])
            save_user_theme_choice(selected_theme)
            break

    theme_window.close()


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
         sg.Button('Add Resident', button_color='green'), sg.Button('Remove Resident', button_color='red')], 
         [sg.Text(text='', expand_x=True), sg.Button("Change Theme"), sg.Text(text='', expand_x=True)]
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
        elif event == 'Remove Resident':
            enter_resident_removal()
        elif event == 'Enter ADL Management':
            print(get_resident_count())
            if get_resident_count() == 0:
                sg.popup("Your Facility Has No Residents. Please Select Click Add Resident.")
                continue
            else:
                window.close()
                management.create_adl_management_window()
            return
        elif event == 'Change Theme':
            window.hide()
            change_theme_window()
            window.un_hide()

    window.close()
    return event


if __name__ == "__main__":
    # Main execution
    while True:
        # Check for existing resident data and display the welcome window
        if not display_welcome_window(get_resident_count()):
            break  # If a new resident was added, refresh the welcome window
    


# Close DB connection
conn.close()

