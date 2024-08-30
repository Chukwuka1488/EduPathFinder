import copy  # For making deep copies of the course schema
from course_types import COURSE_TYPES  # Import COURSE_TYPES


def generate_swagger_spec():
    base_spec = {
        "swagger": "2.0",
        "info": {
            "title": "EduPathFinder API",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http"],
        "paths": {}
    }

    # Define the schema for colleges_degrees
    colleges_degrees_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "course": {
                    "type": "string"
                },
                "degree": {
                    "type": "string"
                },
                "college": {
                    "type": "string"
                }
            }
        }
    }

    # Define the schema for course types
    course_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "important": {
                    "type": "string"
                },
                "hours": {
                    "type": "integer"
                },
                "course_number": {
                    "type": "string"
                },
                "title": {
                    "type": "string"
                },
                "min_grade": {
                    "type": "string"
                },
                "gec": {
                    "type": "string"
                },
                "prerequisite": {
                    "type": "string"
                },
                "additional_notes": {
                    "type": "string"
                }
            }
        }
    }

    # Add the static colleges_degrees path
    base_spec["paths"]["/api/colleges-degrees"] = {
        "get": {
            "summary": "Get all college degrees",
            "responses": {
                "200": {
                    "description": "A list of college degrees",
                    "schema": colleges_degrees_schema
                }
            }
        }
    }

    # Dynamically add course types
    for course in COURSE_TYPES:
        # Convert underscores to hyphens in the path
        level = course["level"].replace("_", "-")
        course_type = course["course_type"].replace("_", "-")
        path = f"/api/{level}-{course_type}-courses"

        # Create a deep copy of the course schema for each path
        course_schema_copy = copy.deepcopy(course_schema)

        # Add the dynamic path
        base_spec["paths"][path] = {
            "get": {
                "summary": f"Get all {course_type.replace('-', ' ')} courses",
                "responses": {
                    "200": {
                        "description": f"A list of {course_type.replace('-', ' ')} courses",
                        "schema": course_schema_copy
                    }
                }
            }
        }

        # Print statement for debugging which APIs are being generated
        print(f"Generated Swagger API for: {path}")

    return base_spec
