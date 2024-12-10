import psycopg2
from typing import Optional, Any, List


class DBManager:
    def __init__(self, db_params):
        """Initialize connection to the database"""
        self.connection = psycopg2.connect(**db_params)  # Connect to the database
        self.cursor = self.connection.cursor()  # Create a cursor for executing queries

    def insert_company(self, company_name: str, industry: Optional[str] = None, area: Optional[str] = None) -> int:
        """Insert a company to the companies table"""
        query = """
            INSERT INTO companies (name, industry, area)
            VALUES (%s, %s, %s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
        """
        self.cursor.execute(query, (company_name, industry, area))  # Try to insert the company
        self.connection.commit()  # Save changes
        result = self.cursor.fetchone()  # Get returned id if inserted
        if result:
            return result[0]  # Return id of the inserted company
        else:
            query = "SELECT id FROM companies WHERE name = %s"  # Get id of the existing company
            self.cursor.execute(query, (company_name,))
            return self.cursor.fetchone()[0]  # Return the existing id

    def insert_vacancy(self, company_id: int, vacancy_title: str, salary_min: Optional[int], salary_max: Optional[int],
                       vacancy_url: str):
        """Insert a single vacancy to the vacancies table"""
        query = """
            INSERT INTO vacancies (title, salary_min, salary_max, url, company_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
        """
        self.cursor.execute(query, (vacancy_title, salary_min, salary_max, vacancy_url, company_id))  # Insert vacancy
        self.connection.commit()  # Save changes

    def insert_vacancies_bulk(self, vacancies: List[tuple]):
        """Insert multiple vacancies to the vacancies table"""
        query = """
            INSERT INTO vacancies (title, salary_min, salary_max, url, company_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
        """
        self.cursor.executemany(query, vacancies)  # Insert all vacancies in one query
        self.connection.commit()  # Save changes

    def get_companies_and_vacancies_count(self) -> List[tuple[Any, ...]]:
        """Get list of companies with count of vacancies"""
        query = """
            SELECT c.name, COUNT(v.id)
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.id
        """
        self.cursor.execute(query)  # Execute query
        return self.cursor.fetchall()  # Return all results

    def get_all_vacancies(self) -> List[tuple[Any, ...]]:
        """Get all vacancies and associated company names"""
        query = """
            SELECT v.title, v.salary_min, v.salary_max, v.url, c.name
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
        """
        self.cursor.execute(query)  # Execute the query
        return self.cursor.fetchall()  # Return all results

    def get_avg_salary(self) -> Optional[float]:
        """Calculate and return the average salary of all vacancies"""
        query = """
            SELECT AVG((COALESCE(v.salary_min, 0) + COALESCE(v.salary_max, 0)) / 2.0) AS avg_salary
            FROM vacancies v
            WHERE v.salary_min IS NOT NULL OR v.salary_max IS NOT NULL
        """
        self.cursor.execute(query)  # Execute the query
        return self.cursor.fetchone()[0]  # Return the average salary

    def get_vacancies_with_higher_salary(self) -> List[tuple[Any, ...]]:
        """Get vacancies where the average salary is higher than the overall average salary"""
        avg_salary = self.get_avg_salary()  # Get the overall average salary
        if avg_salary is None:
            return []  # Return an empty list if no salary data is available
        query = """
            SELECT v.title, v.salary_min, v.salary_max, v.url, c.name
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE ((COALESCE(v.salary_min, 0) + COALESCE(v.salary_max, 0)) / 2.0) > %s
        """
        self.cursor.execute(query, (avg_salary,))  # Find vacancies with higher average salary
        return self.cursor.fetchall()  # Return all results

    def get_vacancies_with_keyword(self, keyword: str) -> List[tuple[Any, ...]]:
        """Find vacancies with a specific keyword in their title"""
        query = """
            SELECT v.title, v.salary_min, v.salary_max, v.url, c.name
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.title ILIKE %s
        """
        self.cursor.execute(query, ('%' + keyword + '%',))  # Search for keyword in title
        return self.cursor.fetchall()  # Return all matching results

    def close_connection(self):
        """Close the connection to the database"""
        if self.cursor:
            self.cursor.close()  # Close the cursor
        if self.connection:
            self.connection.close()  # Close the connection
