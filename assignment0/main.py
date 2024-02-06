import argparse
from assignment0 import fetchincidents, extractincidents, createdb, populatedb, status

def main():
    parser = argparse.ArgumentParser(description="Process incident data from a given URL.")
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL.")
    args = parser.parse_args()

    # Download data
    incident_data = fetchincidents(args.incidents)

    # Extract data
    incidents = extractincidents(incident_data)

    # Create new database
    db = createdb()

    # Insert data
    if db is not None:  # Check if db is not None before proceeding
        # Insert data
        populatedb(db, incidents)

        # Print incident counts
        status(db)
    else:
        print("Error creating the database. Check the createdb function.")

if __name__ == '__main__':
    main()
