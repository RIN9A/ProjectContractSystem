
from datetime import datetime


class Project:

    def __init__(self, name):
        self.name = name
        self.creation_date = datetime.now().strftime("%Y-%m-%d")
        self.contracts = []

    def add_contract(self, contract):
        if contract in self.contracts:
            print('Договор уже добавлен в проект')

        elif contract.status != 'Активен':
            print('Договор должен быть активным')

        elif any(c.status == 'Активен' for c in self.contracts):
            print('В проекте уже есть активный договор')

        else:
            self.contracts.append(contract)
            contract.project = self

    def finish_contract(self, contract):
        if contract in self.contracts:
            contract.finish_contract()
            contract.project = None

