import os
import sqlite3 as sq 
from matplotlib import pyplot as plt 
from expendo import Expendo

def main():
    expendo_menu = Expendo()

    menu_choice = Expendo.user_choice()
    while menu_choice != 'Q':
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
        