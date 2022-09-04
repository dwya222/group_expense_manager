#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os
import sys

expense_db_path = "./expense_db.csv"
expense_db_columns = ["Month", "Description", "Who", "Cost"]
logging = True
commit_log_path = "./commit_log.txt"

class ExpenseInterface:

    def __init__(self, user):
        self.user = user
        if not self.loadExpenseDb():
            self.initExpenseDb()
        self.initCommitLog()

    def loadExpenseDb(self):
        if os.path.exists(expense_db_path):
            if (pd.read_csv(expense_db_path).columns == expense_db_columns).all():
                self.expense_db = pd.read_csv(expense_db_path)
                return True
        return False

    def initExpenseDb(self):
        self.expense_db = pd.DataFrame(columns=expense_db_columns)

    def initCommitLog(self):
        if os.path.exists(commit_log_path):
            os.remove(commit_log_path)

    def start(self):
        while True:
            choice = input(str("What would you like to do?\n"
                               "Enter 'a' to add entry\n"
                               "Enter 'r' to remove entry\n"
                               "Enter 'v' to view database\n"
                               "Enter 'q' to save and quit\n"
                               "Enter 'q!' to quit without saving\n"
                               "Choice: "))
            if choice == 'a':
                self.requestAddExpense()
            elif choice == 'r':
                self.requestRemoveExpense()
            elif choice == 'v':
                self.viewExpenseDb()
            elif choice == 'q':
                self.saveExpenseDb()
                print("\nExiting expense interface")
                break
            elif choice == 'q!':
                print("\nExiting expense interface")
                break
            else:
                print("\nInvalid choice, please try again")

    def requestAddExpense(self):
        try:
            month = str(input("\nPlease enter the month for the expense (ex: August)\n"
                              "Month: "))
            description = str(input("Please enter a description of the expense (ex: Wifi)\n"
                                    "Description: "))
            cost = float(input("Please enter the cost of the expense (ex: 36.52)\n"
                                "Cost: "))
        except ValueError as e:
            print(f"Error: {e}, please try again")
            return

        self.checkAddExpense(month, description, cost)

    def checkAddExpense(self, month, description, cost):
        expense_df = pd.DataFrame([[month, description, self.user, cost]],
                                  columns=expense_db_columns)
        choice = str(input("Are you sure you would like to add the following expense to the "
                           f"database?\n{expense_df}\ny/n: "))
        if choice == 'y' or choice == 'Y':
            self.addExpense(expense_df)
        elif choice == 'n' or choice == 'N':
            print("Not adding to database\n")
        else:
            print("Invalid choice, not adding to database\n")

    def addExpense(self, expense_df):
        self.expense_db = pd.concat([self.expense_db, expense_df])
        self.resetExpenseDbIndex()
        if logging:
            self.logAddition(expense_df)
        print("Expense added successfully\n")

    def requestRemoveExpense(self):
        index = int(input("\nPlease enter the index of the entry you would like to remove\n"
                          f"{self.expense_db}\n"
                          "index: "))
        self.checkRemoveExpense(index)

    def checkRemoveExpense(self, index):
        expense_df = self.expense_db.loc[[index]]
        choice = str(input("Are you sure you would like to remove the following expense from the "
                           f"database?\n{expense_df}\ny/n: "))
        if choice == 'y' or choice == 'Y':
            self.removeExpense(expense_df, index)
        elif choice == 'n' or choice == 'N':
            print("Not removing expense\n")
        else:
            print("Invalid choice, not removing expense\n")

    def removeExpense(self, expense_df, index):
        self.expense_db = self.expense_db.drop(index)
        self.resetExpenseDbIndex()
        if logging:
            self.logRemoval(expense_df, index)
        print("Expense removed successfully\n")

    def viewExpenseDb(self):
        print(f"\nExpense Database: \n{self.expense_db}\n")
        input("press enter to continue")

    def resetExpenseDbIndex(self):
        self.expense_db = self.expense_db.reset_index(drop=True)

    def saveExpenseDb(self):
        self.expense_db.to_csv(expense_db_path, index=False)
        print("Saved expense database successfully\n")

    def logAddition(self, expense_df):
        msg = f"Added {expense_df['Month'][0]} {expense_df['Description'][0]} expense\n"
        self.logCommit(msg)

    def logRemoval(self, expense_df, index):
        msg = f"Removed {expense_df['Month'][index]} {expense_df['Description'][index]} expense\n"
        self.logCommit(msg)

    def logCommit(self, msg):
        with open(commit_log_path, 'a') as f:
            f.write(msg)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user = str(sys.argv[1])
        if user == "David" or user == "Andrew":
            print(f"Hello {user}, welcome to the Heron Lane Expense Interface")
        else:
            raise Exeption(f"You're not in the database, {user}. Please enter as Andrew or David")
    else:
        raise Exception("User undefined, please initialize this interface with your name")

    ei = ExpenseInterface(user)
    ei.start()
