
import urllib.request
import io
import os
import sqlite3
import re
from pypdf import PdfReader



def fetchincidents(url):
    # Set a user-agent to avoid server rejection
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        # Open the URL and read the data
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
            incident_data = response.read()
            return incident_data
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None

def clean_text(text):
    return text.replace('\x00', '') 

def extractincidents(incident_data):
    incidents = []
    try:
        # Convert bytes data to a BytesIO object for PdfReader
        pdf_file = io.BytesIO(incident_data)
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    data = line.split()
                    if len(data) >= 5:
                        incident_time = data[0] + ' ' + data[1]
                        incident_number = data[2]
                        incident_location = " ".join(data[3:-2])
                        nature = data[-2]
                        incident_ori = data[-1]
                        incidents.append((incident_time, incident_number, incident_location, nature, incident_ori))
    except Exception as e:
        print(f"Failed to extract incidents from PDF: {e}")
    return incidents

def createdb():
    # Ensure 'resources' directory exists
    if not os.path.exists('resources'):
        os.makedirs('resources')

    # Connect to the database or create if it doesn't exist
    db_path = os.path.join(os.getcwd(), 'resources', 'normanpd.db')
    conn = sqlite3.connect(db_path)
    
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the SQL query to create the incidents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return db_path



def populatedb(db, incidents):
    # Connect to the database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Iterate over incidents and insert into the database
    for incident in incidents:
        # Unpack the tuple directly
        cursor.execute('''
            INSERT INTO incidents 
            (incident_time, incident_number, incident_location, nature, incident_ori)
            VALUES (?, ?, ?, ?, ?)
        ''', incident)  # Pass the tuple directly

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



def status(db):
    # Connect to the database
    conn = sqlite3.connect(db)
    
    # Create a cursor object
    cursor = conn.cursor()

    # Execute a query to get the nature and count of each incident
    cursor.execute('''
        SELECT nature, COUNT(*) as count 
        FROM incidents 
        GROUP BY nature 
        ORDER BY count DESC, nature
    ''')

    # Fetch all rows and print the status
    rows = cursor.fetchall()

    for row in rows:
        print(f"{row[0]}|{row[1]}")

    # Close the connection
    conn.close()

