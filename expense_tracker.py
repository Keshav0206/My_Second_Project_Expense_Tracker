import json
import datetime

months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


class Transaction:
    def __init__(self, id, category, amount, description, day, month, year):
        self.id = id
        self.category = category
        self.amount = amount
        self.description = description
        self.day = day
        self.month = month
        self.year = year

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "amount": self.amount,
            "description": self.description,
            "day": self.day,
            "month": self.month,
            "year": self.year,
        }


class FinanceTracker:
    file_path = "transactions.json"

    def __init__(self):
        self.transactions = []

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                self.transactions = json.load(file)

        except FileNotFoundError:
            self.transactions = []
            with open(self.file_path, "w") as file:
                json.dump(self.transactions, file, indent=4)

    def get_new_id(self):
        if self.transactions == []:
            return 1
        new_id = max(transaction["id"] for transaction in self.transactions)
        new_id += 1
        return new_id

    def add_transaction(self, t_new):
        self.transactions.append(t_new)

    def save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.transactions, file, indent=4)

    def del_transaction(self, del_id):
        for i, transaction in enumerate(self.transactions):
            if transaction["id"] == del_id:
                self.transactions.pop(i)
                print(f"Transaction with ID {del_id} was deleted")
                break
        else:
            print("Invalid ID")

    def print_header(self):
        print("-" * 75)
        print(f"{'ID':<5}{'Category':<15}{'Amount':<10}{'Description':<25}{'Date':<15}")
        print("-" * 75)

    def print_transaction(self, transaction):
        print(
            f"{transaction['id']:<5}"
            f"{transaction['category']:<15}"
            f"{transaction['amount']:<10.2f}"
            f"{transaction['description']:<25}"
            f"{transaction['day']:02}/{transaction['month']:02}/{transaction['year']:04}"
        )

    def month_summary(self, what_month, what_year):
        self.print_header()

        for transaction in self.transactions:
            if transaction["month"] == what_month and transaction["year"] == what_year:
                self.print_transaction(transaction)
        print("-" * 75)

    def category_summary(self, what_category, what_year=None):
        if what_year != None:
            self.print_header()

            for transaction in self.transactions:
                if (
                    transaction["category"] == what_category
                    and transaction["year"] == what_year
                ):
                    self.print_transaction(transaction)

            print("-" * 75)
        else:
            self.print_header()

            for transaction in self.transactions:
                if transaction["category"] == what_category:
                    self.print_transaction(transaction)

            print("-" * 75)

    def check_budget(self, what_month, what_year):
        Income = 0
        Outgoing = 0
        self.print_header()

        for transaction in self.transactions:
            if (
                transaction["category"] == "Income"
                and transaction["month"] == what_month
                and transaction["year"] == what_year
            ):
                self.print_transaction(transaction)

                Income = Income + transaction["amount"]
        print("-" * 75)
        for transaction in self.transactions:
            if (
                (
                    transaction["category"] == "Expense"
                    or transaction["category"] == "Investment"
                )
                and transaction["month"] == what_month
                and transaction["year"] == what_year
            ):
                self.print_transaction(transaction)
                Outgoing = Outgoing + transaction["amount"]
        print("-" * 75)
        rem_budget = Income - Outgoing
        print(f"Your Budget is {rem_budget}")


tracker = FinanceTracker()
tracker.load_data()
is_on = True
while is_on:
    print("*****************************")
    print("  PERSONAL FINANCE TRACKER")
    print("*****************************")
    print("1. Add Transactions")
    print("2. View Transactions")
    print("3. Delete Transactions")
    print("4. Monthly Summary")
    print("5. Category Summary")
    print("6. Check Budget")
    print("7. Save Data")
    print("8. Exit")
    valid_response = True
    while valid_response:
        try:
            response = int(input("What would you like to do?: "))
            if 0 < response < 9:
                valid_response = False
            else:
                print("Enter a number between 1 and 8")
        except ValueError:
            print("You must enter a number")

    if response == 1:
        cat = input("Enter category: ").capitalize()
        valid_cat = True
        while valid_cat:
            cat = input("Enter category (Income/Expense/Investment): ").capitalize()
            if cat in ["Income", "Expense", "Investment"]:
                valid_cat = False
            else:
                print("Please enter Income, Expense, or Investment")
        valid_amnt = True
        while valid_amnt:
            try:
                amnt = float(input("Enter the amount: "))   
                if amnt <= 0:
                    print("Amount can't be negative or zero")
                else:
                    valid_amnt = False

            except ValueError:
                print("Invalid input")

        valid_desc = True
        while valid_desc:
            desc = input("Enter a description (Upto 25 characters): ")
            if len(desc) > 25:
                print("Description can only be 25 characters long")
            else:
                valid_desc = False
        valid_date = True
        while valid_date:
            try:
                day = int(input("Enter the day: "))
                month = int(input("Enter the month (1-12): "))
                year = int(input("Enter the year: "))

                datetime.datetime(year, month, day)
                valid_date = False
            except ValueError:
                print("Enter a valid date")

        new_id = tracker.get_new_id()
        t1 = Transaction(
            id=new_id,
            category=cat,
            amount=amnt,
            description=desc,
            day=day,
            month=month,
            year=year,
        )
        t1_dict = t1.to_dict()
        tracker.add_transaction(t1_dict)
    if response == 2:
        tracker.print_header()

        for transaction in tracker.transactions:
            tracker.print_transaction(transaction)
        print("-" * 75)
    if response == 3:
        valid_del_id = True
        while valid_del_id:
            try:
                del_id = int(input("Enter ID of transaction you want to delete: "))
                if del_id > 0:
                    valid_del_id = False
                else:
                    print("ID cant be zero or negative")
            except ValueError:
                print("Invalid ID")
        tracker.del_transaction(del_id=del_id)

    if response == 4:
        valid_sum_month_year = True
        while valid_sum_month_year:
            try:
                what_month = int(input("Summary of what month?: "))
                what_year = int(input("In what year?: "))
                datetime.datetime(what_year, what_month, 1)
                valid_sum_month_year = False
            except ValueError:
                print("Enter valid month and/or year")

        print(f"{months.get(what_month)} {what_year} Summary:")
        tracker.month_summary(what_month, what_year)

    if response == 5:
        what_category = input("Enter the category: ").capitalize()
        cat_year = input("Do you want a specific year? (Y/N): ").capitalize()
        while cat_year not in ["Y", "N"]:
            print("Please enter Y or N")
            cat_year = input("Do you want a specific year? (Y/N): ").capitalize()
        if cat_year == "Y":
            valid_cat_year = True
            while valid_cat_year:
                try:

                    what_year = int(input("In what year?: "))
                    datetime.datetime(what_year, 1, 1)
                    valid_cat_year = False
                except ValueError:
                    print("Enter valid year")
            print(f"{what_category} {what_year} Summary: ")
            tracker.category_summary(what_category=what_category, what_year=what_year)
        else:
            print(f"{what_category} Summary: ")
            tracker.category_summary(what_category=what_category)

    if response == 6:
        valid_budget_month_year = True
        while valid_budget_month_year:
            try:
                what_month = int(
                    input("Budget of which month would you like to check?: ")
                )
                what_year = int(input("What year?: "))
                datetime.datetime(what_year, what_month, 1)
                valid_budget_month_year = False
            except ValueError:
                print("Enter valid month and/or year")

        print(f"Budget of {what_month} {what_year}")
        tracker.check_budget(what_month, what_year)

    if response == 7:
        tracker.save_data()
        print("Transactions Saved")
    if response == 8:
        tracker.save_data()
        print("Transactions Saved")
        print("Have a nice day!")
        is_on = False
