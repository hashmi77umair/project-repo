import mysql.connector as m
import datetime
from tabulate import tabulate
import pandas as pd
import csv
import maskpass

mydatabase = m.connect(host='localhost',user='root',password='777@Umair')
cursor = mydatabase.cursor()
cursor.execute('create database new_emp')

mydatabase = m.connect(host='localhost',user='root',password='777@Umair',database='new_emp')

cursor = mydatabase.cursor()

cursor.execute('create table emp_data (ID int not null auto_increment, Name varchar(20), Post varchar(20),Contact BIGINT(50) UNSIGNED NOT NULL , Salary int, Joining_Date Date, PRIMARY KEY (ID))')
cursor.execute('ALTER TABLE emp_data AUTO_INCREMENT = 10001')
password = 'asdfg'

def add_employee():
    while True:
        name = input('Enter Employee Name: ')
        if name.replace(' ', '').isalpha():
            break
        else:
            print('Invalid input! Please enter a valid name (letters and spaces only)')

    while True:
        post = input('Enter Employee Post: ')
        if post.replace(' ', '').isalpha():
            break
        else:
            print('Invalid input! Please enter a valid post (letters and spaces only)')

    while True:
        try:
            contact = int(input("Enter contact number (10 digits only): "))
            if len(str(contact)) != 10:
                raise ValueError('Contact number should be 10 digits long')
            if contact < 0:
                raise ValueError('Contact number should not be less than zero')
            break
        except ValueError:
            print('Invalid input! Please enter a valid contact number (10 digits only)')

    while True:
        try:
            salary = int(input('Enter Employee Salary: '))
            if salary <= 0:
                raise ValueError('Salary should be greater than 0')
            break
        except ValueError:
            print('Invalid input! Please enter a valid salary (numeric values only and greater than 0)')

    join_date = datetime.datetime.now().strftime('%Y-%m-%d')

    sql = 'insert into emp_data(Name, Post, Contact, Salary, Joining_Date) values(%s, %s, %s, %s, %s)'
    cursor.execute(sql, (name, post, contact, salary, join_date))
    mydatabase.commit()
    print('Employee Added Successfully')
    display_employees()
    menu()

def update_employee():
    confirm = maskpass.advpass("Please enter password to update data: ")  
    if confirm == password:
        emp_id = input("Enter Employee ID: ")
        sql = 'select * from emp_data where ID = %s'
        cursor.execute(sql, (emp_id,))
        result = cursor.fetchone()

        if result == None:
            print('No Employee Found')
            menu()
        else:
            print('Employee Found')
            print(f'ID: {result[0]}')
            print(f'Name: {result[1]}')
            print(f'Post: {result[2]}')
            print(f'Contact: {result[3]}')
            print(f'Salary: {result[4]}')
            print(f'Joining Date: {result[5]}')

            while True:
                name = input('Enter New Name (Leave blank to keep existing value): ')
                if name.replace(' ', '').isalpha() or name == '':
                    break
                else:
                    print('Invalid input! Please enter a valid name (letters and spaces only)')
                    
            while True:
                post = input('Enter New Post (Leave blank to keep existing value): ')
                if post.replace(' ', '').isalpha() or post == '':
                    break
                else:
                    print('Invalid input! Please enter a valid post (letters and spaces only)')
                    
            while True:
                contact = input("Enter New Contact number (10 digits) (Leave blank to keep existing value): ")
                if contact == '':
                    break
                elif not contact.isdigit():
                    print('Invalid input! Please enter a valid contact number (numeric values only)')
                elif len(contact) != 10:
                    print('Contact number should be 10 digits long')
                else:
                    break
                              
            while True:
                salary = input('Enter New Salary (Leave blank to keep existing value): ')
                if salary == '':
                    break
                elif not salary.isdigit():
                    print('Invalid input! Please enter a valid salary (numeric values only)')
                elif int(salary) <= 0:
                    print('Salary should be greater than 0')
                else:
                    salary = int(salary)
                    break

        if name == '':
            name = result[1]
        if post == '':
            post = result[2]
        if contact == '':
            contact = result[3]
        if salary == '':
            salary = result[4]

        sql = 'update emp_data set Name=%s, Post=%s, Contact=%s, Salary=%s where ID=%s'
        cursor.execute(sql, (name, post, contact, salary, emp_id))
        mydatabase.commit()
        print('Employee Updated Successfully')
        display_employees()
        menu()
    else:
        print("Incorrect password! Please try again.")
        menu()
        
def delete_employee():
    emp_id = int(input('Enter Employee ID: '))
    sql = 'select * from emp_data where ID = %s'
    cursor.execute(sql, (emp_id,))
    result = cursor.fetchone()

    if result is None:
        print('Employee not found')
        menu()
    else:
        print(f'Employee ID: {result[0]}')
        print(f'Employee Name: {result[1]}')
        print(f'Employee Post: {result[2]}')
        print(f'Contact: {result[3]}')
        print(f'Employee Salary: {result[4]}')
        print(f'Employee Joining Date: {result[5]}')
        print('--------------------------------------')
        
        while True:
            confirm2 = maskpass.advpass("Please enter password to delete: ")  
            if confirm2 == password:
                confirm = input('Are you sure you want to delete this employee? (y/n): ')
                if confirm.lower() == 'y':
                    sql = 'delete from emp_data where ID = %s'
                    cursor.execute(sql, (emp_id,))
                    mydatabase.commit()
                    print('Employee Deleted Successfully')
                    display_employees()
                else:
                    break
            else:
                print("incorrect password! Please try again.")
                break
            menu()
    menu()

def display_employees():
    sql = 'select * from emp_data'
    cursor.execute(sql)
    results = cursor.fetchall()
    
    passInfo = pd.DataFrame(results, columns=["ID", "Name", "Post", "Contact", "Salary", "Joining_Date"])

    if len(passInfo) != 0:

        print("\n\n")
        print(tabulate(passInfo, headers="keys", tablefmt="pretty"))
        print("\n\n")
    
    else:
        print("\nNo Transactions Yet\n")

    menu()
 
def export_employees():
    sql = 'select * from emp_data'
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results) == 0:
        print('No Employee Data Found')
        menu()
    else:
        with open('employee_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Post', 'Contact', 'Salary', 'Joining_Date'])
            for row in results:
                writer.writerow(row)
        print('Employee Data Exported Successfully')
        menu()

def intro():
    print("\t\t\t\t****************************************************")
    print("\t\t\t\t\t\tEMPLOYEE MANAGEMENT SYSTEM")
    print("\t\t\t\t****************************************************")

    input("Press Enter To Contiune: ")
intro()
def menu():
    print("Welcome to Employee Management Record")
    print("Press ")
    print("1- Add Employee")
    print("2- Update Employee")
    print("3- Delete Employees Data")
    print("4- Display Employee Data")
    print("5- Export Data to CSV")
    print("6- Exit")

    choice = int(input("Enter your Choice: "))
    if choice == 1:
        add_employee()
    elif choice == 2:
        update_employee()
    elif choice == 3:
        delete_employee()
    elif choice == 4:
        display_employees()
    elif choice == 5:
        export_employees()        
    elif choice == 6:
        exit(0)
    else:
        print("Invalid Choice")
        menu()

menu()
