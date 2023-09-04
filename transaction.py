class Transaction:
    def __init__(self, date, category, description, amount):
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount

    def __repr__(self):
        return f'(Date: {self.date}, Category: {self.category}, \
        Description: {self.description}, Amount: {self.amount})'
