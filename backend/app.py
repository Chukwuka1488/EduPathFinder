# # backend/app.py

# import logging
# from flask import Flask, send_from_directory, jsonify, request
# from flask_restful import Api
# from flasgger import Swagger
# from flask_cors import CORS
# from config.config import Config
# from db.cosmos_mongo_db import CosmosDB
# from resources.course_resource import CourseResource
# from resources.college_degree_resource import CollegeDegrees  # Import CollegeDegrees
# from course_types import COURSE_TYPES  # Import COURSE_TYPES from course_types.py
# from swagger_config import generate_swagger_spec  # Import the Swagger config generator
# import os


# # Configure logging
# logging.basicConfig(level=logging.DEBUG,  # Set the logging level to DEBUG
#                     format='%(asctime)s %(levelname)s: %(message)s',  # Set log format
#                     datefmt='%Y-%m-%d %H:%M:%S')  # Set date and time format
# import json

# def load_json(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)

# def save_json(file_path, data):
#     with open(file_path, 'w') as file:
#         json.dump(data, file, indent=4)


# def create_app():
#     # Initialize Flask application
#     app = Flask(__name__, static_folder='../frontend', static_url_path='/')
#     CORS(app)  # Enable CORS for cross-origin requests

#     # Configuring Swagger for API documentation
#     app.config.from_object(Config)
#     swagger = Swagger(app, template=generate_swagger_spec())  # Use the dynamic Swagger generation

#     # Initialize CosmosDB using Key Vault for secure credential management
#     cosmos_db = CosmosDB.from_key_vault()

#     # Initialize API and resources with the `cosmos_db` instance
#     api = Api(app)
    
#     # Register the CollegeDegrees resource
#     api.add_resource(CollegeDegrees, '/api/colleges-degrees', resource_class_args=[cosmos_db])

#     # Dynamically add routes for courses
#     for course in COURSE_TYPES:
#         level = course["level"]
#         course_type = course["course_type"]
#         endpoint = f"/api/{level}-{course_type.replace('_', '-')}-courses"

#         # Unique endpoint name with underscores
#         endpoint_name = f"{level}_{course_type}_courses"

#         api.add_resource(
#             CourseResource,
#             endpoint,
#             resource_class_args=(cosmos_db, level, course_type),
#             endpoint=endpoint_name  # Use underscores for the endpoint name
#         )
#         logging.debug(f"Added resource: {endpoint} with endpoint name {endpoint_name}")

#     # Prevent caching by setting headers
#     @app.after_request
#     def add_cache_control_headers(response):
#         response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#         response.headers['Pragma'] = 'no-cache'
#         response.headers['Expires'] = '0'
#         return response

#     # Register additional routes
#     register_routes(app, cosmos_db)

#     return app


# def register_routes(app, cosmos_db):
#     # API routes
#     @app.route('/api/create-collection', methods=['POST'])
#     def create_collection():
#         data = request.get_json()
#         collection_name = data.get("collection_name")
#         return cosmos_db.create_collection(collection_name)

#     @app.route('/api/list-collections', methods=['GET'])
#     def list_collections():
#         return cosmos_db.list_collections()

#     @app.route('/api/add-data/<collection_name>', methods=['POST'])
#     def add_data(collection_name):
#         data = request.get_json()
#         return cosmos_db.add_data(collection_name, data)

#     @app.route('/api/get-data/<collection_name>', methods=['GET'])
#     def get_data(collection_name):
#         return cosmos_db.get_data(collection_name)

#     # New route to handle course updates
#     @app.route('/api/update-course', methods=['PUT'])
#     def update_course():
#         logging.debug("Received request to update course")

#         try:
#             data = request.get_json()
#             logging.debug(f"Request data: {data}")

#             collection_name = data.get('collectionName')
#             course_title = data.get('courseTitle')  # Using course title
#             field = data.get('field')
#             value = data.get('value')

#             logging.debug(f"Collection: {collection_name}, Course Title: {course_title}, Field: {field}, Value: {value}")

#             update_result = cosmos_db.update_course(collection_name, course_title, field, value)

#             if update_result.get('updated'):
#                 logging.info(f"Update successful for course title {course_title} in field {field} with new value {value}")
#                 return jsonify({"message": "Update successful"}), 200
#             else:
#                 logging.warning(f"Update failed or not needed for course title {course_title}")
#                 return jsonify({"error": "Update failed"}), 500

#         except Exception as e:
#             logging.error(f"Exception occurred while processing the update request: {e}")
#             return jsonify({"error": "Internal Server Error"}), 500


#     # Serve the index.html file for all non-API routes (SPA support)
#     @app.route('/', defaults={'path': ''})
#     @app.route('/<path:path>')
#     def serve_static(path):
#         if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
#             return send_from_directory(app.static_folder, path)
#         else:
#             return send_from_directory(app.static_folder, 'index.html')

#     # Health check route to confirm that the service is running
#     @app.route('/health', methods=['GET'])
#     def health_check():
#         return jsonify({"status": "healthy"}), 200

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True, host='0.0.0.0', port=5001)


import logging
from flask import Flask, send_from_directory, jsonify, request
from flask_restful import Api
from flasgger import Swagger
from flask_cors import CORS
from config.config import Config
from resources.course_resource import CourseResource
from resources.college_degree_resource import CollegeDegrees  # Import CollegeDegrees
from course_types import COURSE_TYPES  # Import COURSE_TYPES from course_types.py
from swagger_config import generate_swagger_spec  # Import the Swagger config generator
import os
import json


# Configure logging
logging.basicConfig(level=logging.DEBUG,  # Set the logging level to DEBUG
                    format='%(asctime)s %(levelname)s: %(message)s',  # Set log format
                    datefmt='%Y-%m-%d %H:%M:%S')  # Set date and time format

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def create_app():
    # Initialize Flask application
    app = Flask(__name__, static_folder='../frontend', static_url_path='/')
    CORS(app)  # Enable CORS for cross-origin requests

    # Configuring Swagger for API documentation
    app.config.from_object(Config)
    swagger = Swagger(app, template=generate_swagger_spec())  # Use the dynamic Swagger generation

    # Initialize API
    api = Api(app)
    
    # Path to the local JSON file for college degrees
    colleges_degrees_file = os.path.join(app.root_path, 'data/colleges_degrees.json')
    
    # Register the CollegeDegrees resource with the path to the JSON file
    api.add_resource(CollegeDegrees, '/api/colleges-degrees', resource_class_args=[colleges_degrees_file])

    # Dynamically add routes for courses
    for course in COURSE_TYPES:
        level = course["level"]
        course_type = course["course_type"]
        endpoint = f"/api/{level}-{course_type.replace('_', '-')}-courses"

        # Unique endpoint name with underscores
        endpoint_name = f"{level}_{course_type}_courses"

        course_file = os.path.join(app.root_path, f'data/{endpoint_name}.json')
        
        api.add_resource(
            CourseResource,
            endpoint,
            resource_class_args=(course_file,),  # Pass the file path instead of a database instance
            endpoint=endpoint_name
        )
        logging.debug(f"Added resource: {endpoint} with endpoint name {endpoint_name}")

    # Prevent caching by setting headers
    @app.after_request
    def add_cache_control_headers(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    # Register additional routes
    register_routes(app)

    return app


def register_routes(app):
    # API routes
    @app.route('/api/create-collection', methods=['POST'])
    def create_collection():
        data = request.get_json()
        collection_name = data.get("collection_name")
        # Assuming this is not necessary in the local JSON scenario, you can remove or replace this functionality
        return jsonify({"message": "Collections are handled manually in this setup"}), 200

    @app.route('/api/list-collections', methods=['GET'])
    def list_collections():
        # List available collections (i.e., JSON files) in the data directory
        collections = [f for f in os.listdir('data') if f.endswith('.json')]
        return jsonify(collections), 200

    @app.route('/api/add-data/<collection_name>', methods=['POST'])
    def add_data(collection_name):
        data = request.get_json()
        file_path = os.path.join('data', f'{collection_name}.json')
        existing_data = load_json(file_path)
        existing_data.append(data)
        save_json(file_path, existing_data)
        return jsonify({"message": "Data added successfully"}), 200

    @app.route('/api/get-data/<collection_name>', methods=['GET'])
    def get_data(collection_name):
        file_path = os.path.join('data', f'{collection_name}.json')
        data = load_json(file_path)
        return jsonify(data), 200

    # New route to handle course updates
    @app.route('/api/update-course', methods=['PUT'])
    def update_course():
        logging.debug("Received request to update course")

        try:
            data = request.get_json()
            logging.debug(f"Request data: {data}")

            collection_name = data.get('collectionName')
            course_title = data.get('courseTitle')  # Using course title
            field = data.get('field')
            value = data.get('value')

            logging.debug(f"Collection: {collection_name}, Course Title: {course_title}, Field: {field}, Value: {value}")

            file_path = os.path.join('data', f'{collection_name}.json')
            courses = load_json(file_path)

            for course in courses:
                if course['courseTitle'] == course_title:
                    course[field] = value
                    save_json(file_path, courses)
                    logging.info(f"Update successful for course title {course_title} in field {field} with new value {value}")
                    return jsonify({"message": "Update successful"}), 200
            
            logging.warning(f"Course with title {course_title} not found")
            return jsonify({"error": "Update failed"}), 500

        except Exception as e:
            logging.error(f"Exception occurred while processing the update request: {e}")
            return jsonify({"error": "Internal Server Error"}), 500


    # Serve the index.html file for all non-API routes (SPA support)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_static(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # Health check route to confirm that the service is running
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
