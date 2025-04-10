import sqlite3
import csv
# Connect to the database
conn = sqlite3.connect("EchoSphear.db", check_same_thread=False)
cursor = conn.cursor()


# cursor.execute("CREATE TABLE sys_command(id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))")

# # Insert test data                                                 
# cursor.execute("INSERT INTO sys_command VALUES (NULL, 'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE')")
# conn.commit()


# cursor.execute("CREATE TABLE web_command(id INTEGER PRIMARY KEY, name VARCHAR(100), url VARCHAR(1000))")

# cursor.execute("INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')")
# conn.commit()



# --------------------------------------------------------------------------------------------------------------------
# Drop the table if it exists and create a new one
# cursor.execute("DROP TABLE IF EXISTS sys_command")


# Check table structure
# cursor.execute("PRAGMA table_info(sys_command)")
# print(cursor.fetchall())  # Should show (id, name, path)

# Check if data exists
# cursor.execute("SELECT * FROM sys_command")
# print(cursor.fetchall())  # Should return inserted data


# Drop the table if it exists and create a new one
# cursor.execute("DROP TABLE IF EXISTS contacts")

# Check table structure
# cursor.execute("PRAGMA table_info(web_command)")
# print(cursor.fetchall())  # Should show (id, name, url)

# Check if data exists
# cursor.execute("SELECT * FROM web_command")
# print(cursor.fetchall())  # Should return inserted data

# --------------------------------------------------------------------------------------------------------------------


#test module
# app_name = "one note"
# cursor.execute('SELECT path FROM sys_command WHERE name = ?', (app_name,))
# results = cursor.fetchall()
# print(results)


#===============================================================================================================================================================

# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# desired_columns_indices = [0,18]

# with open('contacts.csv','r',encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute('''INSERT INTO contacts (id, name, mobile_no) VALUES (null, ?, ?);''', tuple(selected_data))

# conn.commit()
# conn.close()

#===============================================================================================================================================================

# Insert into database

# query = "INSERT INTO contacts VALUES (null, 'darshit', '9033917327', null)"
# cursor.execute(query)
# conn.commit()

#Search Contact Query 

# query = 'darshit'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', '%' + query + '%'))

# results = cursor.fetchall()
# print(results[0][0])