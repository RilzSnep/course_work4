from db_manager import DBManager
from hh_api import get_vacancies_for_company

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
}

db_manager = DBManager(db_params)

company_list = [
    {'id': '1', 'name': 'Компания 1'},
    {'id': '2', 'name': 'Компания 2'}
]

for company_info in company_list:
    employer_id = company_info['id']
    employer_name = company_info['name']
    company_vacancies = get_vacancies_for_company(employer_id, pages=5)
    db_company_id = db_manager.insert_company(employer_name)

    vacancy_records = []
    for company_vacancy in company_vacancies:
        vacancy_title = company_vacancy.get('name', 'Не указано')
        salary_details = company_vacancy.get('salary')
        salary_min = salary_details.get('from') if salary_details else None
        salary_max = salary_details.get('to') if salary_details else None
        vacancy_url = company_vacancy.get('alternate_url', 'Нет ссылки')
        vacancy_records.append((vacancy_title, salary_min, salary_max, vacancy_url, db_company_id))

    db_manager.insert_vacancies_bulk(vacancy_records)

while True:
    print("\nВыберите действие:")
    print("1: Вывести все вакансии")
    print("2: Вывести количество вакансий по компаниям")
    print("3: Вывести среднюю зарплату")
    print("4: Вывести вакансии по ключевому слову")
    print("5: Вывести вакансии с зарплатой выше средней")
    print("6: Выйти")

    choice = input("Введите номер действия (1-6): ")

    if choice == '1':
        vacancies = db_manager.get_all_vacancies()
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
