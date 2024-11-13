import requests

HH_API_URL = "https://api.hh.ru"

def get_companies_list(page=0):
    """Получение списка работодателей с hh.ru"""
    url = f"{HH_API_URL}/employers"
    params = {'page': page, 'per_page': 20}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['items']
    else:
        return []

def get_vacancies_for_company(company_id, page=0):
    """Получение вакансий для конкретной компании"""
    url = f"{HH_API_URL}/vacancies"
    params = {'employer_id': company_id, 'page': page, 'per_page': 20}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['items']
    else:
        return []

def get_all_vacancies_for_companies(companies):
    """Получение всех вакансий для списка компаний"""
    all_vacancies = []
    for company in companies:
        company_id = company['id']
        vacancies = get_vacancies_for_company(company_id)
        all_vacancies.extend(vacancies)
    return all_vacancies
