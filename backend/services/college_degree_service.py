# # backend/services/college_degree_service.py

# class CollegeDegreeService:
#     def __init__(self, cosmos_db):
#         self.cosmos_db = cosmos_db

#     def get_all_degrees(self):
#         print("get_all_degrees method called.")  # Print statement to confirm the method is called
#         data, status_code = self.cosmos_db.get_data('colleges_degrees')
#         print("Data retrieved from the database:", data)  # Print the data retrieved to confirm DB interaction
        
#         if status_code == 200:
#             return data  # Return just the Flask Response object
        
#         # If there's an error, you may want to handle it differently
#         return data, status_code




# backend/services/college_degree_service.py

import json

class CollegeDegreeService:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def get_all_degrees(self):
        """
        Load all college degrees from the JSON file.
        """
        try:
            with open(self.json_file_path, 'r') as file:
                degrees = json.load(file)
            return degrees, 200  # Return the degrees and a 200 OK status
        except Exception as e:
            return {"error": str(e)}, 500  # Return an error message and a 500 status if something goes wrong
