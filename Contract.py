from datetime import datetime


class Contract:
    def __init__(self, name):
        self.name = name
        self.creation_date = datetime.now().strftime("%Y-%m-%d")
        self.signed_date = None
        self.status = 'Черновик'
        self.project = None

    def confirm_contract(self):
        self.signed_date = datetime.now().strftime("%Y-%m-%d")
        self.status = 'Активен'

    def finish_contract(self):
        self.status = 'Завершен'
