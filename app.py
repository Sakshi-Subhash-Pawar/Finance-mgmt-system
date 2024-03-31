from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

class Transaction:
    def __init__(self, amount, category, transaction_type, date=None):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = date if date else datetime.datetime.now()

class FinanceManagementSystem:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_total_income(self):
        return sum(transaction.amount for transaction in self.transactions if transaction.transaction_type == 'income')

    def get_total_expenses(self):
        return sum(transaction.amount for transaction in self.transactions if transaction.transaction_type == 'expense')

    def get_total_loan(self):
        return sum(transaction.amount for transaction in self.transactions if transaction.transaction_type == 'loan')

    def get_total_investment(self):
        return sum(transaction.amount for transaction in self.transactions if transaction.transaction_type == 'investment')

    def generate_spending_report(self, start_date=None, end_date=None):
        if not start_date:
            start_date = datetime.datetime.min
        if not end_date:
            end_date = datetime.datetime.now()

        filtered_transactions = [transaction for transaction in self.transactions if start_date <= transaction.date <= end_date]

        report = {}
        for transaction in filtered_transactions:
            if transaction.category not in report:
                report[transaction.category] = 0
            report[transaction.category] += transaction.amount

        return report

finance_system = FinanceManagementSystem()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        transaction_type = request.form['type']
        date_str = request.form['date']
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d") if date_str else None
        transaction = Transaction(amount, category, transaction_type, date)
        finance_system.add_transaction(transaction)
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/report')
def report():
    today = datetime.datetime.now()
    start_of_month = datetime.datetime(today.year, today.month, 1)
    spending_report = finance_system.generate_spending_report(start_date=start_of_month)
    total_income = finance_system.get_total_income()
    total_expenses = finance_system.get_total_expenses()
    total_investment = finance_system.get_total_investment()
    total_loans = finance_system.get_total_loan()
    return render_template('report.html', report=spending_report, total_income=total_income, total_expenses=total_expenses, total_investment=total_investment, total_loans=total_loans)

if __name__ == '__main__':
    app.run(debug=True)
