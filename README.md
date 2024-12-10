# Course Project: Job Vacancies Management System

This project provides a service that manages job vacancies by fetching data from the HeadHunter (hh.ru) API and storing it in a PostgreSQL database. It allows users to interact with the database to view vacancies, calculate average salaries, and perform keyword-based searches.

## Main Functions

### Home Page
The main page of the service performs the following tasks:

- Fetches job vacancies for specified companies from the HeadHunter API.
- Saves the fetched data into a PostgreSQL database.
- Provides a text-based menu for interacting with the database and viewing the results.

### Services
The project allows users to perform the following actions:

- **View All Vacancies**: Lists all the job vacancies stored in the database.
- **View Vacancy Count per Company**: Displays the total number of vacancies available for each company.
- **View Average Salary**: Calculates and displays the average salary across all vacancies.
- **Search Vacancies by Keyword**: Allows users to search for vacancies based on a keyword present in the job title.
- **View Vacancies with Higher-than-Average Salaries**: Displays vacancies with salaries higher than the calculated average salary.

## Modules

### Module: `db_manager.py`
Functions:

- `insert_company`: Inserts a company into the database (if it doesn't already exist) and returns the company's ID.
- `insert_vacancy`: Inserts a single vacancy into the database.
- `insert_vacancies_bulk`: Inserts multiple vacancies into the database in bulk.
- `get_companies_and_vacancies_count`: Retrieves the number of vacancies available for each company.
- `get_all_vacancies`: Fetches all job vacancies and associated company names.
- `get_avg_salary`: Calculates the average salary from all vacancies.
- `get_vacancies_with_higher_salary`: Finds vacancies with salaries higher than the average salary.
- `get_vacancies_with_keyword`: Searches for vacancies by a specified keyword in the title.
- `close_connection`: Closes the connection to the database.

### Module: `hh_api.py`
Functions:

- `get_vacancies_for_company`: Fetches job vacancies for a specific company from the HeadHunter API, with pagination support.

### Module: `main.py`
Functions:

- `main.py`: Main application script that integrates with the `DBManager` and `hh_api.py`. It fetches data from the HeadHunter API, inserts it into the database, and provides an interactive menu for user interaction.

## Environment Variables

Environment variables are stored in the `db.ini` file, which contains the database connection parameters:

```ini
[database]
dbname = your_database_name
user = your_database_user
password = your_database_password
host = your_database_host
