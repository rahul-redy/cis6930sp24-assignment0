
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



import io
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

def extractincidents(incident_data):
    incidents = []
    max_columns = 0  # Track the maximum number of columns found on a page
    try:
        # Convert bytes data to a BytesIO object for PdfReader
        pdf_file = io.BytesIO(incident_data)
        for page_layout in extract_pages(pdf_file):
            column_texts = {}  # Dictionary to hold column data
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    x, y = int(element.x0), int(element.y0)  # Get the x-coordinate of the text element
                    text = element.get_text()
                    column = x // 100  # Group by every 100 pixels on the x-axis
                    if column in column_texts:
                        column_texts[column].append((y, text))  # Append text along with its y-coordinate
                    else:
                        column_texts[column] = [(y, text)]

            # Update the maximum number of columns found on a page
            max_columns = max(max_columns, len(column_texts))

            # Sort texts in each column by y-coordinate (top to bottom)
            for column, texts in column_texts.items():
                column_texts[column] = sorted(texts, key=lambda x: -x[0])

            # Extract data assuming a variable number of columns
            for i in range(len(column_texts[0])):  # Use the maximum number of columns found
                incident_data = [""] * max_columns  # Initialize with empty strings for all columns
                for column in range(max_columns):  # Iterate through all columns
                    if column in column_texts:
                        try:
                            text = column_texts[column][i][1].strip()  # Get the text for each column

                            # Handle cases for mapping data to columns
                            if column == 3:
                                if text == "Location" or not text:  # Handle "Location" or empty in nature column
                                    incident_data[2] = text  # Map to location or empty
                                else:
                                    incident_data[3] = text  # Map to nature column
                            elif column == 4:
                                if not text:  # Handle empty incident_ori
                                    incident_data[4] = "Empty"  # Or provide a default value
                                else:
                                    incident_data[4] = text  # Map to incident_ori column
                            else:
                                incident_data[column] = text  # Map to other columns
                        except IndexError:
                            pass  # Handle cases where a column might have fewer entries

                # Swap the data in nature and incident_ori columns
                incident_data[3], incident_data[4] = incident_data[4], incident_data[3]

                incidents.append(incident_data[:5])  # Append only the first five columns to match the database schema

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



import sqlite3

def populatedb(db, incidents):
    # Connect to the database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Iterate over incidents and insert into the database
    for incident in incidents:
        # Ensure that incident is a tuple with exactly five elements
        if len(incident) == 5:
            cursor.execute('''
                INSERT INTO incidents 
                (incident_time, incident_number, incident_location, nature, incident_ori)
                VALUES (?, ?, ?, ?, ?)
            ''', incident)  # Pass the tuple directly
        else:
            print(f"Skipping invalid incident: {incident}")

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

