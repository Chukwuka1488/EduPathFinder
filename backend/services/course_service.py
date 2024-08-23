# backend/services/course_service.py

class CourseService:
    def __init__(self, cosmos_db, level, course_type):
        self.cosmos_db = cosmos_db
        self.level = level
        self.course_type = course_type

    def get_all_courses(self):
        """
        Fetch all courses from the collection without filtering.
        """
        collection_name = f"{self.level}_{self.course_type}_courses"
        data, status_code = self.cosmos_db.get_data(collection_name)
        if status_code == 200:
            return data  # Return just the Flask Response object
        
        # Handle any potential errors
        return {'error': data}, status_code
