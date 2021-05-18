import datetime

# Input parameters (SEM for semester)
SEM_START_DATE = datetime.datetime(2021, 7, 26)
SEM_BREAK_DATE = datetime.datetime(2021, 9, 13)
SEM_RESUME_DATE = datetime.datetime(2021, 9, 27)
SEM_END_DATE = datetime.datetime(2021, 11, 27)
# 0 is Sunday ... 6 is Saturday (CAL for Calendar)
CAL_START_WEEKDAY = 1
###

# Design constants
TABLES_COUNT = 2
ROWS_PER_CELL = 4
###

# Computed constants
semester_length_days = (SEM_END_DATE - SEM_START_DATE).days

sem_start_weekday = int(SEM_START_DATE.strftime("%w"))
cal_start_date = SEM_START_DATE - datetime.timedelta(days=sem_start_weekday + CAL_START_WEEKDAY)

sem_end_weekday = int(SEM_END_DATE.strftime("%w"))
cal_end_date = SEM_END_DATE + (datetime.timedelta(days=- sem_end_weekday + 6 + CAL_START_WEEKDAY))

cal_weeks_count = int((cal_end_date - cal_start_date).days / 7)

table1_weeks_count = int(cal_weeks_count / 2) + (cal_weeks_count % 2 > 0) # < Round up

table2_weeks_count = cal_weeks_count - table1_weeks_count

###

# Drawing section
width = 297.0 * 4
height = 210.0 * 4
margin = 5.0 * 4
# + 1 row for weekday names (mon, tues, wed...)
row_count = table1_weeks_count * ROWS_PER_CELL + 1
row_height = (height - (margin * 2)) / row_count
table_width = (width - 4 * margin - 2 * row_height) / 2
cell_width = (table_width / 7)
cell_height = row_height * ROWS_PER_CELL
text_padding = 0.02 * cell_width
text_size = 0.7 * row_height

import svgwrite
dwg = svgwrite.Drawing(filename='studyplanoutput.svg', size=(width, height))

##########################
# Draw table 1 rows (grey lines)
x = margin + row_height
y = row_height + margin
i = 0
while i < row_count:
    line = dwg.add(dwg.line((x, y), (margin + table_width + row_height, y), stroke='lightgrey'))
    y = y + row_height
    i = i + 1

# Draw table1 cells (black boxes)
current_date = cal_start_date
week = 0
semester_week = 0
x = margin + row_height
y = margin + row_height
while week < table1_weeks_count:
    day = 0
    while day < 7:
        dwg.add(dwg.rect((x, y), (cell_width, cell_height), stroke='black', fill='none'))
        current_date = current_date + datetime.timedelta(days=1)
        text_string = ""
        box_size = row_height
        temp_text_padding = text_padding
        
        # Draw sem week numbers
        if day == 0:
            temp_week_number = (current_date - SEM_START_DATE).days / 7
            # If current week is during semester and not during break
            if current_date + datetime.timedelta(days=CAL_START_WEEKDAY) >= SEM_START_DATE and current_date + datetime.timedelta(days=CAL_START_WEEKDAY) < SEM_END_DATE and (current_date + datetime.timedelta(days=CAL_START_WEEKDAY) < SEM_BREAK_DATE or current_date + datetime.timedelta(days=CAL_START_WEEKDAY) >= SEM_RESUME_DATE) :
                semester_week = semester_week + 1
                dwg.add(dwg.text(semester_week, insert=(x - text_padding * 4, y + cell_height / 2), fill='black', font_family='Helvetica', font_size=text_size, style="baseline-shift:-33%;text-anchor:end"))
                
        if week == 0:
            week_string = current_date.strftime("%a")
            dwg.add(dwg.text(week_string, insert=(x + cell_width/2, y - row_height / 2), fill='black', font_family='Helvetica', font_size=text_size, style="baseline-shift-33%;text-anchor:middle"))
        
        
        
        if day == 0 and week == 0:
            dwg.add(dwg.rect((x, y), (cell_width / 1.5, row_height), stroke='black', fill='none'))
            text_string = str(current_date.day) + " " + current_date.strftime("%b")
        elif current_date.day == 1:
            dwg.add(dwg.rect((x, y), (cell_width / 1.5, row_height), stroke='black', fill='none'))
            text_string = str(current_date.day) + " " + current_date.strftime("%b")
        elif current_date.day - 9 <= 0:
            dwg.add(dwg.rect((x, y), (row_height, row_height), stroke='black', fill='none'))
            temp_text_padding = text_padding * 3
            text_string = current_date.day
        else:
            dwg.add(dwg.rect((x, y), (row_height, row_height), stroke='black', fill='none'))
            text_string = current_date.day
        dwg.add(dwg.text(text_string, insert=(x + temp_text_padding, y + row_height/2), fill='black', font_family='Helvetica', font_size=text_size, style="baseline-shift:-33%"))
        day = day + 1
        x = x + cell_width
    y = y + cell_height
    x = margin + row_height
    week = week + 1
    
#####################################
# Draw table 2 rows (grey lines)
row_count = table2_weeks_count * ROWS_PER_CELL

y = row_height + margin
x = 3 * margin + table_width + row_height
i = 0
while i < row_count:
    line = dwg.add(dwg.line((x, y), (x + table_width, y), stroke='lightgrey'))
    y = y + row_height
    i = i + 1

# Draw table2 cells (black boxes)
week = 0
y = margin + row_height
while week < table2_weeks_count:
    day = 0
    while day < 7:
        dwg.add(dwg.rect((x, y), (cell_width, cell_height), stroke='black', fill='none'))
        current_date = current_date + datetime.timedelta(days=1)
        text_string = ""
        box_size = row_height
        temp_text_padding = text_padding
        
        # Draw sem week numbers
        if day == 0:
            temp_week_number = (current_date - SEM_START_DATE).days / 7
            # If current week is during semester and not during break
            if current_date + datetime.timedelta(days=CAL_START_WEEKDAY) >= SEM_START_DATE and current_date + datetime.timedelta(days=CAL_START_WEEKDAY) < SEM_END_DATE and (current_date + datetime.timedelta(days=CAL_START_WEEKDAY) < SEM_BREAK_DATE or current_date + datetime.timedelta(days=CAL_START_WEEKDAY) >= SEM_RESUME_DATE) :
                semester_week = semester_week + 1
                dwg.add(dwg.text(semester_week, insert=(x - text_padding * 4, y + cell_height / 2), fill='black', font_family='Helvetica', font_size=text_size, style="baseline-shift:-33%;text-anchor:end"))
        
        if week == 0:
            week_string = current_date.strftime("%a")
            dwg.add(dwg.text(week_string, insert=(x + cell_width/2, y - row_height / 2), fill='black', font_family='Helvetica', font_size=text_size, style="baseline-shift-33%;text-anchor:middle"))
        
        
        if current_date.day == 1:
            dwg.add(dwg.rect((x, y), (cell_width / 1.5, row_height), stroke='black', fill='none'))
            text_string = str(current_date.day) + " " + current_date.strftime("%b")
        elif current_date.day - 9 <= 0:
            dwg.add(dwg.rect((x, y), (row_height, row_height), stroke='black', fill='none'))
            temp_text_padding = text_padding * 3
            text_string = current_date.day
        else:
            dwg.add(dwg.rect((x, y), (row_height, row_height), stroke='black', fill='none'))
            text_string = current_date.day
        dwg.add(dwg.text(text_string, insert=(x + temp_text_padding, y + row_height / 2), fill='black', font_family='Helvetica', font_size=text_size, style="baseline-shift:-33%"))
        day = day + 1
        x = x + cell_width
    y = y + cell_height
    x = 3 * margin + table_width + row_height
    week = week + 1
# todo rotate
dwg.save()
print("Saved to 'studyplanoutput.svg'")


    
