from hh_api import get_companies_list, get_all_vacancies_for_companies
from db_manager import DBManager

# Конфигурация подключения к PostgreSQL
db_config = {
    'dbname': 'postgres',  # Замените на имя вашей базы данных
    'user': 'postgres',  # Замените на имя вашего пользователя
    'password': '123456',  # Замените на ваш пароль
    'host': 'localhost'  # Замените на хост, если требуется
}


def user_interface(db_manager):
    """Интерфейс для взаимодействия с пользователем"""
    while True:
        print("\n1. Список всех компаний и вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Вакансии по ключевому слову")
        print("6. Выход")

        choice = input("Выберите опцию: ")

        if choice == "1":
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"{company['name']}: {company['vacancy_count']} вакансий")
        elif choice == "2":
            vacancies = db_manager.get_all_vacancies()
            for vacancy in vacancies:
                print(
                    f"{vacancy['name']} - {vacancy['title']}: {vacancy['salary_min']} - {vacancy['salary_max']}, {vacancy['url']}")
        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")
        elif choice == "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            for vacancy in vacancies:
                print(
                    f"{vacancy['name']} - {vacancy['title']}: {vacancy['salary_min']} - {vacancy['salary_max']}, {vacancy['url']}")
        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vacancy in vacancies:
                print(
                    f"{vacancy['name']} - {vacancy['title']}: {vacancy['salary_min']} - {vacancy['salary_max']}, {vacancy['url']}")
        elif choice == "6":
            break
        else:
            print("Неверный выбор!")


def main():
    """Главная функция для запуска программы"""
    db_manager = DBManager(db_config)
    db_manager.create_tables()

    # Получение списка компаний и их вакансий
    companies = get_companies_list()
    all_vacancies = get_all_vacancies_for_companies(companies)

    # Заполнение базы данных
    for company in companies:
        company_id = db_manager.insert_company(company['name'], company.get('industry', ''), company.get('area', ''))
        for vacancy in all_vacancies:
            if vacancy['employer']['id'] == company['id']:
                db_manager.insert_vacancy(vacancy['name'], vacancy['salary']['from'], vacancy['salary']['to'],
                                          company_id, vacancy['alternate_url'])

    # Интерфейс пользователя
    user_interface(db_manager)

    db_manager.close()


if __name__ == "__main__":
    main()
