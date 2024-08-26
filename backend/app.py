# backend/app.py

import logging
from flask import Flask, send_from_directory, jsonify, request
from flask_restful import Api
from flasgger import Swagger
from flask_cors import CORS
from config.config import Config
from db.cosmos_mongo_db import CosmosDB
from resources.course_resource import CourseResource
from resources.college_degree_resource import CollegeDegrees  # Import CollegeDegrees
from course_types import COURSE_TYPES  # Import COURSE_TYPES from course_types.py
from swagger_config import generate_swagger_spec  # Import the Swagger config generator
import os
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG,  # Set the logging level to DEBUG
                    format='%(asctime)s %(levelname)s: %(message)s',  # Set log format
                    datefmt='%Y-%m-%d %H:%M:%S')  # Set date and time format

def print_available_routes(app):
    """Print all available routes in the application."""
    print("\nAvailable Routes:")
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            print(f"{rule} -> {rule.endpoint}")
            time.sleep(5)

def create_app():
    # Initialize Flask application
    app = Flask(__name__, static_folder='../frontend', static_url_path='/')
    CORS(app)  # Enable CORS for cross-origin requests

    # Configuring Swagger for API documentation
    app.config.from_object(Config)
    swagger = Swagger(app, template=generate_swagger_spec())  # Use the dynamic Swagger generation

    # Initialize CosmosDB using Key Vault for secure credential management
    cosmos_db = CosmosDB.from_key_vault()

    # Initialize API and resources with the `cosmos_db` instance
    api = Api(app)
    
    # Register the CollegeDegrees resource
    api.add_resource(CollegeDegrees, '/api/colleges-degrees', resource_class_args=[cosmos_db])

    # Dynamically add routes for courses
    for course in COURSE_TYPES:
        level = course["level"]
        course_type = course["course_type"]
        endpoint = f"/api/{level}-{course_type.replace('_', '-')}-courses"

        # Unique endpoint name with underscores
        endpoint_name = f"{level}_{course_type}_courses"

        api.add_resource(
            CourseResource,
            endpoint,
            resource_class_args=(cosmos_db, level, course_type),
            endpoint=endpoint_name  # Use underscores for the endpoint name
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
    register_routes(app, cosmos_db)

    return app


def register_routes(app, cosmos_db):
    # API routes
    @app.route('/api/create-collection', methods=['POST'])
    def create_collection():
        data = request.get_json()
        collection_name = data.get("collection_name")
        return cosmos_db.create_collection(collection_name)

    @app.route('/api/list-collections', methods=['GET'])
    def list_collections():
        return cosmos_db.list_collections()

    @app.route('/api/add-data/<collection_name>', methods=['POST'])
    def add_data(collection_name):
        data = request.get_json()
        return cosmos_db.add_data(collection_name, data)

    @app.route('/api/get-data/<collection_name>', methods=['GET'])
    def get_data(collection_name):
        return cosmos_db.get_data(collection_name)

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

            update_result = cosmos_db.update_course(collection_name, course_title, field, value)

            if update_result.get('updated'):
                logging.info(f"Update successful for course title {course_title} in field {field} with new value {value}")
                return jsonify({"message": "Update successful"}), 200
            else:
                logging.warning(f"Update failed or not needed for course title {course_title}")
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
