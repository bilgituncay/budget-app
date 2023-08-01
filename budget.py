class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total_funds = 0
        for item in self.ledger:
            total_funds += item['amount']
        return total_funds

    def transfer(self, amount, target_category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + target_category.category)
            target_category.deposit(amount, "Transfer from " + self.category)
            return True
        return False

    def check_funds(self, amount):
        total_funds = self.get_balance()
        return total_funds >= amount

    def __str__(self):
        category_print = self.category.center(30, '*')
        amounts = []
        descriptions = []
        for item in self.ledger:
            amounts.append(item['amount'])
            descriptions.append(item['description'][:23])
        for i in range(len(amounts)):
            formatted_amount = f"{amounts[i]:.2f}"
            truncated_amount = formatted_amount[:7]
            category_print += f"\n{descriptions[i]:<23}{truncated_amount:>7}"
        category_print += f"\nTotal: {self.get_balance()}"
        return category_print

def create_spend_chart(args):
    spendings = dict()
    for i in args:
        total_spent_in_cat = 0
        for item in i.ledger:
            if item['amount'] < 0:
                total_spent_in_cat -= item['amount']
        spendings[i.category] = total_spent_in_cat

    total_spent = sum(spendings.values())
    percentages = {category: (spending / total_spent) * 100 for category, spending in spendings.items()}

    chart = "Percentage spent by category\n"
    for i in range(100, -10, -10):
        chart += f"{i:3}| "
        for percentage in percentages.values():
            if percentage >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    chart += "    " + "-" * (len(percentages) * 3 + 1) + "\n"

    max_category_length = max(len(category) for category in percentages.keys())
    for i in range(max_category_length):
        chart += " " * 5
        for category in percentages.keys():
            if i < len(category):
                chart += category[i] + "  "
            else:
                chart += "   "
        if i != max_category_length - 1:
            chart += "\n"

    return chart