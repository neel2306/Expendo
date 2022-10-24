import os
import sqlite3 as sq 
from matplotlib import pyplot as plt 

class Expendo():
    def __init__(self):
        self.bank = None #Object that takes care of casgh flow in
        print("""
        |--------------------------EXPENDO-------------------------|
        |                     Welcome to Expendo!                  |
        |            One stop for all your money Management        |
        """)
    
    #Funtion portraying the menu for Expendo and also taking in the user's input.
    def user_choice(self):
        print("""
        |---------------------------MENU---------------------------|
        a. Press 1 to create/load your database.
        b. Press 2 to view your expenditure statement.
        c. Press 3 to add an expenditure. 
        d. Press 4 to add money saved for the month.
        e. Press 5 to delete the latest entry. #Accountability for your spendings.
        f. Press 6 to update an entry.
        g. Press 7 for visualization of your financial situation. 
        h. Press Q to quit the program.
        """)
    
        try:
            choice = int(input("Enter your choice: "))
            return choice
        except:
            print("Please enter a valid key next time!")
    
    #Funtion to create/load the existing databases.
    def load_db(self):
        db_choice = input("Create a new database? (C) | Load an existing database(L) : ").upper() #Asking user to create or load a database.
        try:
            #Creating a new database.
            if db_choice == "C":
                db_name = input("Name your database! : ").lower()
                self.con = sq.connect("{}.db".format(db_name)) #Establishing connection with database.
                self.cur = con.cursor() #Cursor.
            
            #Loading the pre-existing database.
            elif db_choice == "L":
                db_name = input("Name of your database! : ").lower()
                self.con = sq.connect("{}.db".format(db_name)) #Establishing connection with database.
                self.cur = con.cursor() #Cursor.
            
            #Checking for and creating a table if it doesnt exist.
            self.cur.execute("CREATE TABLE IF NOT EXISTS expenses(ID INTEGER PRIMARY KEY AUTOINCREMENT,ID_Date DATETIME DEFAULT CURRENT_TIMESTAMP, Expenditure_TAG TEXT NOT NULL, Expense REAL NOT NULL")
            self.con.commit()
            print("Loaded/Created {} database!".format(db_name))
        except Exception as e:
            print("There was a program error: ", e)
    
    #Function to show 5 latest expenditures.
    def exp_statement(self):
        try:
            print("-"*24,"Showing last 5 expenditures!", "-"*24)
            self.cur.execute("SELECT * FROM expenses ORDER BY ID_Date DESC LIMIT 10")
            self.con.commit()
        except Exception as e:
            print("There was a program error: ", e)
    
    #Function to add an expense.
    def add_expense(self):
        try:
            flag = True
            while flag:
                Expenditure_TAG = input("What kind of expenditure is this[Food, Grocery etc]: ").upper()
                Expenditure = float(input("Enter the amount: "))

                #Adding the data.
                self.cur.execute("INSERT INTO expenses (Expenditure_TAG, Expense) VALUES(?,?)", (Expenditure_TAG, Expenditure))
                self.con.commit()

                #Addition of more data.
                continuation = input("Do you want to enter more expenses?[Y/N]: ").upper()
                if continuation == 'N':
                    flag = False
        
        except Exception as e:
            print("There was a program error: ", e)
    
    #Lump sum for the month.
    def month_bank(self):
        try:
            bank_choice = input("Enter a new monthly bank (N) | Load the existing monthly bank (L): ").upper()
            if bank_choice == "N":
                self.bank = float(input("Enter the amount available for this month: "))
                dir_path = os.path.dirname(os.path.realpath(__file__))
                filename = input("Enter name of your file: ")
                filepath = dir_path + r"\{}.txt".format
                 
                with open(filepath,"w") as f:
                    f.write(self.bank)
                    f.close()
                print("Entered new lump sum available for the month!")
            
            elif bank_choice == "L":
                dir_path = os.path.dirname(os.path.realpath(__file__))
                filename = input("Enter name of your file: ")
                filepath = dir_path + r"\{}.txt".format
                if (os.path.getsize(filepath)) == 0:
                    self.bank = input("Your salary file is empty. Enter your salary: ")
                    with open(filepath, 'w') as f:
                        f.write(self.bank)
                        f.close()
                else:
                    with open(filepath, 'r') as f:
                        self.bank = f.read()
                        f.close()
                print("Loaded your amount available for the month!")
        
        except Exception as e:
            print("There was a program error: ", e)
            
    #Deleting an entry.
    def delete_entry(self):
        try:
            self.cur.execute("DELETE FROM expenses WHERE id = (SELECT MAX(id) FROM expenses)")
            print('Deleted the latest entry!')
        except Exception as e:
            print("There was a program error: ", e)
    
    def update_entry():
        try:
            update_entry = int(input("Enter the Row ID of the data entry you want to update: "))
            updated_expense = float(input("Enter the new expense value: "))
            updated_tag = input("Enter the tag for the expense: ").upper()
            self.cur.execute("UPDATE expenses SET Expenditure_TAG = ?, Expense = ? where ID = ?", (updated_tag, updated_expense, update_entry))
            self.con.commit()
            print("Updated the emtry!")
        except Exception as e:
            print("There was a program error: ", e)
            




        






        
#exp1 = Expendo()
#exp1.exp_statement()

    
