The error you're seeing indicates that your Azure Active Directory (AAD) tenant requires multi-factor authentication (MFA) for the operation you're attempting, and it's requesting you to authenticate interactively.

### Steps to Resolve the MFA Requirement

To proceed, follow these steps:

1. **Re-authenticate with Azure CLI Using Interactive Login**:
   You need to log in interactively to satisfy the MFA requirement.

   ```bash
   az login --scope https://graph.microsoft.com//.default
   ```

   - This command opens a web page where you can sign in and complete the MFA process.

2. **Retrieve the Object ID After Authentication**:
   After successfully logging in with MFA, you can try retrieving the `objectId` again:

   ```bash
   az ad user show --id chukwuka.akibor01@utrgv.edu
   ```

   This command should now work and provide the details of your user, including the `objectId`.

3. **Proceed with Role Assignment**:
   Once you have the `objectId`, you can use it in your role assignment command as previously described.

### Summary of Commands

- **Log in with MFA**:
  ```bash
  az login --scope https://graph.microsoft.com//.default
  ```

- **Get Object ID**:
  ```bash
  az ad user show --id chukwuka.akibor01@utrgv.edu
  ```

After logging in with MFA, your Azure CLI session should have the necessary permissions to execute further commands, including retrieving the `objectId` and assigning roles.

To find the `principal-id` or `object-id` of the identity you are using with Azure CLI, you can use the following commands:

### 1. **If You Are Using Your User Account (Azure CLI Login Identity)**

If you're logged in with your personal or organizational account, you can get your `object-id` using:

```bash
az ad user show --id <your-email-address>
```

Replace `<your-email-address>` with your email address. This command will return details about your Azure Active Directory (AD) user account, including the `objectId`.

### 2. **If You Are Using a Service Principal**

If you're using a service principal (typically used in CI/CD pipelines), you can find the `object-id` with:

```bash
az ad sp show --id <your-service-principal-id>
```

Replace `<your-service-principal-id>` with your service principal's app ID (client ID).

### 3. **To Get the Object ID of the Currently Logged-In User**

If you're logged in and want to get the object ID of the currently active account, you can use:

```bash
az ad signed-in-user show --query objectId -o tsv
```

### 4. **Listing All Service Principals**

If you're not sure about the service principal ID, you can list all service principals in your Azure AD tenant and find the relevant one:

```bash
az ad sp list --query "[].{DisplayName:displayName, AppId:appId, ObjectId:objectId}" -o table
```

### Example Outputs

- **For a User Account**:
  ```bash
  az ad user show --id your.email@example.com
  ```
  This will output JSON with your user's details, including `"objectId": "your-object-id"`.

- **For a Service Principal**:
  ```bash
  az ad sp show --id <your-service-principal-id>
  ```
  This will show the service principal details, including `"objectId": "your-object-id"`.

- **Get the Object ID of the Currently Logged-In User**:
  ```bash
  az ad signed-in-user show --query objectId -o tsv
  ```
  This returns just the `objectId` of the logged-in user.

### Using the Object ID

Once you have the `objectId`, you can use it in role assignment commands:

```bash
az role assignment create --role "Key Vault Secrets Officer" --assignee <your-object-id> --scope /subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.KeyVault/vaults/<your-key-vault-name>
```

Replace `<your-object-id>` with the object ID you retrieved from the previous commands.

The error message `Forbidden: Caller is not authorized to perform action on resource` indicates that the Azure CLI identity you are using does not have the necessary permissions to perform the action of setting a secret in the Azure Key Vault.

### Steps to Resolve the Issue

1. **Verify Azure CLI Login**: Ensure that you're logged in with the correct Azure CLI account that has the appropriate permissions.

   ```bash
   az login
   ```

   Verify your account and subscription:

   ```bash
   az account show
   ```

2. **Assign the Required Roles**: You need to assign the appropriate roles to the Azure CLI identity so it can manage secrets in the Key Vault.

   - The identity needs the **Key Vault Secrets Officer** role or the **Key Vault Contributor** role on the specific Key Vault.

   To assign the role, use the following command:

   ```bash
   az role assignment create --role "Key Vault Secrets Officer" --assignee <your-principal-id-or-object-id> --scope /subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.KeyVault/vaults/<your-key-vault-name>
   ```

   Replace:
   - `<your-principal-id-or-object-id>`: with the Object ID of the Azure CLI identity.
   - `<your-subscription-id>`: with your Azure subscription ID.
   - `<your-resource-group>`: with your resource group name.
   - `<your-key-vault-name>`: with your Key Vault name.

3. **Check Role Assignment Propagation**: Role assignments can take a few minutes to propagate. If you recently assigned a role, wait a few minutes and try running your script again.

4. **Verify Role Assignments**: You can verify the role assignments to ensure they have been applied correctly:

   ```bash
   az role assignment list --assignee <your-principal-id-or-object-id> --scope /subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.KeyVault/vaults/<your-key-vault-name>
   ```

   This command lists the roles assigned to your identity for the specific Key Vault.

5. **Retry the Operation**: After ensuring that the roles are correctly assigned and the permissions have propagated, try running your script again.

### Example Commands

Here's an example of assigning the `Key Vault Secrets Officer` role to a user or service principal:

```bash
az role assignment create \
    --role "Key Vault Secrets Officer" \
    --assignee <your-principal-id-or-object-id> \
    --scope /subscriptions/e<your-subscription-id>/resourceGroups/student-success/providers/Microsoft.KeyVault/vaults/cosmos-mongo-db
```

### Explanation

- **`Key Vault Secrets Officer` Role**: This role allows the assigned identity to manage secrets within the Key Vault but does not allow management of certificates or keys.
- **`Key Vault Contributor` Role**: Provides broader permissions, including managing keys, secrets, and certificates within the Key Vault.

By assigning the correct role, your script should be able to set secrets in the Azure Key Vault without encountering the `Forbidden` error.

To access `SecretClient` and `DefaultAzureCredential` from the `azure-keyvault-secrets` and `azure-identity` libraries, you need to follow these steps:

### Step 1: Install Required Azure SDK Libraries

First, you need to install the Azure SDK libraries that include `azure-keyvault-secrets` and `azure-identity`. These libraries will allow you to interact with Azure Key Vault and handle authentication securely.

You can install them using `pip`:

```bash
pip install azure-identity azure-keyvault-secrets
```

### Step 2: Set Up Azure Key Vault and Access Permissions

To securely retrieve secrets from Azure Key Vault, you need to configure a few things on Azure:

1. **Create an Azure Key Vault**:
   - Go to the [Azure portal](https://portal.azure.com/).
   - Navigate to **Key Vaults** and create a new Key Vault if you don’t have one already.

2. **Add Secrets to Azure Key Vault**:
   - Once your Key Vault is created, add a new secret (e.g., your Cosmos DB connection string).

3. **Set Up Access Permissions**:
   - Ensure that your Azure Active Directory (AAD) user or service principal has the appropriate access policies to read secrets from the Key Vault.
   - In the Azure portal, go to your Key Vault and under **Access Policies**, ensure that the user/service principal has at least the `Get` permission for secrets.

### Step 3: Use `DefaultAzureCredential` to Authenticate

`DefaultAzureCredential` automatically attempts to authenticate using a series of credential providers. It works seamlessly in many Azure-hosted environments like Azure Virtual Machines, App Services, and Kubernetes. If you're developing locally, it will use your Azure CLI or Visual Studio Code login.

Here’s how you can use `DefaultAzureCredential` to authenticate and access a secret from Key Vault:

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Set up the Key Vault URL (replace with your actual Key Vault URL)
KEYVAULT_ENDPOINT = "https://<your-keyvault-name>.vault.azure.net/"

# Authenticate using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create a SecretClient to interact with Key Vault
secret_client = SecretClient(vault_url=KEYVAULT_ENDPOINT, credential=credential)

# Retrieve a secret (replace 'your-secret-name' with the actual name of the secret)
secret_name = "your-secret-name"
retrieved_secret = secret_client.get_secret(secret_name)

# Use the secret value
print("Retrieved secret value:", retrieved_secret.value)
```

### Step 4: Ensure Your Environment is Configured for Authentication

`DefaultAzureCredential` tries various methods to authenticate depending on where your code is running:

- **Local Development**: If you are running locally, ensure you are logged in via the Azure CLI:
  
  ```bash
  az login
  ```

- **Azure Hosted Environment**: If your code is running in an Azure environment (like Azure App Service or Azure Virtual Machine), `DefaultAzureCredential` will automatically use the managed identity assigned to that environment.

### Testing the Setup

Once you've set everything up, run your application. The code should authenticate using `DefaultAzureCredential` and retrieve the secret from your Azure Key Vault.

### Troubleshooting

- **Access Denied**: If you encounter permission issues, double-check the access policies in the Azure Key Vault and ensure that the identity you're using has the necessary permissions.
- **Authentication Failure**: Ensure that the Azure CLI is logged in with the correct account if you're developing locally.

By following these steps, you should be able to securely access your secrets stored in Azure Key Vault using `SecretClient` and `DefaultAzureCredential`.

To integrate the Azure Key Vault access into your `cosmos_mongo_db.py` file and `app.py` file, you'll follow these steps:

### 1. **Integrate with `cosmos_mongo_db.py`**

First, we'll update your `cosmos_mongo_db.py` to use Azure Key Vault to securely retrieve the Cosmos DB connection string.

```python
# backend/db/cosmos_mongo_db.py

from pymongo import MongoClient, errors
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class CosmosDB:
    def __init__(self, connection_string, db_name):
        # Initialize MongoDB client with the provided connection string
        self.client = MongoClient(connection_string)
        self.database = self.client[db_name]
        ...
```

### 2. **Integrate with `app.py`**

Now, we'll update `app.py` to initialize the `CosmosDB` class using the `from_key_vault` method, so that the connection string is retrieved securely from Azure Key Vault.

```python
# backend/app.py

from flask import Flask, send_from_directory, jsonify, request
from flask_restful import Api
from flasgger import Swagger
from flask_cors import CORS
from config.config import Config
from db.cosmos_mongo_db import CosmosDB
from resources.college_degree_resource import CollegeDegrees
from resources.social_work_course_resource import SocialWorkCourses

def create_app():
    # Initialize Flask application
    app = Flask(__name__, static_folder='../frontend', static_url_path='/')
    CORS(app)  # Enable CORS for cross-origin requests

    # Configuring Swagger
    app.config.from_object(Config)
    swagger = Swagger(app, template_file='./static/swagger.json')

    # Initialize CosmosDB using Key Vault for secure credential management
    cosmos_db = CosmosDB.from_key_vault(
        keyvault_endpoint="https://<your-keyvault-name>.vault.azure.net/",
        secret_name="cosmosconnectionstring",
        db_name="YOUR_COSMOS_DB_NAME"
    )
    ...
```

### Explanation of Changes

1. **Azure Key Vault Integration in `CosmosDB`**:
   - The `CosmosDB` class now includes a `from_key_vault` method that handles retrieving the connection string from Azure Key Vault.
   - `DefaultAzureCredential` is used to handle authentication with Azure Key Vault. This method supports various authentication methods, including Managed Identity when running in Azure.

2. **App Initialization**:
   - In `create_app()`, the `CosmosDB` class is initialized with the `from_key_vault` method, which securely retrieves the connection string from Azure Key Vault.

3. **Configuration of Routes**:
   - The `register_routes` function connects the CosmosDB instance to various Flask routes, allowing CRUD operations on the database.

### Running the Application

To run your application:

1. **Install Required Libraries**:
   Ensure you have the required Azure libraries installed:

   ```bash
   pip install azure-identity azure-keyvault-secrets pymongo
   ```

2. **Set Up Azure Key Vault**:
   - Store your Cosmos DB connection string as a secret in Azure Key Vault.
   - Make sure your environment (local or cloud) can authenticate with Azure Key Vault using `DefaultAzureCredential`.

3. **Run the Flask Application**:
   Start your Flask application as usual:

   ```bash
   python app.py
   ```

This setup ensures that your Cosmos DB credentials are securely managed and not exposed in your code, following best practices for secure application development.