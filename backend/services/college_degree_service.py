# backend/services/college_degree_service.py

class CollegeDegreeService:
    def __init__(self, cosmos_db):
        self.cosmos_db = cosmos_db

    def get_all_degrees(self):
        print("get_all_degrees method called.")  # Print statement to confirm the method is called
        data, status_code = self.cosmos_db.get_data('colleges_degrees')
        print("Data retrieved from the database:", data)  # Print the data retrieved to confirm DB interaction
        
        if status_code == 200:
            return data  # Return just the Flask Response object
        
        # If there's an error, you may want to handle it differently
        return data, status_code



