import PySimpleGUI as sg
import sqlite3
import calendar

# sg.theme('black')

# Define the width of the label cell and regular cells
label_cell_width = 12  # This may need to be adjusted to align perfectly
regular_cell_width = 5  # This may need to be adjusted to align perfectly

# Define the number of days
num_days = 31


def create_horizontal_bar(text):
    return [sg.Text(f'{text}', justification='center', expand_x=True, relief=sg.RELIEF_SUNKEN)]


def create_row_label(text):
    return [sg.Text(f'{text}', size=(label_cell_width+1, 1), pad=(0,0), justification='center')]


def create_input_text(key):
    return [sg.InputText(size=(regular_cell_width, 1), pad=(3, 3), justification='center', key=f'-{key}-{i}-') for i in range(1, num_days + 1)]


def fetch_adl_chart_data_for_month(resident_name, year_month):
    # year_month should be in the format 'YYYY-MM'
    with sqlite3.connect('resident_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM adl_chart
            WHERE resident_name = ? AND strftime('%Y-%m', date) = ?
            ORDER BY date
        ''', (resident_name, year_month))
        return cursor.fetchall()


def show_adl_chart(resident_name, year_month):
    # Define the number of days
    num_days = 31

    # Define the width of the label cell and regular cells
    label_cell_width = 12  # This may need to be adjusted to align perfectly
    regular_cell_width = 5  # This may need to be adjusted to align perfectly

    # Define activities
    activities = [
        "1. Movie & Snack or TV",
        "2. Exercise/Walking",
        "3. Games/Puzzles",
        "4. Outside/Patio",
        "5. Arts & Crafts",
        "6. Music Therapy",
        "7. Gardening",
        "8. Listen to Music",
        "9. Social Hour",
        "10. Cooking/Baking",
        "11. Birdwatching",
        "12. Outing/Excursion",
        "13. Hospice Visit",
        "14. Other as Listed on the Service Plan",
        "15. Social Media"
    ]

    # Divide activities into three columns
    column1 = [[sg.Text(activities[i])] for i in range(0, len(activities), 3)]
    column2 = [[sg.Text(activities[i])] for i in range(1, len(activities), 3)]
    column3 = [[sg.Text(activities[i])] for i in range(2, len(activities), 3)]

    # Create a frame with three columns
    activities_frame = sg.Frame('Activities', layout=[
        [sg.Column(column1), sg.Column(column2), sg.Column(column3)]
    ], relief=sg.RELIEF_SUNKEN)

    # Empty row for the table to just show headers
    data = [[]]  # No data rows, only headers

    # Parse the year and month
    year, month_number = year_month.split('-')
    month_name = calendar.month_name[int(month_number)]

    # Define the layout of the window
    layout = [
        [sg.Text('CareTech Monthly ADL Chart', font=('Helvetica', 16), justification='center', expand_x=True)],
        [sg.Text('RESIDENT:', size=(10, 1)), sg.Text(f'{resident_name}', key='-RESIDENT-', size=(20, 1)),
        sg.Text('MONTH:', size=(10, 1)), sg.Text(f'{month_name} {year}', key='-MONTH-', size=(20, 1))],
        # Table as a header row of cells
        [sg.Table(values=data,
              headings=[''] + [str(i) for i in range(1, num_days + 1)],
              max_col_width=regular_cell_width,
              auto_size_columns=False,
              col_widths=[label_cell_width] + [regular_cell_width]*num_days,
              display_row_numbers=False,
              justification='center',
              num_rows=0,
              key='-TABLE-',
              row_height=25,
              pad=(0,0),
              hide_vertical_scroll=True)],
        create_horizontal_bar("Service Plan (initial when completed)"),
        create_row_label("1st Shift") +
        create_input_text("1ST_SHIFT_SP"),
        create_row_label("2nd Shift") +
        create_input_text("2ND_SHIFT_SP"),
        create_horizontal_bar("Activity Record Number (see legend at bottom)"),
        create_row_label("1st Shift") +
        create_input_text("1ST_SHIFT_ACTIVITY1"),
        create_row_label("1st Shift") +
        create_input_text("1ST_SHIFT_ACTIVITY2"),
        create_row_label("1st Shift") +
        create_input_text("1ST_SHIFT_ACTIVITY3"),
        create_row_label("2nd Shift") +
        create_input_text("2ND_SHIFT_ACTIVITY4"),
        create_horizontal_bar("Bowel Movement Record size of BM and how many if more than one (Example: S, M, L, XL, or D for diarrhea)"),
        create_row_label("1st Shift") +
        create_input_text("1ST_SHIFT_BM"),
        create_row_label("2nd Shift") +
        create_input_text("2ND_SHIFT_BM"),
        create_horizontal_bar("ADL's (initial when complete)"),
        create_row_label("SHOWER") +
        create_input_text("SHOWER"),
        create_row_label("SHAMPOO") +
        create_input_text("SHAMPOO"),
        create_row_label("SPONGE BATH") +
        create_input_text("SPONGE"),
        create_row_label("PERI CARE AM") +
        create_input_text("PERI_AM"),
        create_row_label("PERI CARE PM") +
        create_input_text("PERI_PM"),
        create_row_label("ORAL CARE AM") +
        create_input_text("ORAL_CARE_AM"),
        create_row_label("ORAL CARE PM") +
        create_input_text("ORAL_CARE_PM"),
        create_row_label("NAIL CARE") +
        create_input_text("NAIL_CARE"),
        create_row_label("SKIN CARE") +
        create_input_text("SKIN_CARE"),
        create_row_label("SHAVE") +
        create_input_text("SHAVE"),
        create_horizontal_bar("Meals (Record Percentage of Meal Eaten)"),
        create_row_label("BREAKFAST") +
        create_input_text("BREAKFAST"),
        create_row_label("LUNCH") +
        create_input_text("LUNCH"),
        create_row_label("DINNER") +
        create_input_text("DINNER"),
        create_row_label("SNACK AM") +
        create_input_text("SNACK_AM"),
        create_row_label("SNACK PM") +
        create_input_text("SNACK_PM"),
        create_row_label("WATER IN-TAKE") +
        create_input_text("WATER"),
        [sg.Text(text='', expand_x=True), activities_frame, sg.Text(text='', expand_x=True)]
    ]

    # Create the window
    window = sg.Window(' CareTech Monthly ADLs', layout, finalize=True, resizable=True)

    adl_data = fetch_adl_chart_data_for_month(resident_name, year_month)

    # If data is found, update the layout fields accordingly
    if adl_data:
        for entry in adl_data:
            chart_id, resident, date, *values = entry  # Unpack each tuple
            day_number = int(date.split('-')[2])  # Extract day number from date

            adl_keys = [
                "1ST_SHIFT_SP", "2ND_SHIFT_SP", "1ST_SHIFT_ACTIVITY1", "1ST_SHIFT_ACTIVITY2",
                "1ST_SHIFT_ACTIVITY3", "2ND_SHIFT_ACTIVITY4", "1ST_SHIFT_BM", "2ND_SHIFT_BM",
                "SHOWER", "SHAMPOO", "SPONGE", "PERI_AM", "PERI_PM", "ORAL_CARE_AM", "ORAL_CARE_PM",
                "NAIL_CARE", "SKIN_CARE", "SHAVE", "BREAKFAST", "LUNCH", "DINNER", "SNACK_AM",
                "SNACK_PM", "WATER"
                # ... list all the keys in the same order as they are in the database ...
            ]

            for adl_key, value in zip(adl_keys, values):
                if value:  # Check if there is a value to update
                    window[f'-{adl_key}-{day_number}-'].update(value)

    # Event Loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    show_adl_chart("Rosa Soto", "2023-12")
