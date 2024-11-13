import requests

BASE_URL = "https://api.hh.ru/"


def get_vacancies_for_company(employer_id=None, pages=1):
    all_vacancies = []
    params = {'employer_id': employer_id, 'per_page': 100} if employer_id else {'per_page': 100}
    url = f"{BASE_URL}vacancies"
    for page_number in range(pages):
        params['page'] = page_number
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            all_vacancies.extend(data.get('items', []))
            if len(data.get('items', [])) < 100:
                break
        else:
            print(f"Ошибка при получении данных о вакансиях: {response.status_code}")
            break

    return all_vacancies
