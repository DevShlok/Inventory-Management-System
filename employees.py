from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import pymysql

def connect_database():
    try:
        connection=pymysql.connect(host='localhost',user='root',password='Niraj@9599')
        cursor=connection.cursor()
    except:
        messagebox.showerror('Error','Database Connectivity Issue try again')
        return None,None
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')
    cursor.execute('CREATE TABLE IF NOT EXISTS employee_data (empid INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100),gender VARCHAR(50),DOB varchar(30),'
                   'contact VARCHAR(30),employment_type VARCHAR(50),'
                   'work_shift VARCHAR(50),address VARCHAR(100),'
                   'doj VARCHAR(30),salary VARCHAR(50),'
                   'usertype VARCHAR(50),password VARCHAR(50))')
    
    return cursor,connection

connect_database()

def treeview():
    cursor,connection=connect_database()
    if not cursor or not connection:
        return 
    cursor.execute('SELECT * from employee_data')
    employee_records=cursor.fetchall()
    employee_treeview.delete(*employee_treeview.get_children())
    print(employee_records)
    for record in employee_records:
        employee_treeview.insert('',END,values=record)




def add_employee(empid,name,email,gender,dob,contact,employment_type,work_shift,address,doj,salary,user_type,password):
    if (empid == "" or name == "" or email == "" or gender == "Select Gender" or dob == "" or contact == "" or employment_type == "Select type"  or work_shift == "Select Shift" or address== '\n' or doj == "" or salary == "" or user_type == "Select User Type" or password == ""):
        messagebox.showerror("Error", "All fields are required!")
    else: 
        cursor,connection=connect_database()
        if not cursor or not connection:
            return 
        cursor.execute ('INSERT INTO employee_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(empid,name,email,gender,dob,contact,employment_type,work_shift,address,doj,salary,user_type,password))  
        connection.commit()
        treeview()
        messagebox.showinfo('Success','Data is inserted successfully')
def update_employee(empid, name, email, gender, dob, contact, employment_type, work_shift, address, doj, salary, user_type, password):
    if empid == "":
        messagebox.showerror("Error", "Employee ID is required for updating!")
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return 
        cursor.execute('SELECT * FROM employee_data WHERE empid=%s', (empid,))
        if cursor.fetchone() is None:
            messagebox.showerror("Error", "Employee ID not found!")
        else:
            cursor.execute('''UPDATE employee_data SET name=%s, email=%s, gender=%s, dob=%s, contact=%s, 
                              employment_type=%s, work_shift=%s, address=%s, doj=%s, salary=%s, usertype=%s, password=%s 
                              WHERE empid=%s''',
                           (name, email, gender, dob, contact, employment_type, work_shift, address, doj, salary, user_type, password, empid))
            connection.commit()
            treeview()
            messagebox.showinfo('Success', 'Employee details updated successfully')

def delete_employee(empid):
    if empid == "":
        messagebox.showerror("Error", "Employee ID is required for deletion!")
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return 
        cursor.execute('SELECT * FROM employee_data WHERE empid=%s', (empid,))
        if cursor.fetchone() is None:
            messagebox.showerror("Error", "Employee ID not found!")
        else:
            cursor.execute('DELETE FROM employee_data WHERE empid=%s', (empid,))
            connection.commit()
            treeview()
            messagebox.showinfo('Success', 'Employee deleted successfully')




    
def employee_form(window):
    global back_image, employee_treeview

    # Employee Frame
    employee_frame = Frame(window, width=1070, height=567, bg='white')
    employee_frame.place(x=200, y=100)

    heading_label = Label(employee_frame, text='Manage Employee Details', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    # **Top Frame for Treeview**
    top_frame = Frame(employee_frame, bg='white')
    top_frame.place(x=0, y=40, relwidth=1, height=235)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)

    employee_treeview = ttk.Treeview(top_frame, columns=('empid', 'name', 'email', 'gender', 'dob', 'contact', 
                                                         'employment_type', 'education', 'work_shift', 'address', 
                                                         'doj', 'salary', 'usertype'), show='headings',
                                     yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10, 0))

    # Define column headings
    columns = [
        ('empid', 'EmpId', 60),
        ('name', 'Name', 140),
        ('email', 'Email', 180),
        ('gender', 'Gender', 80),
        ('dob', 'Date of Birth', 100),
        ('contact', 'Contact', 100),
        ('employment_type', 'Employment Type', 140),
        ('education', 'Education', 120),
        ('work_shift', 'Work Shift', 100),
        ('address', 'Address', 200),
        ('doj', 'Date of Joining', 120),
        ('salary', 'Salary', 100),
        ('usertype', 'User Type', 120)
    ]

    for col, text, width in columns:
        employee_treeview.heading(col, text=text)
        employee_treeview.column(col, width=width)

    # **Call treeview() to display data initially**
    treeview()

    # **Detail Frame**
    detail_frame = Frame(employee_frame, bg='white')
    detail_frame.place(x=20, y=280)

    # **Form Fields**
    labels = [
        ('EmpId', 0, 0), ('Name', 0, 2), ('Email', 0, 4),
        ('Gender', 1, 0), ('Date of Birth', 1, 2), ('Contact', 1, 4),
        ('Employment Type', 2, 0), ('Education', 2, 2), ('Work Shift', 2, 4),
        ('Address', 3, 0), ('Date of Joining', 3, 2), ('Salary', 3, 4),
        ('User Type', 4, 2), ('Password', 4, 4)
    ]

    entries = {}

    for text, row, col in labels:
        Label(detail_frame, text=text, font=('times new roman', 12), bg='white').grid(row=row, column=col, padx=20, pady=10, sticky='w')

        if text in ['Gender', 'Employment Type', 'Education', 'Work Shift', 'User Type']:
            values = {
                'Gender': ('Male', 'Not Male'),
                'Employment Type': ('Full Time', 'Part Time', 'Casual', 'Contractual', 'Intern'),
                'Education': ('B.Tech', 'Others'),
                'Work Shift': ('Morning', 'Evening', 'Night'),
                'User Type': ('Admin', 'Employee')
            }
            entries[text] = ttk.Combobox(detail_frame, values=values[text], font=('times new roman', 12), width=18, state='readonly')
            entries[text].set(f'Select {text}')
        elif text in ['Date of Birth', 'Date of Joining']:
            entries[text] = DateEntry(detail_frame, width=18, font=('times new roman', 12), state='readonly', date_pattern='dd/mm/yyyy')
        elif text == 'Address':
            entries[text] = Text(detail_frame, width=20, height=3, font=('times new roman', 12), bg='lightyellow')
            entries[text].grid(row=row, column=col + 1, rowspan=2)
            continue
        else:
            entries[text] = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')

        entries[text].grid(row=row, column=col + 1, padx=20, pady=10)

    # **Button Frame**
    button_frame = Frame(employee_frame, bg='white')
    button_frame.place(x=300, y=520)

    # **Add Buttons**
    add_button = Button(button_frame, text='ADD', font=('times new roman', 12), cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: add_employee(
                            entries['EmpId'].get(), entries['Name'].get(), entries['Email'].get(),
                            entries['Gender'].get(), entries['Date of Birth'].get(), entries['Contact'].get(),
                            entries['Employment Type'].get(), entries['Work Shift'].get(), entries['Address'].get(1.0, END),
                            entries['Date of Joining'].get(), entries['Salary'].get(), entries['User Type'].get(), entries['Password'].get()
                        ))

    update_button = Button(button_frame, text='UPDATE', font=('times new roman', 12), cursor='hand2', fg='white',
                           bg='#0f4d7d', command=lambda: update_employee(
                               entries['EmpId'].get(), entries['Name'].get(), entries['Email'].get(),
                               entries['Gender'].get(), entries['Date of Birth'].get(), entries['Contact'].get(),
                               entries['Employment Type'].get(), entries['Work Shift'].get(), entries['Address'].get(1.0, END),
                               entries['Date of Joining'].get(), entries['Salary'].get(), entries['User Type'].get(), entries['Password'].get()
                           ))

    delete_button = Button(button_frame, text='DELETE', font=('times new roman', 12), cursor='hand2', fg='white',
                           bg='#d9534f', command=lambda: delete_employee(entries['EmpId'].get()))

 


    # **Button Layout**
    add_button.grid(row=0, column=0, padx=10, pady=10)
    update_button.grid(row=0, column=1, padx=10, pady=10)
    delete_button.grid(row=0, column=2, padx=10, pady=10)
    clear_button.grid(row=0, column=3, padx=10, pady=10)

    # **Call `treeview()` Again to Refresh Data**
    treeview()
