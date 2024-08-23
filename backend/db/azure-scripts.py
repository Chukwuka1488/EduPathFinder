# backend/db/azure-scripts.py 

import os
import logging
from azure.identity import AzureCliCredential
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from the .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AzureCosmosManager:
    def __init__(self):
        """
        Initialize the AzureCosmosManager with environment variables and Azure credentials.
        """
        self.subscription_id = os.getenv("SUBSCRIPTION_ID")
        self.resource_group_name = os.getenv("RESOURCE_GROUP_NAME")
        self.keyvault_name = os.getenv("keyvault_name")
        self.account_name = os.getenv("cosmosdb_account_name")
        
        if not all([self.subscription_id, self.resource_group_name, self.keyvault_name, self.account_name]):
            logging.error("One or more required environment variables are missing.")
            raise ValueError("Missing required environment variables.")
        
        self.credential = AzureCliCredential()
        self.kv_client = KeyVaultManagementClient(self.credential, self.subscription_id)
        self.cosmos_client = CosmosDBManagementClient(self.credential, self.subscription_id)
        
        self.keyvault_endpoint = self.get_keyvault_endpoint()
        self.primary_connection_string = self.get_cosmos_connection_string()

    def get_keyvault_endpoint(self):
        """
        Retrieve the Key Vault endpoint URI.

        :return: Key Vault endpoint URI.
        """
        try:
            vault = self.kv_client.vaults.get(self.resource_group_name, self.keyvault_name)
            logging.info(f"Retrieved Key Vault endpoint: {vault.properties.vault_uri}")
            return vault.properties.vault_uri
        except Exception as e:
            logging.error(f"Failed to retrieve Key Vault endpoint: {e}")
            raise

    def get_cosmos_connection_string(self):
        """
        Retrieve the primary MongoDB connection string from Cosmos DB.

        :return: The primary MongoDB connection string.
        """
        try:
            connection_strings = self.cosmos_client.database_accounts.list_connection_strings(self.resource_group_name, self.account_name)
            primary_connection_string = connection_strings.connection_strings[0].connection_string
            logging.info("Successfully retrieved Cosmos DB connection string.")
            return primary_connection_string
        except Exception as e:
            logging.error(f"Failed to retrieve Cosmos DB connection string: {e}")
            raise

    def set_secret_in_keyvault(self, secret_name="cosmosconnectionstring"):
        """
        Set or update a secret in Azure Key Vault.

        :param secret_name: The name of the secret in the Key Vault.
        """
        try:
            secret_client = SecretClient(vault_url=self.keyvault_endpoint, credential=self.credential)
            secret_client.set_secret(secret_name, self.primary_connection_string)
            logging.info(f"Secret '{secret_name}' has been set in Key Vault '{self.keyvault_endpoint}'.")
        except Exception as e:
            logging.error(f"Failed to set secret in Key Vault: {e}")
            raise

    def list_cosmos_db_accounts(self):
        """
        List all Cosmos DB accounts in the subscription.
        """
        try:
            logging.info("Listing all Cosmos DB accounts in the subscription:")
            accounts = self.cosmos_client.database_accounts.list()
            for account in accounts:
                logging.info(f"Cosmos DB Account Name: {account.name}")
        except Exception as e:
            logging.error(f"Failed to list Cosmos DB accounts: {e}")
            raise

    def connect_to_cosmos_db(self):
        """
        Connect to Cosmos DB using the primary MongoDB connection string.

        :return: A MongoClient instance connected to Cosmos DB.
        """
        try:
            client = MongoClient(self.primary_connection_string)
            logging.info("Successfully connected to Cosmos DB.")
            return client
        except Exception as e:
            logging.error(f"Failed to connect to Cosmos DB: {e}")
            raise

    def list_databases_and_collections(self, client):
        """
        List all databases and collections in Cosmos DB.

        :param client: A MongoClient instance connected to Cosmos DB.
        """
        try:
            logging.info("Listing all databases and collections:")
            databases = client.list_database_names()
            for db_name in databases:
                db = client[db_name]
                logging.info(f"Database: {db_name}")
                collections = db.list_collection_names()
                for collection_name in collections:
                    logging.info(f" - Collection: {collection_name}")
        except Exception as e:
            logging.error(f"Failed to list databases and collections: {e}")
            raise

    def delete_database_and_collections(self, client, db_name, collections_to_delete=None):
        """
        Delete a specified database and its collections from Cosmos DB.

        :param client: A MongoClient instance connected to Cosmos DB.
        :param db_name: The name of the database to delete.
        :param collections_to_delete: A list of collection names to delete.
        """
        try:
            databases = client.list_database_names()
            
            if db_name in databases:
                db = client[db_name]
                if collections_to_delete:
                    for collection_to_delete in collections_to_delete:
                        if collection_to_delete in db.list_collection_names():
                            db.drop_collection(collection_to_delete)
                            logging.info(f"Deleted collection '{collection_to_delete}' from database '{db_name}'.")
                        else:
                            logging.warning(f"Collection '{collection_to_delete}' not found in database '{db_name}'.")
                else:
                    client.drop_database(db_name)
                    logging.info(f"Deleted entire database '{db_name}'.")
            else:
                logging.warning(f"Database '{db_name}' not found.")
        except Exception as e:
            logging.error(f"Failed to delete database or collections: {e}")
            raise

def main():
    try:
        # Initialize the AzureCosmosManager
        azure_manager = AzureCosmosManager()

        # Set the Cosmos DB connection string in Azure Key Vault
        azure_manager.set_secret_in_keyvault()

        # List all Cosmos DB accounts in the subscription
        azure_manager.list_cosmos_db_accounts()

        # Connect to Cosmos DB
        client = azure_manager.connect_to_cosmos_db()

        # List all databases and collections
        azure_manager.list_databases_and_collections(client)

        # Delete specified collections or entire database
        collections_to_delete = [
            "bachelor_business_analytics_courses",
            "bachelor_accountancy_courses",
            "bachelor_social_work_courses",
            "bachelor_civil_engineering_courses",
            "colleges_degrees"
        ]
        azure_manager.delete_database_and_collections(client, db_name="edupathfinder-cosmosdb-account", collections_to_delete=collections_to_delete)

    except Exception as e:
        logging.error(f"An error occurred in the main process: {e}")

if __name__ == "__main__":
    main()
