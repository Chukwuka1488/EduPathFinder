The issue seems to be with the flow of the response object and how it's being handled in your service layer. Let me explain the flow and point out where the problem might be.

### Flow Breakdown:

1. **API Request**: 
   - The request starts in `app.py` with the endpoint `/api/colleges-degrees`.
   - This endpoint is handled by the `CollegeDegrees` resource class in `college_degree_resource.py`.

2. **Resource Class**:
   - The `CollegeDegrees` resource calls the `get_all_degrees()` method of `CollegeDegreeService`.

3. **Service Class**:
   - In `get_all_degrees()`, the service class calls the `get_data()` method on the `CosmosDB` instance.

4. **Database Interaction**:
   - The `get_data()` method in `CosmosDB` fetches the data, converts the `_id` fields from `ObjectId` to `string`, and then wraps the data in a `jsonify()` call, which returns a Flask `Response` object.

5. **Service Layer Handling**:
   - The `CollegeDegreeService.get_all_degrees()` method returns the Flask `Response` object and a status code directly.

6. **Resource Layer Handling**:
   - The `get()` method of `CollegeDegrees` returns the same `Response` object.

### Problem Identification:

The `get_all_degrees()` method is returning a tuple `(Response, status_code)`. The `Response` object already contains the status code, so it doesn't make sense to return it separately. Flask expects either a Flask `Response` object or a tuple of `(data, status_code)` where `data` is not a `Response` object but raw data that Flask will wrap into a `Response` object. By returning both, it confuses Flask, leading to the error.

### Solution:

You should not return `status_code` separately when you are already returning a `Response` object.

### Updated `get_all_degrees()` Method:

```python
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
```

### Updated `CosmosDB.get_data()` Method:

Make sure the `CosmosDB.get_data()` method correctly handles the data and the response, and returns a `Response` object only.

```python
class CosmosDB:
    # ... (other methods)

    def get_data(self, collection_name):
        try:
            collection = self.database[collection_name]
            data = list(collection.find())
            for item in data:
                if '_id' in item:
                    item['_id'] = str(item['_id'])
            return jsonify(data), 200  # Return the JSON response directly
        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Make sure to jsonify the error as well
```

### Conclusion:

- The `CollegeDegreeService.get_all_degrees()` method should only return the `Response` object created by `jsonify` from `CosmosDB.get_data()`.
- Ensure that `CosmosDB.get_data()` only returns `Response` objects that Flask can directly send as HTTP responses.
- With these changes, your endpoint should no longer raise the `TypeError: Object of type Response is not JSON serializable` error.