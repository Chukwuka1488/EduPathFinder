# backend/db/cosmos_mongo_db.py 

import os
import json
import logging
import time
from flask import jsonify
from pymongo import MongoClient, errors as pymongo_errors
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class CosmosDB:
    def __init__(self, connection_string, db_name):
        """
        Initialize a connection to the CosmosDB using MongoDB API.
        This method attempts to connect to the specified database using the provided connection string.

        :param connection_string: The connection string for MongoDB.
        :param db_name: The name of the database to connect to.
        """
        try:
            # Establish MongoDB client with a timeout to avoid hanging
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=20000)
            self.database = self.client[db_name]
            
            # Test the connection immediately to ensure validity
            self.client.admin.command('ping')
            logging.info(f"Successfully connected to database: {db_name}")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise

    @staticmethod
    def from_key_vault():
        """
        Factory method to create a CosmosDB instance by retrieving the connection string from Azure Key Vault.

        :return: Instance of CosmosDB connected to the specified database.
        """
        try:
            # Retrieve necessary configuration from environment variables
            keyvault_name = os.getenv('keyvault_name')
            secret_name = "cosmosconnectionstring"  # This is the name of the secret storing the connection string
            db_name = os.getenv('cosmosdb_account_name')

            if not keyvault_name or not secret_name or not db_name:
                raise ValueError("Missing required environment variables")

            # Construct the Key Vault endpoint and authenticate
            keyvault_endpoint = f"https://{keyvault_name}.vault.azure.net/"
            credential = DefaultAzureCredential()
            secret_client = SecretClient(vault_url=keyvault_endpoint, credential=credential)

            # Retrieve the connection string from Key Vault
            connection_string = secret_client.get_secret(secret_name).value

            # Return an initialized CosmosDB instance
            return CosmosDB(connection_string=connection_string, db_name=db_name)
        except Exception as e:
            logging.error(f"Failed to initialize CosmosDB from Key Vault: {e}")
            raise
        
    def collection_exists(self, collection_name):
        """
        Check if a collection exists in the database.

        :param collection_name: The name of the collection to check.
        :return: True if the collection exists, False otherwise.
        """
        try:
            return collection_name in self.database.list_collection_names()
        except pymongo_errors.PyMongoError as e:
            logging.error(f"Failed to check if collection exists: {e}")
            return False


    def create_collection(self, collection_name):
        """
        Create a collection in the database if it does not already exist.

        :param collection_name: The name of the collection to create.
        :return: A tuple containing a status message and HTTP status code.
        """
        try:
            if collection_name not in self.database.list_collection_names():
                self.database.create_collection(collection_name)
                logging.info(f"Collection created: {collection_name}")
                return {"status": "Collection created", "collection_name": collection_name}, 201
            else:
                logging.info(f"Collection already exists: {collection_name}")
                return {"status": "Collection already exists", "collection_name": collection_name}, 200
        except Exception as e:
            logging.error(f"Failed to create collection: {e}")
            return {"error": str(e)}, 400

    def add_data_from_json(self, collection_name, json_file_path):
        """
        Insert multiple documents from a JSON file into a specified collection.
        This method is optimized with retry logic to handle transient errors.

        :param collection_name: The name of the collection to insert data into.
        :param json_file_path: The path to the JSON file containing the documents.
        :return: A tuple containing a status message and HTTP status code.
        """
        try:
            # Load data from JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            # Ensure the JSON contains a non-empty list of documents
            if not isinstance(data, list) or not data:
                raise ValueError("The JSON file must contain a non-empty list of documents")

            collection = self.database[collection_name]
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    # Attempt to insert documents in bulk
                    result = collection.insert_many(data)
                    logging.info(f"Successfully added data to {collection_name}. Inserted IDs: {result.inserted_ids}")
                    return {"status": "Data added", "inserted_ids": result.inserted_ids}, 201
                except pymongo_errors.BulkWriteError as bwe:
                    first_error = bwe.details['writeErrors'][0]
                    if first_error['code'] == 16500:  # Handle TooManyRequests error with retry
                        logging.warning(f"TooManyRequests error, retrying... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise
                except pymongo_errors.PyMongoError as e:
                    logging.error(f"PyMongoError encountered: {e}")
                    raise
            # Handle failure after all retries
            if 'bwe' in locals():
                return {"error": "Failed after retries", "details": bwe.details}, 400
            else:
                return {"error": "Failed after retries"}, 400

        except Exception as e:
            logging.error(f"Failed to add data from JSON: {e}")
            return {"error": str(e)}, 400

    def add_single_data(self, collection_name, document):
        """
        Insert a single document into a specified collection.

        :param collection_name: The name of the collection to insert data into.
        :param document: The document to insert.
        :return: A tuple containing a status message and HTTP status code.
        """
        try:
            collection = self.database[collection_name]
            result = collection.insert_one(document)
            logging.info(f"Successfully added a document to {collection_name}. Inserted ID: {result.inserted_id}")
            return {"status": "Data added", "inserted_id": str(result.inserted_id)}, 201
        except pymongo_errors.PyMongoError as e:
            logging.error(f"Failed to add document: {e}")
            return {"error": str(e)}, 400

    def find_document(self, collection_name, query):
        """
        Find a single document in a collection based on a query.

        :param collection_name: The name of the collection to search in.
        :param query: The query to find the document.
        :return: The found document or None if not found.
        """
        try:
            collection = self.database[collection_name]
            document = collection.find_one(query)
            if document:
                logging.info(f"Document found in {collection_name} with query {query}")
            else:
                logging.info(f"No document found in {collection_name} with query {query}")
            return document
        except pymongo_errors.PyMongoError as e:
            logging.error(f"Failed to find document: {e}")
            return None

    def get_data(self, collection_name):
        """
        Retrieve all documents from a specified collection.

        :param collection_name: The name of the collection to retrieve data from.
        :return: A tuple containing the data and HTTP status code.
        """
        try:
            collection = self.database[collection_name]
            data = list(collection.find())
            for item in data:
                if '_id' in item:
                    item['_id'] = str(item['_id'])  # Convert ObjectId to string for JSON serialization
            logging.info(f"Successfully retrieved data from {collection_name}")
            return jsonify(data), 200
        except Exception as e:
            logging.error(f"Failed to retrieve data: {e}")
            return {"error": str(e)}, 500

    def list_collections(self):
        """
        List all collections in the database.

        :return: A tuple containing the list of collections and HTTP status code.
        """
        try:
            collections = self.database.list_collection_names()
            logging.info("Successfully listed collections")
            return {"collections": collections}, 200
        except Exception as e:
            logging.error(f"Failed to list collections: {e}")
            return {"error": str(e)}, 400

    def update_course(self, collection_name, course_title, field, value):
        """
        Update a specific field in a course document identified by the course title within a nested structure.

        :param collection_name: The name of the collection containing the course.
        :param course_title: The course title identifying the document to update.
        :param field: The field to update within the course document.
        :param value: The new value to set for the field.
        :return: A dictionary containing the update status.
        """
        try:
            collection = self.database[collection_name]

            # Find the document containing the course
            document = collection.find_one({"years.semesters.courses.title": course_title})
            if not document:
                logging.warning(f"Course with title {course_title} not found in {collection_name}")
                return {"error": "Course not found"}, 404

            # Traverse the document to find and update the course
            updated = False
            for year in document['years']:
                for semester in year['semesters']:
                    for course in semester['courses']:
                        if course['title'] == course_title:
                            course[field] = value  # Update the specific field
                            updated = True
                            break
                    if updated:
                        break
                if updated:
                    break

            if updated:
                # Perform the update in the database
                result = collection.replace_one({"_id": document["_id"]}, document)
                if result.modified_count > 0:
                    logging.info(f"Successfully updated course {course_title} in {collection_name}")
                    return {"status": "success", "updated": True}
                else:
                    logging.warning(f"No modification made for course {course_title} in {collection_name}")
                    return {"status": "not modified"}, 200
            else:
                logging.warning(f"Course with title {course_title} was not found in {collection_name}")
                return {"error": "Course not found"}, 404

        except Exception as e:
            logging.error(f"Failed to update course: {e}")
            return {"error": str(e)}, 500
