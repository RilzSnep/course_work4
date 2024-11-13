import psycopg2
from psycopg2 import sql
import psycopg2.extras

class DBManager:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def create_tables(self):
        """Создание таблиц для компаний и вакансий"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                industry VARCHAR(255),
                area VARCHAR(255)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                salary_min INT,
                salary_max INT,
                employer_id INT,
                url VARCHAR(255),
                FOREIGN KEY (employer_id) REFERENCES companies(id)
            );
        """)
        self.conn.commit()

    def insert_company(self, name, industry, area):
        """Вставка новой компании в базу данных"""
        self.cursor.execute("""
            INSERT INTO companies (name, industry, area)
            VALUES (%s, %s, %s) RETURNING id;
        """, (name, industry, area))
        company_id = self.cursor.fetchone()['id']
        self.conn.commit()
        return company_id

    def insert_vacancy(self, title, salary_min, salary_max, employer_id, url):
        """Вставка вакансии в базу данных"""
        self.cursor.execute("""
            INSERT INTO vacancies (title, salary_min, salary_max, employer_id, url)
            VALUES (%s, %s, %s, %s, %s);
        """, (title, salary_min, salary_max, employer_id, url))
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """Получение списка компаний с количеством вакансий"""
        self.cursor.execute("""
            SELECT c.name, COUNT(v.id) AS vacancy_count
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.employer_id
            GROUP BY c.name;
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Получение списка всех вакансий"""
        self.cursor.execute("""
            SELECT c.name, v.title, v.salary_min, v.salary_max, v.url
            FROM vacancies v
            JOIN companies c ON v.employer_id = c.id;
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Получение средней зарплаты по всем вакансиям"""
        self.cursor.execute("""
            SELECT AVG((salary_min + salary_max) / 2) AS avg_salary FROM vacancies;
        """)
        return self.cursor.fetchone()['avg_salary']

    def get_vacancies_with_higher_salary(self):
        """Получение вакансий с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        self.cursor.execute("""
            SELECT c.name, v.title, v.salary_min, v.salary_max, v.url
            FROM vacancies v
            JOIN companies c ON v.employer_id = c.id
            WHERE (v.salary_min + v.salary_max) / 2 > %s;
        """, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получение вакансий по ключевому слову в названии"""
        self.cursor.execute("""
            SELECT c.name, v.title, v.salary_min, v.salary_max, v.url
            FROM vacancies v
            JOIN companies c ON v.employer_id = c.id
            WHERE v.title LIKE %s;
        """, ('%' + keyword + '%',))
        return self.cursor.fetchall()

    def close(self):
        """Закрытие соединения с БД"""
        self.cursor.close()
        self.conn.close()
