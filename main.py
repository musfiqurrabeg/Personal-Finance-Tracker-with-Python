import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from data_entry import get_amount, get_category, get_date, get_desc

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date" : date,
            "amount": amount,
            "category": category,
            "description": description
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filter_df = df.loc[mask]

        start_time = start_date.strftime(CSV.FORMAT)
        end_time = end_date.strftime(CSV.FORMAT)

        total_Income = filter_df[filter_df["category"] == "I"]["amount"].sum()
        total_Expense = filter_df[filter_df["category"] == "E"]["amount"].sum()
        net_savings = total_Income - total_Expense

        if filter_df.empty:
            print("No transaction found in the given data range")
        else:
            print(f"Transactions from {start_time} to {end_time}")
            print(
                filter_df.to_string(
                    index=False, 
                    formatters = {"date": lambda x:x.strftime(cls.FORMAT)}
                )
            )
            print("\nSummary:")
            print(f"Total Income: ${total_Income:.2f}")
            print(f"Total Expense: ${total_Expense:.2f}")
            print(f"Net Savings: ${net_savings:.2f}")
        return filter_df

def add():
    CSV.initialize_csv()
    date = get_date("\nEnter the date of the transaction (dd-mm-yyyy) or press enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_desc()
    CSV.add_entry(date, amount, category, description)

def plot_transaction(df):
    if df.empty:
        print("No data to plot.")
        return

    df.set_index('date', inplace=True)
    income_df = df[df["category"] == "I"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "E"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 6))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\nWelcome to Personal Finance Tracker.\n")
        print("1. Add a new transaction\n")
        print("2. View transaction and a summary within a date range.\n")
        print("3. Exit\n\n")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("\nEnter the start date(dd-mm-yyyy): ")
            end_date = get_date("\nEnter the end date(dd-mm-yyyy): ")

            df = CSV.get_transaction(start_date, end_date)
            plotchoice = input("Do you want to see a plot? (y/n): ").lower()
            if plotchoice == "y":
                plot_transaction(df)
                
        elif choice == "3":
            print("\nExiting................")
            break
        else:
            print("Invalid Choice. Enter 1 or 2 or 3 : ")

if __name__ == "__main__":
    main()



