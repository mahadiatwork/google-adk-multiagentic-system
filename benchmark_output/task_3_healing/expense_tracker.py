import click
import csv
import os

CSV_FILE = 'expenses.csv'

@click.group()
def cli():
    """CLI Expense Tracker"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Amount', 'Category', 'Description'])

@cli.command()
@click.option('--amount', type=float, required=True, help='Amount of the expense')
@click.option('--category', required=True, help='Category of the expense')
@click.option('--description', required=True, help='Description of the expense')
def add(amount, category, description):
    """Add an expense"""
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Get the last ID and increment it
        last_id = get_last_id() + 1
        writer.writerow([last_id, amount, category, description])
    click.echo(f"Expense added: {amount} - {category} - {description}")

@cli.command()
def view():
    """View all expenses"""
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            click.echo(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

@cli.command()
@click.option('--id', type=int, required=True, help='ID of the expense to delete')
def delete(id):
    """Delete an expense"""
    expenses = []
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if int(row[0]) != id:
                expenses.append(row)
    
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(expenses)
    
    click.echo(f"Expense with ID {id} deleted.")

def get_last_id():
    """Get the last expense ID"""
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if len(rows) > 1:
            return int(rows[-1][0])
        return 0

if __name__ == '__main__':
    cli()