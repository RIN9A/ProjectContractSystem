import sqlite3
from Contract import Contract
from Project import Project

conn = sqlite3.connect('project_contract.db')


def create_contract():
    name = input('Введите название договора: ')
    contract = Contract(name)
    return contract


def create_project():
    name = input('Введите название проекта: ')
    project = Project(name)
    return project


def confirm_contract():
    print('Список договоров:')
    for i, contract in enumerate(contracts):
        print(f'{i + 1}. {contract.name}')

    contract_index = int(input('Выберите номер договора для подтверждения: ')) - 1
    contract = contracts[contract_index]
    contract.confirm_contract()
    print(f'Договор "{contract.name}" был подтвержден')


def finish_contract():
    print('Список договоров:')
    for i, contract in enumerate(contracts):
        print(f'{i + 1}. {contract.name}')

    contract_index = int(input('Выберите номер договора для завершения: ')) - 1
    contract = contracts[contract_index]
    contract.finish_contract()
    print(f'Договор "{contract.name}" был завершен')


def print_projects():
    print('Список проектов: ')
    for i, project in enumerate(projects):
        print(f'{i + 1}.{project.name}')

    print('Список договоров: ')
    for i, contract in enumerate(contracts):
        print(f'{i + 1}.{contract.name}')


def print_menu():
    print('1. Проект')
    print('2. Договор')
    print('3. Завершить работу с программой')


cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS contracts
                (name TEXT, creation_date TEXT,
                signed_date TEXT, status TEXT, project_id INTEGER,
                FOREIGN KEY(project_id) REFERENCES
                projects(rowid))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS projects
                (name TEXT, creation_date TEXT)''')
conn.commit()

projects = []
contracts = []

while True:
    print_menu()
    choice = input('Выберите пункт меню: \n')
    if choice == '1':
        project_name = input('Введите название проекта: \n')
        project = Project(project_name)
        projects.append(project)
        while True:
            print('1. Создать договор')
            print('2. Добавить договор')
            print('3. Завершить договор')
            print('4. Назад\n')
            project_choice = input('Выберите пункт меню: \n')

            if project_choice == '1':
                contract = create_contract()
                contracts.append(contract)

                cursor.execute("INSERT INTO contracts VALUES (?, ?, ?, ?, ?)",
                               (contract.name,
                                contract.creation_date, contract.signed_date,
                                contract.status, None
                                ))
                conn.commit()

            elif project_choice == '2':
                if not contracts:
                    print('Должен существовать хотя бы один активный договор\n')
                    continue
                print('Список договоров:\n')
                for i, contract in enumerate(contracts):
                    if contract.status == 'Активен' and contract.project is None:
                        print(f'{i + 1}. {contract.name}')

                contract_index = int(input('Выберите номер договора для добавления: \n')) - 1
                contract = contracts[contract_index]
                project.add_contract(contract)

                cursor.execute("UPDATE contracts SET project_id = ? WHERE name = ?", (project.name, contract.name))
                conn.commit()

            elif project_choice == '3':
                if not contracts:
                    print('Должен существовать хотя бы один активный договор\n')
                    continue
                print('Список договоров:\n')
                for i, contract in enumerate(contracts):
                    if contract.project == project:
                        print(f'{i + 1}. {contract.name}')

                contract_index = int(input('Выберите номер договора для завершения: \n')) - 1
                contract = contracts[contract_index]
                project.finish_contract(contract)

                cursor.execute("UPDATE contracts SET project_id = ? WHERE name = ?", (None, contract.name))
                conn.commit()

            elif project_choice == '4':
                break

    elif choice == '2':
        while True:
            print('1. Создать договор')
            print('2. Подтвердить договор')
            print('3. Завершить договор')
            print('4. Назад')
            contract_choice = input('Выберите пункт меню: \n')

            if contract_choice == '1':
                contract = create_contract()
                contracts.append(contract)

                cursor.execute("INSERT INTO contracts VALUES (?, ?, ?, ?, ?)",
                               (contract.name, contract.creation_date, contract.signed_date,
                                contract.status, None))
                conn.commit()

            elif contract_choice == '2':
                if not contracts:
                    print('Должен существовать хотя бы один договор\n')
                    continue

                confirm_contract()
                cursor.execute("UPDATE contracts SET signed_date = ?, status = ? WHERE name = ?",
                               (contract.signed_date, contract.status, contract.name))
                conn.commit()

            elif contract_choice == '3':
                if not contracts:
                    print('Должен существовать хотя бы один договор\n')
                    continue

                finish_contract()

                cursor.execute("UPDATE contracts SET status = ? WHERE name = ?",
                               (contract.status,
                                contract.name))

                conn.commit()

            elif contract_choice == '4':
                break

    elif choice == '3':
        break

    print_projects()

conn.close()


