#!/usr/bin/env python3

import pandas as pd
import os

expense_db_path = "./expense_db.csv"
expense_summary_path = "./expense_summary.csv"
expense_summary_columns = ["Month", "Who", "Spent", "Owes"]
users = ["David", "Andrew"]

class ExpenseSummarizer:

    def __init__(self):
        self.loadExpenseDb()
        self.initSummaryDb()

    def loadExpenseDb(self):
        try:
            self.expense_db = pd.read_csv(expense_db_path)
        except FileNotFoundError as e:
            raise FileNotFoundError("Need to create expense database before attempting to "
                                    f"summarize, error msg: {e}")

    def initSummaryDb(self):
        self.expense_summary = pd.DataFrame(columns=expense_summary_columns)
        for index, row in self.expense_db.iterrows():
            if row["Month"] not in self.expense_summary['Month'].unique():
                self.addMonth(row["Month"])

    def addMonth(self, month):
        for user in users:
            month_df = pd.DataFrame([[month, user, 0.0, 0.0]],
                                    columns=expense_summary_columns)
            self.expense_summary = pd.concat([self.expense_summary, month_df])
        self.resetSummaryDbIndex()

    def resetSummaryDbIndex(self):
        self.expense_summary = self.expense_summary.reset_index(drop=True)

    def createSummaryDb(self):
        self.calculateSpent()
        self.calculateOwes()
        self.saveSummaryDb()

    def calculateSpent(self):
        for index, row in self.expense_db.iterrows():
            update_index = (self.expense_summary['Month'].eq(row['Month'])
                            & self.expense_summary['Who'].eq(row['Who']))
            self.expense_summary.loc[update_index, 'Spent'] += row['Cost']

    def calculateOwes(self):
        for month in self.expense_summary['Month'].unique():
            month_indices = self.expense_summary['Month'].eq(month)
            total = 0
            for cost in self.expense_summary.loc[month_indices, 'Spent'].to_list():
                total += cost
            individual_owes = total/len(users)
            update_index = (self.expense_summary['Month'].eq(month)
                            & self.expense_summary['Spent'].lt(individual_owes))
            self.expense_summary.loc[update_index, 'Owes'] = (individual_owes -
                    self.expense_summary.loc[update_index, 'Spent'])

    def saveSummaryDb(self):
        self.expense_summary.to_csv(expense_summary_path, index=False)

if __name__ == "__main__":
    es = ExpenseSummarizer()
    es.createSummaryDb()
    print(f"expense_summary: \n{es.expense_summary}")

