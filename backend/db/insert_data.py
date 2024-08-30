# backend/db/insert.py 
import os
import logging
import time
import json
from dotenv import load_dotenv
from cosmos_mongo_db import CosmosDB

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file):
    """
    Load configuration from a JSON file.
    
    :param config_file: Path to the configuration JSON file.
    :return: List of data files configuration.
    """
    try:
        with open(config_file, 'r') as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        logging.error(f"Configuration file '{config_file}' not found.")
        return []
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the configuration file '{config_file}'.")
        return []

def insert_json_data(cosmos_mongo_db, collection_name, json_file_path, bulk_insert=False, batch_size=100):
    """
    Insert JSON data into the specified CosmosDB collection. If bulk_insert is True, the data will be inserted in batches.
    Existing documents are skipped based on the 'course' field for 'colleges_degrees' and other criteria for other collections.

    :param cosmos_mongo_db: Instance of the CosmosDB class
    :param collection_name: Name of the collection in the database
    :param json_file_path: Path to the JSON file containing data to insert
    :param bulk_insert: Boolean indicating whether to use bulk insert or not
    :param batch_size: Number of documents per batch in case of bulk insert
    """
    try:
        # Step 1: Check if the collection already exists to skip unnecessary creation attempts
        if cosmos_mongo_db.collection_exists(collection_name):
            logging.info(f"Collection '{collection_name}' already exists. Skipping creation.")
        else:
            response, status_code = cosmos_mongo_db.create_collection(collection_name)
            if status_code not in [200, 201]:
                logging.error(f"Error creating collection {collection_name}: {response.get('error', 'Unknown error')}")
                return

            logging.info(f"Collection creation response: {response}")

        # Step 2: Load the JSON data
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Step 3: Insert the data in batches or as a whole
        if bulk_insert:
            process_batches(cosmos_mongo_db, collection_name, data, batch_size)
        else:
            process_single_documents(cosmos_mongo_db, collection_name, data)

        logging.info(f"Successfully processed data into {collection_name}.")

    except Exception as e:
        logging.exception(f"An error occurred while inserting data into {collection_name}: {str(e)}")

def process_batches(cosmos_mongo_db, collection_name, data, batch_size):
    """
    Process and insert data in batches.

    :param cosmos_mongo_db: Instance of the CosmosDB class
    :param collection_name: Name of the collection in the database
    :param data: The data to be inserted
    :param batch_size: Number of documents per batch
    """
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]

        for document in batch:
            query = {"course": document["course"]} if collection_name == "colleges_degrees" else document
            existing_document = cosmos_mongo_db.find_document(collection_name, query)

            if existing_document:
                logging.info(f"Document with course '{document['course']}' already exists in {collection_name}. Skipping...")
            else:
                cosmos_mongo_db.add_single_data(collection_name, document)
                logging.info(f"Inserted new document into {collection_name}: {document}")

        logging.info(f"Batch {i//batch_size + 1}: Processed {len(batch)} documents in {collection_name}.")

        # Pause for 10 seconds to reduce load on the database
        logging.info("Pausing for 10 seconds to reduce load on the database...")
        time.sleep(10)

def process_single_documents(cosmos_mongo_db, collection_name, data):
    """
    Process and insert each document individually without splitting.
    Adds 'totalSemesterHours' to each semester, 'totalDegreeHours' and 'advancedMinimumCreditHours' 
    at the document level, summing the hours of all courses within each semester and 
    calculating advanced hours for courses starting with '3' or '4' across all years.

    :param cosmos_mongo_db: Instance of the CosmosDB class
    :param collection_name: Name of the collection in the database
    :param data: The data to be inserted
    """
    for document in data:
        # Initialize total degree hours counter and advanced credit hours
        total_degree_hours = 0
        advanced_minimum_credit_hours = 0  # Initialize at document level

        # Calculate the total semester hours for each semester and advanced minimum credit hours
        if "years" in document:  # Ensure the data structure includes 'years'
            for year in document["years"]:
                year_total_hours = 0  # Initialize total hours for the year

                for semester in year["semesters"]:
                    total_hours = sum(course["hours"] for course in semester["courses"])
                    semester["totalSemesterHours"] = total_hours  # Add the total hours to the semester data
                    year_total_hours += total_hours  # Accumulate yearly total

                    # Calculate advanced minimum credit hours across all semesters
                    for course in semester["courses"]:
                        course_number = course["courseNumber"].strip()
                        # Check if course number has sufficient length and starts with '3' or '4'
                        if len(course_number) >= 6 and course_number[5] in ['3', '4']:
                            advanced_minimum_credit_hours += course["hours"]

                # year["totalYearHours"] = year_total_hours
                total_degree_hours += year_total_hours

            # Set advanced credit hours and total degree hours for the document
            document["totalDegreeHours"] = total_degree_hours
            document["advancedMinimumCreditHours"] = advanced_minimum_credit_hours
            document["approved"] = "Approved: "
            document["revised"] = "Revised: Tuesday, August 20th, 2024"
            document["aboveYearOne"] = "Important Notice: Register in the Business Foundation Courses listed below in thier posted sequence or sooner! Business Foundation courses are listed in BOLD and an * next to thier name."
            document["belowYearTwo"] = "Students must be admitted into RCVCoBE to be able to register for the Advanced Business Courses as shown on the next page. ** Apply to be admitted into RCVCoBE at https://www.utrgv.edu/cobe/undergrauate/apply-for-admission **"
            document["aboveYearThree"] = "Students must be admitted into RCVCoBE to be able to register for the Advanced Business Courses as shown on this page. For questions contact the RCVCoBE Coordinators at: business.advising@utrgv.edu"
            document["aboveYearFour"] = "Students needs to review all pending course prerequisites for thier major using the Roadmap and Degree Works. Students will need to request approval for MGMT 4389 three weeks before registration begins by emailing business.advising@utrgv.edu"
            
        query = {"course": document["course"]} if collection_name == "colleges_degrees" else document
        existing_document = cosmos_mongo_db.find_document(collection_name, query)

        if existing_document:
            logging.info(f"Document with course '{document['course']}' already exists in {collection_name}. Skipping...")
        else:
            cosmos_mongo_db.add_single_data(collection_name, document)
            logging.info(f"Inserted new document into {collection_name}: {document}")

        # Pause for 10 seconds to reduce load on the database
        logging.info("Pausing for 10 seconds to reduce load on the database...")
        time.sleep(10)

def main():
    """
    Main entry point for the script. Initializes CosmosDB connection and inserts data from JSON files.
    """
    try:
        # Initialize the CosmosDB class using the connection string from Key Vault
        cosmos_mongo_db = CosmosDB.from_key_vault()

       # Load the data files configuration from JSON
        config_file = "config/data_files_config.json"
        data_files = load_config(config_file)

        # Insert data for each collection
        for data_file in data_files:
            collection_name = data_file.get("collection_name")
            json_file_path = data_file.get("json_file_path")
            bulk_insert = data_file.get("bulk_insert", False)

            if not os.path.exists(json_file_path):
                logging.warning(f"JSON file {json_file_path} does not exist. Skipping...")
                continue

            insert_json_data(cosmos_mongo_db, collection_name, json_file_path, bulk_insert)


    except Exception as e:
        logging.exception(f"An error occurred in the main process: {str(e)}")

if __name__ == "__main__":
    main()
