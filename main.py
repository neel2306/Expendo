import os
import sqlite3 as sq 
from matplotlib import pyplot as plt 
from expendo import Expendo
import sys
import traceback

def main():
    expendo_menu = Expendo()
    menu_choice = expendo_menu.user_choice()
    while menu_choice != 8:
        if menu_choice == 1:
            expendo_menu.load_db()
        elif menu_choice==2:
            expendo_menu.exp_statement()
        elif menu_choice==3:
            expendo_menu.add_expense()
        elif menu_choice==4:
            expendo_menu.month_bank()
        elif menu_choice==5:
            expendo_menu.delete_entry()
        elif menu_choice==6:
            expendo_menu.update_entry()
        elif menu_choice==7:
            expendo_menu.visuals()
        menu_choice = expendo_menu.user_choice()
        
if __name__ == '__main__':
    main()