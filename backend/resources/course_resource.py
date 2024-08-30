# backend/resources/course_resource.py

from flask_restful import Resource
from flasgger import swag_from
from services.course_service import CourseService

class CourseResource(Resource):
    def __init__(self, cosmos_db, level, course_type):
        self.service = CourseService(cosmos_db, level, course_type)

    @swag_from({
        'responses': {
            200: {
                'description': 'A list of courses',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'important': {'type': 'string'},
                                    'hours': {'type': 'integer'},
                                    'course_number': {'type': 'string'},
                                    'title': {'type': 'string'},
                                    'min_grade': {'type': 'string'},
                                    'gec': {'type': 'string'},
                                    'prerequisite': {'type': 'string'},
                                    'additional_notes': {'type': 'string'},
                                    'department': {'type': 'string'},
                                    'program': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        }
    })
    def get(self):
        """
        Get all courses
        """
        return self.service.get_all_courses()
