#### Edu Path Finder

##### For Devs:

To merge your `dev-courses-grid` branch into your `master` branch, you can follow these steps:

1. First, check out to the `master` branch:

```bash
git checkout master
```

```bash
git pull
```

2. Then, merge the `dev-courses-grid` branch into `master`:

```bash
git merge dev-courses-grid
```

3. If there are any merge conflicts, you'll need to resolve them. Once you've resolved any conflicts, you can commit the changes:

```bash
git commit -m "Resolved merge conflicts"
```

4. Finally, push the changes to the remote repository:

```bash
git push origin master
```

Please replace `origin` with the name of your remote if it's different. Also, make sure to pull the latest changes from the remote `master` branch before merging.

Remember, it's a good practice to ensure your code is working as expected after resolving merge conflicts before you push the changes. Let me know if you need help with anything else! 😊

##### USING SOLID PRINCIPLES

Certainly! Splitting the app into modules and following SOLID principles can make the code more maintainable, testable, and extensible. Let's split the app into several modules and explain where and how each SOLID principle is applied.

### Directory Structure

```
backend/
│
├── data/
│   ├── colleges_degrees.json
│   └── bachelor_social_work_courses.json
│
├── services/
│   ├── __init__.py
│   ├── college_degree_service.py
│   └── social_work_course_service.py
│
├── resources/
│   ├── __init__.py
│   ├── college_degree_resource.py
│   └── social_work_course_resource.py
│
├── config/
│   ├── __init__.py
│   └── config.py
│
├── app.py
├── populate_db.py
└── requirements.txt
```

### SOLID Principles Applied

#### Single Responsibility Principle (SRP)

Each class or module should have one responsibility. This principle is applied by splitting services and resources into separate modules.

#### Open/Closed Principle (OCP)

Classes should be open for extension but closed for modification. We achieve this by defining clear interfaces and extending functionalities without modifying existing code.

#### Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types. Here, we ensure that any derived class can replace its base class without altering the desirable properties of the program.

#### Interface Segregation Principle (ISP)

No client should be forced to depend on methods it does not use. We segregate interfaces so that classes only need to know about the methods that are relevant to them.

#### Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules. Both should depend on abstractions. We use dependency injection where needed.

### Explanation of SOLID Principles

1. **Single Responsibility Principle (SRP)**:

   - Each module/class has one responsibility.
   - `CollegeDegreeService` and `SocialWorkCourseService` are responsible for managing their respective data.
   - `CollegeDegrees` and `SocialWorkCourses` are responsible for handling API requests.

2. **Open/Closed Principle (OCP)**:

   - Services and resources are open for extension but closed for modification.
   - New functionalities can be added by extending these classes without modifying existing code.

3. **Liskov Substitution Principle (LSP)**:

   - Any subclass or service can replace its base class or service without affecting the functionality.
   - For example, if we had a base `Service` class, any specific service like `CollegeDegreeService` should be replaceable without changing the application behavior.

4. **Interface Segregation Principle (ISP)**:

   - Clients (resources) should not be forced to depend on interfaces they do not use.
   - Resources only depend on the methods provided by their respective services.

5. **Dependency Inversion Principle (DIP)**:
   - High-level modules (resources) depend on abstractions (services), not on low-level modules (data access methods).
   - This is achieved by injecting services into resources.

#### Terraform

```
TF_VAR_subscription_id="your-azure-subscription-id"
TF_VAR_resource_group_name="student-success"
TF_VAR_location="US Central"
TF_VAR_cosmosdb_account_name="edupathfinder-cosmosdb-account"
TF_VAR_failover_location="East US 2"
TF_VAR_enable_multi_region_writes="false"
```

echo ".env" >> .gitignore

##### Tests

backend/
├── app.py
├── config/
├── db/
├── requirements.txt
├── resources/
├── services/
├── static/
├── tests/
│ ├── test_cosmos_db.py # Your test file
└── ...

python -m unittest discover -s tests -p "test\_\*.py"

### ENV VARIABLES

You can retrieve the necessary information for your `.env` file using the Azure CLI (`az`). Here’s how you can get each piece of information:

### 1. **KEYVAULT_NAME**:

- This is the name of your Azure Key Vault. If you already know the name, you can set it directly. If not, you can list your Key Vaults:

```bash
az keyvault list --query "[].{Name:name}" --output tsv
```

- This will list all Key Vaults in your subscription. Choose the appropriate one for your application.

### 2. **COSMOSDB_ACCOUNT_NAME**:

- This is the name of your Cosmos DB account. You can find it using the following command:

```bash
az cosmosdb list --query "[].{Name:name}" --output tsv
```

- This will list all Cosmos DB accounts in your subscription.

### 3. **AZURE_CLIENT_ID**:

- The client ID corresponds to the application (service principal) that you’ve registered in Azure AD to use with your application. To retrieve the client ID:

```bash
az ad sp list --display-name <your-service-principal-name> --query "[].appId" --output tsv
```

- Replace `<your-service-principal-name>` with the display name of your service principal. This will return the client ID (App ID) for the specified service principal.

### 4. **AZURE_TENANT_ID**:

- The tenant ID is the directory ID of your Azure Active Directory. To get the tenant ID:

```bash
az account show --query tenantId --output tsv
```

- This will return the tenant ID for your current subscription context.

### 5. **AZURE_CLIENT_SECRET**:

- The client secret is a credential you create for your service principal to authenticate with Azure. To create and retrieve the client secret:

```bash
az ad sp credential reset --name <your-service-principal-name> --query "password" --output tsv
```

- Replace `<your-service-principal-name>` with the name or ID of your service principal. This command will generate a new client secret and return it. **Be sure to store this securely** because it will not be shown again.

### Example of Populating the `.env` File:

After running these commands, you’ll have the necessary values to populate your `.env` file:

```plaintext
# .env
KEYVAULT_NAME=your-keyvault-name
COSMOSDB_ACCOUNT_NAME=your-cosmosdb-account-name
AZURE_CLIENT_ID=your-azure-client-id
AZURE_TENANT_ID=your-azure-tenant-id
AZURE_CLIENT_SECRET=your-azure-client-secret
```

### Summary:

- Use the Azure CLI to retrieve the required information.
- Populate the `.env` file with these values.
- Ensure you store the `.env` file securely and avoid committing it to version control.

This setup ensures your application can authenticate and access necessary Azure resources during local development.

#### NB: If you can find your service principal, create one

When you create a new Service Principal using the Azure CLI, the command itself will provide you with the `appId`, which is your `AZURE_CLIENT_ID`. Here's a quick guide on how to retrieve it:

### 1. **Creating the Service Principal**:

If you haven't done so already, create the Service Principal using the following command:

```bash
az ad sp create-for-rbac --name my-app-sp
```

After running this command, Azure will return a JSON object that includes the `appId`, `tenant`, and `password`:

Example Output:

```plaintext
{
  "appId": "your-azure-client-id",
  "displayName": "my-app-sp",
  "name": "http://my-app-sp",
  "password": "your-azure-client-secret",
  "tenant": "your-azure-tenant-id"
}
```

- **`appId`**: This is your `AZURE_CLIENT_ID`.
- **`password`**: This is your `AZURE_CLIENT_SECRET`.
- **`tenant`**: This is your `AZURE_TENANT_ID`.

### 2. **Retrieving the `AZURE_CLIENT_ID` Again**:

If you need to retrieve the `appId` (Azure Client ID) again after creating the Service Principal, you can run the following command:

```bash
az ad sp show --id http://my-app-sp --query appId --output tsv
```

- This command queries the Azure Active Directory for the Service Principal named `my-app-sp` and returns the `appId`.

### 3. **Environment Variables for `.env` File**:

With the information provided, you can populate your `.env` file:

```plaintext
# .env
KEYVAULT_NAME=your-keyvault-name
COSMOSDB_ACCOUNT_NAME=your-cosmosdb-account-name
AZURE_CLIENT_ID=your-azure-client-id
AZURE_TENANT_ID=your-azure-tenant-id
AZURE_CLIENT_SECRET=your-azure-client-secret
```

### Summary:

- **`appId`** is your `AZURE_CLIENT_ID`.
- **`password`** is your `AZURE_CLIENT_SECRET`.
- **`tenant`** is your `AZURE_TENANT_ID`.

After creating the Service Principal, make sure to securely store the `password` as it won't be retrievable again. If you lose it, you'll need to reset the credentials using the Azure CLI.

az keyvault set-policy --name <your-keyvault-name> \
 --spn <your-service-principal-app-id> \
 --secret-permissions get list

az role assignment create --role "Key Vault Secrets User" \
 --assignee "780ae873-58dc-4894-9920-dbc6b9eea679" \
 --scope "/subscriptions/ed0d9dbe-2f4a-4f14-94df-452c45994c1e/resourceGroups/student-success/providers/Microsoft.KeyVault/vaults/cosmos-mongo-db"
