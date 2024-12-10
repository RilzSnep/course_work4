import configparser
from db_manager import DBManager
from hh_api import get_vacancies_for_company

#  Import necessary modules and classes
config = configparser.ConfigParser()
config.read('database.ini')  # Read database configuration from .ini file

# Create a dictionary with database connection parameters
db_params = {
    'dbname': config['database']['dbname'],
    'user': config['database']['user'],
    'password': config['database']['password'],
    'host': config['database']['host']
}


db_manager = DBManager(db_params)

#  Define a list of companies with ID and name
company_list = [
    {'id': '1', 'name': 'Компания 1'},
    {'id': '2', 'name': 'Компания 2'}
]


for company_info in company_list:
    #  Extract employer ID and name from the company info
    employer_id = company_info['id']
    employer_name = company_info['name']

    #  Get vacancies for current company HH API
    company_vacancies = get_vacancies_for_company(employer_id, pages=5)

    #  Insert the company to database and get its database ID
    db_company_id = db_manager.insert_company(employer_name)

    # Prepare a list of vacancy records to insert in bulk
    vacancy_records = []
    for company_vacancy in company_vacancies:
        # Extract vacancy title or set default if missing
        vacancy_title = company_vacancy.get('name', 'Не указано')

        #  Extract salary details or set none if missing
        salary_details = company_vacancy.get('salary')
        salary_min = salary_details.get('from') if salary_details else None
        salary_max = salary_details.get('to') if salary_details else None

        # Extract vacancy URL or set default if missing
        vacancy_url = company_vacancy.get('alternate_url', 'Нет ссылки')

        #  Add vacancy details to the list
        vacancy_records.append((vacancy_title, salary_min, salary_max, vacancy_url, db_company_id))

    # Insert all vacancies to the database
    db_manager.insert_vacancies_bulk(vacancy_records)

# Provide a menu for user interaction with the database
while True:
    print("\nВыберите действие:")
    print("1: Вывести все вакансии")
    print("2: Вывести количество вакансий по компаниям")
    print("3: Вывести среднюю зарплату")
    print("4: Вывести вакансии по ключевому слову")
    print("5: Вывести вакансии с зарплатой выше средней")
    print("6: Выйти")

    # Get user choice
    choice = input("Введите номер действия (1-6): ")

    if choice == '1':
        #Fetch all vacancies from the database
        vacancies = db_manager.get_all_vacancies()

        # Print each vacancy with details
        for vacancy in vacancies:
            print(
                f"Вакансия: {vacancy[0]}, От {vacancy[1]} до {vacancy[2]}, Ссылка: {vacancy[3]}, Компания: {vacancy[4]}")
    elif choice == '2':
        companies = db_manager.get_companies_and_vacancies_count()
        for company in companies:
            print(f"Компания: {company[0]}, Количество вакансий: {company[1]}")
    elif choice == '3':
        avg_salary = db_manager.get_avg_salary()
        if avg_salary:
            print(f"Средняя зарплата: {avg_salary:.2f}")
        else:
            print("Нет данных о зарплатах.")
    elif choice == '4':
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        vacancies = db_manager.get_vacancies_with_keyword(keyword)
        for vacancy in vacancies:
            print(
                f"Вакансия: {vacancy[0]}, От {vacancy[1]} до {vacancy[2]}, Ссылка: {vacancy[3]}, Компания: {vacancy[4]}")
    elif choice == '5':
        vacancies = db_manager.get_vacancies_with_higher_salary()
        for vacancy in vacancies:
            print(
                f"Вакансия: {vacancy[0]}, От {vacancy[1]} до {vacancy[2]}, Ссылка: {vacancy[3]}, Компания: {vacancy[4]}")
    elif choice == '6':
        db_manager.close_connection()
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите действие от 1 до 6.")
