import csv
import datetime as dt
# Step 1: Read the attendance log
log = {}
with open('attendence_log.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name'].strip()
        log[name] = {'timestamp': row['Time'].strip()}

# Step 2: Read students.csv and update "Present" column
updated_rows = []
with open('students.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames + ['Present'] if 'Present' not in reader.fieldnames else reader.fieldnames
    
    for row in reader:
        name = row['Name'].strip()
        row['Present'] = 'True' if name in log else 'False'
        updated_rows.append(row)
date = dt.date.today()
file_name = f'attendence_{date}.csv'
# Step 3: Write the updated data to a new CSV file
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"Attendance marking complete. Check {file_name}")
