import unittest
import os
import tempfile
from assignment0.assignment0 import fetchincidents, extractincidents, createdb, populatedb, status

class TestAssignment0(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        # Mock database path for testing
        self.mock_db_path = os.path.join(self.temp_dir.name, 'test_db.db')
        # Create the database and necessary table
        createdb()  # Call createdb without any arguments


    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_fetchincidents(self):
    # Mock a URL and fetch incidents
        url = 'https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf'
        incidents_data = fetchincidents(url)

    # Assert that incidents_data is not None
        self.assertIsNotNone(incidents_data)
        # ...

    def test_extractincidents(self):
        # Mock incident data
        incident_data = b'Mock PDF data'

        # Call extractincidents and assert the expected behavior
        incidents = extractincidents(incident_data)

        # Additional assertions based on the expected behavior of extractincidents
        # ...

        # Clean up or additional assertions as needed
        # ...

    def test_createdb(self):
        # Call createdb and assert the expected behavior
        db_path = createdb()

        # Assert that the database file is created at the expected path
        self.assertTrue(os.path.isfile(db_path))

        # Additional assertions based on the expected behavior of createdb
        # ...

        # Clean up or additional assertions as needed
        # ...

    def test_populatedb(self):
    # Mock a database path and incidents
        db_path = os.path.join(os.getcwd(), 'resources', 'normanpd.db')
        incidents = [('2022-01-01', '1', 'Location1', 'Nature1', 'ORI1')]

    # Ensure the database is created before calling populatedb
        createdb()  # Remove the argument since createdb doesn't take any

    # Call populatedb and assert the expected behavior
        populatedb(db_path, incidents)

    def test_status(self):
        # Mock a database path
        db_path = 'mock_db_path.db'

        # Call status and assert the expected behavior
        # Note: Since status prints to the console, you may need to capture the printed output
        # and assert against it, or consider refactoring the status function to return data.
        # ...

        # Additional assertions based on the expected behavior of status
        # ...

        # Clean up or additional assertions as needed
        # ...

if __name__ == '__main__':
    unittest.main()
