## CIS6930SP24 Assignment 0

Rahul Reddy Vade ::: 14288319

This repository contains code for processing incident data from a given URL and storing it in a SQLite database. The project structure is organized as follows:

- **COLLABORATORS.md:** File listing project collaborators.
- **Pipfile:** Configuration file for managing project dependencies using Pipenv.
- **README.md:** Project documentation.
- **assignment0:** Directory containing the main Python script.
  - **main.py:** Main script for processing incident data.
  - **assignment0.py:** Module containing functions for fetching, extracting, and managing incident data.
- **resources:** Directory for storing project-related resources.
  - **normanpd.db:** SQLite database file for storing incident data.
- **setup.cfg:** Configuration file for pytest.
- **setup.py:** Project setup file.
- **tests:** Directory containing test scripts.
  - **testassignment0.py:** Test script for testing the assignment0 module.

## Usage

1. Install dependencies using Pipenv:

   ```bash
   pipenv install


2. Execute the main script with the desired incident data URL:

  ```bash
  pipenv run python assignment0/main.py --incidents <url>
  ```

##Project Overview

#main.py
The main.py script serves as the entry point for the project. It utilizes the functions defined in the assignment0 module to download incident data from a specified URL, extract relevant information, create a SQLite database, and populate it with the extracted data.

#assignment0.py
The assignment0.py module contains the following functions:

fetchincidents(url): Downloads incident data from a given URL using the urllib library.
extractincidents(incident_data): Extracts relevant incident information from PDF data, assuming a variable number of columns on each page. The extracted data is formatted to match the database schema.
createdb(): Creates or connects to the SQLite database (normanpd.db) and initializes the 'incidents' table if it does not exist.
populatedb(db, incidents): Connects to the specified database and inserts incident data into the 'incidents' table.
status(db): Connects to the database and prints a summary of incident data, including the count of each non-empty nature.




Running Tests

To run tests, use the following command:
```bash
pipenv run pytest
```


...
