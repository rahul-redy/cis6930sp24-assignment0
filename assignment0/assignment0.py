
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



def extractincidents(incident_data):
    # Convert the bytes object to a file-like object
    pdf_file = io.BytesIO(incident_data)

    # Create a PDF reader object
    pdf_reader = PdfReader(pdf_file)

    # Initialize an empty list to store extracted incidents
    incidents_list = []

    # Iterate through each page of the PDF
    for page_num in range(len(pdf_reader.pages)):
        # Get the text content of the current page
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()

        # Use regular expressions to extract relevant information
        pattern = re.compile(r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}) (\d{4}-\d+) (\S+ \S+ \S+) ([^\n]+) (\S+)')

        # Search for patterns in the page text
        matches = pattern.findall(page_text)

        # Process matches and skip empty rows
        for match in matches:
            if match[0] and match[1] and match[2] and match[3] and match[4]:
                incident = {
                    'Date/Time': match[0],
                    'Incident Number': match[1],
                    'Location': match[2],
                    'Nature': match[3],
                    'Incident ORI': match[4]
                }
                incidents_list.append(incident)

    return incidents_list



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
      # Add this line
    # Create a cursor object
    cursor = conn.cursor()

    # Iterate over incidents and insert into the database
    for incident in incidents:
        cursor.execute('''
            INSERT INTO incidents 
            (incident_time, incident_number, incident_location, nature, incident_ori)
            VALUES (?, ?, ?, ?, ?)
        ''', (incident['Date/Time'], incident['Incident Number'], incident['Location'], incident['Nature'], incident['Incident ORI']))

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
  # Add similar lines for relevant queries
    print("Debug: Rows -", rows)
    for row in rows:
        print(f"{row[0]}|{row[1]}")

    # Close the connection
    conn.close()

