import csv
from datetime import datetime

CSV_FILE = 'expenses.csv'

def initialize_csv():
    try:
        with open(CSV_FILE, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Description', 'Amount'])
    except FileExistsError:
        pass

def add_expense():
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    description = input("Enter expense description: ")
    try:
        amount = float(input("Enter expense amount: "))
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return
    
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, description, amount])
    
    print("Expense added successfully.")

def view_expenses():
    try:
        with open(CSV_FILE, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                print(f"Date: {row[0]}, Description: {row[1]}, Amount: {row[2]}")
    except FileNotFoundError:
        print("No expenses found. Please add some expenses first.")
    except PermissionError:
        print("Permission denied. Unable to read the expenses file.")

def main():
    initialize_csv()
    while True:
        print("\nOptions: add, view, exit")
        command = input("Enter command: ").strip().lower()
        
        if command == 'add':
            add_expense()
        elif command == 'view':
            view_expenses()
        elif command == 'exit':
            print("Exiting the application.")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()