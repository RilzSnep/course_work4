import psycopg2
from typing import Optional, Any, List


class DBManager:
    def __init__(self, db_params):
        self.connection = psycopg2.connect(**db_params)
        self.cursor = self.connection.cursor()

    def insert_company(self, company_name: str, industry: Optional[str] = None, area: Optional[str] = None) -> int:
        query = "INSERT INTO companies (name, industry, area) VALUES (%s, %s, %s) ON CONFLICT (name) DO NOTHING RETURNING id"
        self.cursor.execute(query, (company_name, industry, area))
        self.connection.commit()
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            query = "SELECT id FROM companies WHERE name = %s"
            self.cursor.execute(query, (company_name,))
            return self.cursor.fetchone()[0]

    def insert_vacancy(self, company_id: int, vacancy_title: str, salary_min: Optional[int], salary_max: Optional[int],
                       vacancy_url: str):
        query = """
            INSERT INTO vacancies (title, salary_min, salary_max, url, company_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
        """
        self.cursor.execute(query, (vacancy_title, salary_min, salary_max, vacancy_url, company_id))
        self.connection.commit()

    def insert_vacancies_bulk(self, vacancies: List[tuple]):
        query = """
            INSERT INTO vacancies (title, salary_min, salary_max, url, company_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
        """
        self.cursor.executemany(query, vacancies)
        self.connection.commit()

    def get_companies_and_vacancies_count(self) -> List[tuple[Any, ...]]:
        query = """
            SELECT c.name, COUNT(v.id)
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> List[tuple[Any, ...]]:
        query = """
            SELECT v.title, v.salary_min, v.salary_max, v.url, c.name
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        query = """
            SELECT AVG((COALESCE(v.salary_min, 0) + COALESCE(v.salary_max, 0)) / 2.0) AS avg_salary
            FROM vacancies v
            WHERE v.salary_min IS NOT NULL OR v.salary_max IS NOT NULL
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[tuple[Any, ...]]:
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []

        query = """
            SELECT v.title, v.salary_min, v.salary_max, v.url, c.name
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE ((COALESCE(v.salary_min, 0) + COALESCE(v.salary_max, 0)) / 2.0) > %s
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[tuple[Any, ...]]:
        query = """
            SELECT v.title, v.salary_min, v.salary_max, v.url, c.name
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.title ILIKE %s
        """
        self.cursor.execute(query, ('%' + keyword + '%',))
        return self.cursor.fetchall()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
