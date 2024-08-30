import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_json_files(data_folder, input_file):
    """
    Generate JSON files from a source JSON file by replacing hyphens with underscores in courseType.

    Args:
    data_folder (str): The directory where the input JSON file is located and where the output JSON files will be saved.
    input_file (str): The path to the JSON file containing the course data.

    Returns:
    None
    """
    try:
        # Load data from colleges-degrees.json
        with open(input_file, 'r') as file:
            courses = json.load(file)
        logging.info(f"Successfully loaded data from {input_file}.")
    except FileNotFoundError:
        logging.error(f"Input file '{input_file}' not found.")
        return
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the file '{input_file}'.")
        return

    # Process each course and save as JSON
    for course in courses:
        try:
            # Replace hyphens with underscores in courseType
            collection_name = course["courseType"].replace("-", "_")
            
            # Create JSON filename based on collection_name
            filename = f"{collection_name}.json"
            filepath = os.path.join(data_folder, filename)
            
            # Check if the file already exists
            if os.path.exists(filepath):
                logging.info(f"File '{filename}' already exists. Skipping...")
                continue
            
            # Write course data to JSON file
            with open(filepath, 'w') as json_file:
                json.dump(course, json_file, indent=4)
            
            logging.info(f"Created {filename} in {data_folder}.")
        
        except Exception as e:
            logging.error(f"An error occurred while processing '{course['courseType']}': {str(e)}")

if __name__ == "__main__":
    # Define the path to the JSON file and the output directory
    data_folder = 'data'
    input_file = os.path.join(data_folder, 'colleges_degrees.json')

    # Generate JSON files
    generate_json_files(data_folder, input_file)
