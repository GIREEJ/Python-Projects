import json
import csv
from datetime import datetime
import matplotlib.pyplot as plt

EXPENSE_FILE = "expenses.json"


def load_expenses(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_expenses(filename, expenses):
    with open(filename, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses):
    date_str = input("Enter date (YYYY-MM-DD): ")
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD")
        return

    category = input("Enter Category: ")
    description = input("Enter description: ")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    expense = {
        "date": date.isoformat(),
        "category": category,
        "description": description,
        "amount": amount,
    }
    expenses.append(expense)
    print("Expense added successfully!")


def view_expenses(expenses):
    if not expenses:
        print("No expenses found.")
    else:
        for i, expense in enumerate(expenses, start=1):
            print(
                f"{i}. Date: {expense['date']},"
                f" Category: {expense['category']},"
                f" Description: {expense['description']},"
                f" Amount: ₹{expense['amount']:.2f}"
            )
    print()


def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return

    try:
        index = int(input("Enter the number of the expense to delete: ")) - 1
        if 0 <= index < len(expenses):
            deleted_expense = expenses.pop(index)
            print(f"Deleted expense: {deleted_expense}")
        else:
            print("Invalid number. No expense deleted.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def edit_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return

    try:
        index = int(input("Enter the number of the expense to edit: ")) - 1
        if 0 <= index < len(expenses):
            print("Leave a field blank to keep it unchanged.")
            date_str = input(f"Enter new date(YYYY-MM-DD) [{expenses[index]['date']}]: ")
            category = input(f"Enter new category [{expenses[index]['category']}]: ")
            description = input(f"Enter new description [{expenses[index]['description']}]: ")
            amount_str = input(f"Enter new amount [{expenses[index]['amount']}]: ")

            if date_str:
                try:
                    expenses[index]['date'] = datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
                except ValueError:
                    print("Invalid date formate. keeping the existing date.")

            if category:
                expenses[index]['category'] = category

            if description:
                expenses[index]['description'] = description

            if amount_str:
                try:
                    expenses[index]['amount'] = float(amount_str)
                except ValueError:
                    print("Invalid amount. keeping the existing amount.")

            print("expense updated successfully.")
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input. Please enter a valid number. ")


def filter_expenses_by_date(expenses):
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalide date format. Please use YYYY-MM-DD.")
        return []

    filterd_expenses = [
        expense for expense in expenses
        if start_date <= datetime.fromisoformat(expense['date']).date() <= end_date
    ]
    return filterd_expenses


def filter_expenses_by_category(expenses):
    category = input("Enter category to filter by: ")
    filtered_expenses = [expense for expense in expenses if expense['category'].lower() == category.lower()]
    return filtered_expenses


def calculate_total_expenses(expenses):
    total = sum(expense['amount'] for expense in expenses)
    print(f"Total expenses: ₹{total:.2f}")


def calculate_total_expenses_by_category(expenses):
    totals = {}
    for expense in expenses:
        category = expense['category']
        if category in totals:
            totals[category] += expense['amount']
        else:
            totals[category] = expense['amount']

    print("Total expenses by category!")
    for category, total in totals.items():
        print(f"{category}: ₹{total:.2f}")


def export_expenses_to_csv(expenses):
    filename = input("Enter the CSV filename to export to: ")
    with open(filename, "w", newline="") as file:
        write = csv.writer(file)
        write.writerow(["Date", "Category", "Description", "Amount"])
        for expense in expenses:
            write.writerow([expense['date'], expense['category'], expense['description'], expense['amount']])

    print("Expenses exported to CSV successfully.")


def import_expenses_from_csv():
    filename = input("Enter the CSV filename to import from: ")
    expenses = []
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append({
                    "date": row['Date'],
                    "category": row['Category'],
                    "description": row['Description'],
                    "amount": float(row['Amount']),
                })
        print("Expenses imported from CSV successfully.")
    except FileNotFoundError:
        print("CSV file not found.")
    return expenses


def visualize_expenses(expenses):
    totals = calculate_total_expenses_by_category_dict(expenses)
    categories = list(totals.keys())
    amounts = list(totals.values())

    plt.figure(figsize=(10, 5))
    plt.bar(categories, amounts, color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.title('Ecpenses by Category')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def calculate_total_expenses_by_category_dict(expenses):
    totals = {}
    for expense in expenses:
        category = expense['category']
        if category in totals:
            totals[category] += expense['amount']
        else:
            totals[category] = expense['amount']
    return totals


def main():
    expenses = load_expenses(EXPENSE_FILE)

    while True:
        print("\nExpenses Tracker")
        print("1.  Add Expense")
        print("2.  View Expenses")
        print("3.  Remove/Delete Expense")
        print("4.  Edit Expense")
        print("5.  Filter Expenses by Date")
        print("6.  Filter Expenses by Category")
        print("7.  Calculate Total Expenses")
        print("8.  Calculate Total Expenses by Category")
        print("9.  Export Expenses to CSV")
        print("10. Import Expenses from CSV")
        print("11. Visualize Expenses")
        print("12. Save and Exit")
        print("13. Exit without Saving")

        choice = input("Choose an Option: ")
        print("")
        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_expenses(expenses)
        elif choice == '3':
            delete_expense(expenses)
        elif choice == '4':
            edit_expense(expenses)
        elif choice == '5':
            filtered_expenses = filter_expenses_by_date(expenses)
            view_expenses(filtered_expenses)
        elif choice == '6':
            filtered_expenses = filter_expenses_by_category(expenses)
            view_expenses(filtered_expenses)
        elif choice == '7':
            calculate_total_expenses(expenses)
        elif choice == '8':
            calculate_total_expenses_by_category(expenses)
        elif choice == '9':
            export_expenses_to_csv(expenses)
        elif choice == '10':
            imported_expenses = import_expenses_from_csv()
            expenses.extend(imported_expenses)
        elif choice == '11':
            visualize_expenses(expenses)
        elif choice == '12':
            save_expenses(EXPENSE_FILE, expenses)
            print("Expenses saved. Exiting!")
            break
        elif choice == "13":
            print("Exiting without saving.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
