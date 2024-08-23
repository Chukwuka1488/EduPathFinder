# backend/resources/college_degree_resource.py

from flask_restful import Resource
from flasgger import swag_from
from services.college_degree_service import CollegeDegreeService

class CollegeDegrees(Resource):
    def __init__(self, cosmos_db):
        self.service = CollegeDegreeService(cosmos_db)

    @swag_from({
        'responses': {
            200: {
                'description': 'A list of college degrees',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'course': {
                                        'type': 'string'
                                    },
                                    'degree': {
                                        'type': 'string'
                                    },
                                    'college': {
                                        'type': 'string'
                                    }
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
        Get all college degrees
        """
        return self.service.get_all_degrees()
