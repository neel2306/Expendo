import os
import sqlite3 as sq 
from matplotlib import pyplot as plt 
import sys
import traceback

class Expendo():
    def __init__(self):
        self.bank = None #Object that takes care of cash flow in
        self.conn = None
        self.cur = None
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
        h. Press 8 to quit the program.
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
                self.conn = sq.connect("{}.db".format(db_name)) #Establishing connection with database.
                self.cur = self.conn.cursor() #Cursor.
            
            #Loading the pre-existing database.
            elif db_choice == "L":
                db_name = input("Name of your database! : ").lower()
                self.conn = sq.connect("{}.db".format(db_name)) #Establishing connection with database.
                self.cur = self.conn.cursor() #Cursor.
            
            #Checking for and creating a table if it doesnt exist.
            self.cur.execute("CREATE TABLE IF NOT EXISTS expenses(ID INTEGER PRIMARY KEY AUTOINCREMENT,ID_Date DATETIME DEFAULT CURRENT_TIMESTAMP, Expenditure_TAG TEXT NOT NULL, Expense REAL NOT NULL)")
            self.conn.commit()
            print("Loaded/Created {} database!".format(db_name))
        except Exception as e:
            print("There was a program error: ", e)
    
    #Function to show the user his/her statement log.
    def exp_statement(self):
        try:
            print('''
            |----------------------STATEMENT MENU----------------------|
            a. Press 1 to view your latest expense.
            b. Press 2 to view your whole statement.
            c. Press 3 to view your n latest expenses.
            ''')
            view_choice = int(input("Please enter your choice: "))
            if view_choice == 1: #If the user only wants to see his/her last entry.
                print('''
                |------------------------STATEMENT-------------------------|
                ''')
                for row in self.cur.execute("SELECT * FROM expenses WHERE ID = (SELECT MAX(ID) FROM expenses)"):
                    print(row)
            elif view_choice == 2: #If the user wants to view hs whole statement log.
                print('''
                |------------------------STATEMENT-------------------------|
                ''')
                for row in self.cur.execute("SELECT * FROM expenses"):
                    print(row)

            elif view_choice == 3: #If the user wants to see his/her last n number of logs.
                no_of_entries = int(input("How many latest entries do you want to see: "))
                print('''
                |------------------------STATEMENT-------------------------|
                ''')
                for row in self.cur.execute("SELECT * FROM expenses ORDER BY ID DESC LIMIT ?", str(no_of_entries)):
                    print(row)
        except Exception as e:
            print("There was a program error: ", e)

    #Function to add an expense.
    def add_expense(self):
        try:
            flag = True
            while flag: #Looping through so that the user doesnt have to go through the menu each time.
                Expenditure_TAG = input("What kind of expenditure is this[Food, Grocery etc]: ").upper()
                Expenditure = float(input("Enter the amount: "))

                #Adding the data.
                self.cur.execute("INSERT INTO expenses (Expenditure_TAG, Expense) VALUES(?,?)", (Expenditure_TAG, Expenditure))
                self.conn.commit()

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
            if bank_choice == "N": #Entering a new monthly bank
                self.bank = input("Enter the amount available for this month: ")
                dir_path = os.path.dirname(os.path.realpath(__file__))
                filename = input("Enter name of your file: ")
                filepath = dir_path + r"\{}.txt".format(filename)
                 
                with open(filepath,"w") as f:
                    f.write(self.bank)
                    f.close()
                print("Entered new lump sum available for the month!")
            
            elif bank_choice == "L": #Loading the existing bank account.
                dir_path = os.path.dirname(os.path.realpath(__file__))
                filename = input("Enter name of your file: ")
                filepath = dir_path + r"\{}.txt".format(filename)
                if (os.path.getsize(filepath)) == 0:
                    self.bank = input("Your salary file is empty. Enter your bank amount: ") #The bank amount isnt entered.
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
    
    #Updating an entry.
    def update_entry(self):
        try:
            update_entry = int(input("Enter the Row ID of the data entry you want to update: "))
            updated_expense = float(input("Enter the new expense value: "))
            updated_tag = input("Enter the tag for the expense: ").upper()
            self.cur.execute("UPDATE expenses SET Expenditure_TAG = ?, Expense = ? where ID = ?", (updated_tag, updated_expense, update_entry))
            self.conn.commit()
            print("Updated the emtry!")
        except Exception as e:
            print("There was a program error: ", e)
    
    #Visualizations for the same.
    def visuals(self):
        try:
            #Sum of all the expenses
            print("")
            for row in self.cur.execute("SELECT TOTAL(Expense) FROM expenses"):
                agg_expense = row[0]
            #List of attributes to be plotted.
            y_list = [self.bank, agg_expense]
            labels = ["Money Bank", "Expenses"]
            plt.pie(y_list, labels=labels)
            plt.show()
        
        except BaseException as ex:
            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : %s" %stack_trace)




        

    
