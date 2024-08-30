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
    "colleges_degrees",
    "bachelor_accountancy_courses",
    "bachelor_business_analytics_courses",
    "bachelor_early_care_early_childhood_studies_courses",
    "bachelor_early_care_early_childhood_studies_teacher_certification_courses",
    "bachelor_economics_courses",
    "bachelor_economics_finance_double_major_courses",
    "bachelor_economics_minor_courses",
    "bachelor_entrepreneurship_innovation_courses",
    "bachelor_finance_courses",
    "bachelor_global_supply_chain_management_courses",
    "bachelor_information_systems_courses",
    "bachelor_international_business_courses",
    "bachelor_management_courses",
    "bachelor_marketing_courses",
    "bachelor_social_work_courses",
    "bachelor_education_bilingual_education_ec_sixth_certification_courses",
    "bachelor_education_english_as_a_second_language_ec_sixth_certification_courses",
    "bachelor_education_special_education_courses",
    "bachelor_hospitality_tourism_management_event_and_destination_management_courses",
    "bachelor_hospitality_tourism_management_lodging_asset_ownership_and_management_courses",
    "bachelor_hospitality_tourism_management_restaurant_entrepreneurship_and_management_courses",
    "bachelor_nursing_courses",
    "bachelor_nursing_rn_to_bsn_courses",
    "bachelor_nursing_second_degree_courses",
    "bachelor_civil_engineering_courses",
    "bachelor_computer_engineering_courses",
    "bachelor_computer_science_courses",
    "bachelor_cyber_security_courses",
    "bachelor_electrical_engineering_courses",
    "bachelor_mechanical_engineering_courses",
    "bachelor_manufacturing_engineering_courses",
    "bachelor_engineering_technology_courses",
    "bachelor_applied_statistics_data_science_courses",
    "bachelor_biology_courses",
    "bachelor_biology_seventh_twelfth_teacher_certification_courses",
    "bachelor_chemistry_courses",
    "bachelor_chemistry_seventh_twelfth_teacher_certification_courses",
    "bachelor_environmental_science_earth_and_ocean_sciences_courses",
    "bachelor_environmental_science_environment_and_society_courses",
    "bachelor_environmental_science_environmental_biology_courses",
    "bachelor_environmental_science_environmental_chemistry_courses",
    "bachelor_environmental_science_interdisciplinary_environmental_science_courses",
    "bachelor_interdisciplinary_studies_middle_school_mathematics_fourth_eight_teacher_certification_courses",
    "bachelor_interdisciplinary_studies_science_fourth_eight_teacher_certification_courses",
    "bachelor_marine_biology_courses",
    "bachelor_mathematics_fourth_eight_teacher_certification_courses",
    "bachelor_mathematics_seventh_twelfth_teacher_certification_courses",
    "bachelor_mathematics_applied_mathematics_courses",
    "bachelor_mathematics_economics_courses",
    "bachelor_mathematics_pure_math_courses",
    "bachelor_mathematics_science_and_engineering_courses",
    "bachelor_mathematics_statistics_courses",
    "bachelor_physics_biophysics_courses",
    "bachelor_physics_minor_required_courses",
    "bachelor_physics_pure_and_applied_physics_courses",
    "bachelor_physics_teacher_certification_courses",
    "bachelor_sustainable_agriculture_food_systems_courses",
    "bachelor_addiction_studies_courses",
    "bachelor_american_sign_language_interpretation_communication_studies_courses",
    "bachelor_american_sign_language_interpretation_spanish_translation_and_interpreting_courses",
    "bachelor_biomedical_science_courses",
    "bachelor_communication_sciences_audiology_american_sign_language_courses",
    "bachelor_communication_sciences_speech_language_pathology_american_sign_language_courses",
    "bachelor_exercise_science_occupational_therapy_courses",
    "bachelor_exercise_science_physical_therapy_course",
    "bachelor_exercise_science_course",
    "bachelor_health_courses",
    "bachelor_health_services_technology_courses",
    "bachelor_integrated_health_science_clinical_professions_courses",
    "bachelor_integrated_health_science_health_services_courses",
    "bachelor_integrated_health_science_professional_studies_courses",
    "bachelor_kinesiology_athletic_training_courses",
    "bachelor_kinesiology_coaching_course",
    "bachelor_kinesiology_recreational_sports_management_courses",
    "bachelor_kinesiology_courses",
    "bachelor_kinesiology_teacher_certification_courses",
    "bachelor_medical_laboratory_science_courses",
    "bachelor_nutritional_sciences_nutrition_courses",
    "bachelor_nutritional_sciences_food_and_technology_management_courses",
    "bachelor_nutritional_sciences_nutrition_and_fitness_courses",
    "bachelor_rehabilitation_services_deaf_and_hard_of_hearing_courses",
    "bachelor_rehabilitation_services_courses",
    "bachelor_art_all_level_secondary_education_minor_courses",
    "bachelor_art_ceramics_courses",
    "bachelor_art_sculpture_courses",
    "bachelor_art_studio_art_courses",
    "bachelor_art_teacher_certification_courses",
    "bachelor_fine_art_dance_mexican_dance_courses",
    "bachelor_art_dance_teacher_certification_courses",
    "bachelor_art_dance_courses",
    "bachelor_fine_art_dance_courses",
    "bachelor_music_guitar_teacher_certification_courses",
    "bachelor_music_mariachi_teacher_certification_courses",
    "bachelor_music_piano_teacher_certification_courses",
    "bachelor_music_string_teacher_certification_courses",
    "bachelor_music_voice_teacher_certification_courses",
    "bachelor_music_woodwinds_brass_percussion_teacher_certification_courses",
    "bachelor_music_music_composition_courses",
    "bachelor_music_music_technology_courses",
    "bachelor_performance_guitar_courses",
    "bachelor_performance_piano_courses",
    "bachelor_performance_string_courses",
    "bachelor_performance_voice_courses",
    "bachelor_performance_woodwinds_brass_percussion_courses",
    "bachelor_theatre_design_technical_courses",
    "bachelor_theatre_film_production_courses",
    "bachelor_theatre_performance_courses",
    "bachelor_theatre_teacher_certification_courses",
    "bachelor_visual_communication_design_courses",
    "bachelor_anthropology_archaeology_courses",
    "bachelor_anthropology_global_health_and_migration_courses",
    "bachelor_anthropology_courses",
    "bachelor_criminal_justice_courses",
    "bachelor_communication_studies_courses",
    "bachelor_english_rhetoric_composition_literacy_studies_courses",
    "bachelor_english_language_arts_courses",
    "bachelor_english_creative_writing_course",
    "bachelor_english_teacher_certification_seventh_twelfth_courses",
    "bachelor_history_courses",
    "bachelor_history_teacher_certification_courses",
    "bachelor_human_dimensions_organizations_courses"
]

        azure_manager.delete_database_and_collections(client, db_name="edupathfinder-cosmosdb-account", collections_to_delete=collections_to_delete)

    except Exception as e:
        logging.error(f"An error occurred in the main process: {e}")

if __name__ == "__main__":
    main()
