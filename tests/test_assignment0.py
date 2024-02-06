import pytest
from assignment0.assignment0 import extractincidents, createdb, populatedb, status
import sqlite3

# Mock incident_data for testing
incident_data = b"Mock incident data"
incidents = extractincidents(incident_data)

def test_extractincidents():
    assert isinstance(incidents, list)
    # Add more assertions based on your requirements

def test_createdb():
    # Create a temporary database for testing
    test_db = 'resources/test_db.db'
    createdb(test_db)
    
    # Check if the database file is created
    assert os.path.exists(test_db)
    
    # Clean up: remove the temporary database
    os.remove(test_db)

def test_populatedb():
    # Create a temporary database for testing
    test_db = 'resources/test_db.db'
    createdb(test_db)

    # Insert data into the temporary database
    populatedb(test_db, incidents)

    # Connect to the database and check if data is inserted
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents")
    count = cursor.fetchone()[0]

    assert count == len(incidents)

    # Clean up: remove the temporary database
    os.remove(test_db)

def test_status():
    # Create a temporary database for testing
    test_db = 'resources/test_db.db'
    createdb(test_db)

    # Insert data into the temporary database
    populatedb(test_db, incidents)

    # Print the status and check for output
    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        status(test_db)
        output = mock_stdout.getvalue()

    assert len(output.strip()) > 0

    # Clean up: remove the temporary database
    os.remove(test_db)
