import datetime
import svgwrite

# Input parameters (SEM for Semester)
SEM_START_DATE = datetime.datetime(2021, 7, 26)
SEM_BREAK_DATE = datetime.datetime(2021, 9, 13)
SEM_RESUME_DATE = datetime.datetime(2021, 9, 27)
SEM_END_DATE = datetime.datetime(2021, 11, 27)
CAL_START_WEEKDAY = 1 # 0 is Monday, 1 is Sunday ... (CAL for Calendar)

# Design constants
ROWS_PER_CELL = 4

# Calendar constants
semester_length_days = (SEM_END_DATE - SEM_START_DATE).days
sem_start_weekday = int(SEM_START_DATE.strftime("%w")) # Weekday as a decimal number, 0 is Mon
cal_start_date = SEM_START_DATE - datetime.timedelta(days=sem_start_weekday + CAL_START_WEEKDAY)
sem_end_weekday = int(SEM_END_DATE.strftime("%w"))
cal_end_date = SEM_END_DATE + (datetime.timedelta(days=- sem_end_weekday + 6 + CAL_START_WEEKDAY))
cal_weeks_count = int((cal_end_date - cal_start_date).days / 7)
table1_weeks_count = int(cal_weeks_count / 2) + (cal_weeks_count % 2 > 0) # < Round up
table2_weeks_count = cal_weeks_count - table1_weeks_count

# Graphics constants
width = 297.0 * 4 # A4 is typically 29.7x21.0 cm
height = 210.0 * 4
margin = 5.0 * 4
row_count = table1_weeks_count * ROWS_PER_CELL + 1 # + 1 row for weekday names (mon, tues, wed...)
row_height = (height - (margin * 2)) / row_count
table_width = (width - 4 * margin - 2 * row_height) / 2
cell_width = (table_width / 7)
cell_height = row_height * ROWS_PER_CELL
text_padding = 0.02 * cell_width
text_size = 0.7 * row_height

def draw_table(x, y, width, height, weeks):
    global dwg
    global date
    global semester_week
    global first_table
    
    start_x = x

    # Draw rows (grey lines)
    i = 0
    rows = weeks * ROWS_PER_CELL + 1 # + 1 extra row for weekday names (mon, tues, wed...)
    while i < rows:
        line = dwg.add(dwg.line((x, y), (x + width, y), stroke='lightgrey'))
        y = y + row_height
        i = i + 1

    # Draw cells (black boxes)
    week = 0
    y = margin + row_height
    while week < weeks:
        day = 0
        while day < 7:
            dwg.add(dwg.rect((x, y), (cell_width, cell_height), stroke='black', fill='none'))
            date = date + datetime.timedelta(days=1)
            text_string = ""
            box_size = row_height
            temp_text_padding = text_padding

            # Draw sem week numbers
            # if current week is during sem and not during break
            if day == 0:
                semester_week = semester_week + 1
                dwg.add(dwg.text(semester_week, insert=(x - text_padding * 4, y + cell_height / 2), 
                    fill='black', font_family='Helvetica', 
                    font_size=text_size, style="baseline-shift:-33%;text-anchor:end"))

            # Draw week names
            if week == 0:
                week_string = date.strftime("%a") # abbreviated weekday name ie "Mon"
                dwg.add(dwg.text(week_string, insert=(x + cell_width/2, y - row_height / 2), 
                    fill='black', font_family='Helvetica', 
                    font_size=text_size, style="baseline-shift-33%;text-anchor:middle"))

            # calendar days
            if day == 0 and week == 0 and first_table: # If first cell on calendar
                dwg.add(dwg.rect((x, y), (cell_width / 1.5, row_height), stroke='black', fill='none'))
                text_string = str(date.day) + " " + date.strftime("%b") # Abbreviated month name
            elif date.day == 1: # If first day of month
                dwg.add(dwg.rect((x, y), (cell_width / 1.5, row_height), stroke='black', fill='none'))
                text_string = str(date.day) + " " + date.strftime("%b") 
            # Pad single digit days a bit more for aesthetics
            elif date.day - 9 <= 0: 
                dwg.add(dwg.rect((x, y), (row_height, row_height), stroke='black', fill='none'))
                temp_text_padding = text_padding * 3
                text_string = date.day
            else:
                dwg.add(dwg.rect((x, y), (row_height, row_height), stroke='black', fill='none'))
                text_string = date.day
            dwg.add(dwg.text(text_string, insert=(x + temp_text_padding, y + row_height/2), 
                fill='black', font_family='Helvetica', font_size=text_size, style="baseline-shift:-33%"))

            day = day + 1
            x = x + cell_width
        y = y + cell_height
        x = start_x
        week = week + 1
    first_table = False

dwg = svgwrite.Drawing(filename='studyplanoutput.svg', size=(width, height))
date = cal_start_date
semester_week = 0
first_table = True

draw_table(margin + row_height, row_height + margin, table_width, 0, table1_weeks_count)
draw_table(3 * margin + table_width + row_height, row_height + margin, table_width, 0, table2_weeks_count)
dwg.save()
print("Saved to 'studyplanoutput.svg'")