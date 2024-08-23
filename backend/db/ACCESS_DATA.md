If someone else wants to run your application locally after pulling the containers from Docker Hub, they will need to provide their own Azure credentials, or you will need to securely share the necessary credentials with them. Here’s how they can proceed:

### 1. **Create Their Own Azure Service Principal (Recommended Approach)**

- They can create their own Azure Service Principal (a set of credentials for authentication with Azure) using the Azure CLI.

```bash
az ad sp create-for-rbac --name <app-name> --role contributor --scopes /subscriptions/<subscription-id>
```

This command will return a JSON object with `client_id`, `client_secret`, `tenant_id`, and other details. They will use these details in their `.env` file.

### 2. **Update the `.env` File with Their Credentials**

They need to update their `.env` file with the credentials they generated:

```bash
KEYVAULT_NAME="cosmos-mongo-db"  # This remains the same if you're sharing the same Key Vault
COSMOSDB_ACCOUNT_NAME="edupathfinder-cosmosdb-account"  # This also remains the same
AZURE_CLIENT_ID="<Their-Azure-Client-ID>"
AZURE_TENANT_ID="<Their-Azure-Tenant-ID>"
AZURE_CLIENT_SECRET="<Their-Azure-Client-Secret>"
```

### 3. **Access Rights to the Azure Key Vault**

The error message you're encountering indicates that the Azure Key Vault is using Azure Role-Based Access Control (RBAC) for managing access permissions, rather than the traditional access policy model.

When Azure Key Vault is configured with RBAC, you don't use the `az keyvault set-policy` command to manage permissions. Instead, you assign roles directly using Azure RBAC.

Here’s how you can proceed:

### 1. **Assign Access Using Azure RBAC**

To grant access to a user or service principal to retrieve secrets from Azure Key Vault, you need to assign the appropriate role using Azure RBAC. The role you typically need is `Key Vault Secrets User`.

You can assign this role using the following command:

```bash
az role assignment create --role "Key Vault Secrets User" --assignee <TheirAzureClientId> --scope /subscriptions/<SubscriptionId>/resourceGroups/<ResourceGroupName>/providers/Microsoft.KeyVault/vaults/<YourKeyVaultName>
```

Replace the placeholders with the appropriate values:

- `<TheirAzureClientId>`: The client ID of the user's service principal.
- `<SubscriptionId>`: The Azure subscription ID where the Key Vault resides.
- `<ResourceGroupName>`: The resource group name where the Key Vault is located.
- `<YourKeyVaultName>`: The name of your Key Vault (in this case, `cosmos-mongo-db`).

### Example:

```bash
az role assignment create --role "Key Vault Secrets User" --assignee 257df3b7-efba-415d-9c16-5c1550cdbab1 --scope /subscriptions/ed0d9dbe-2f4a-4f14-94df-452c45994c1e/resourceGroups/student-success/providers/Microsoft.KeyVault/vaults/cosmos-mongo-db
```

### 2. **Verify the Role Assignment**

After running the command, you can verify the role assignment using:

```bash
az role assignment list --assignee <TheirAzureClientId> --scope /subscriptions/<SubscriptionId>/resourceGroups/<ResourceGroupName>/providers/Microsoft.KeyVault/vaults/<YourKeyVaultName>
```

This command will list the roles assigned to the service principal for that specific Key Vault.

### 3. **Retry Accessing the Key Vault**

Once the role assignment is complete, the service principal should have access to the Key Vault and be able to retrieve the secrets.

### **Summary:**

- **Azure RBAC** is used instead of traditional access policies when the Key Vault is configured with `--enable-rbac-authorization`.
- Use `az role assignment create` to assign the `Key Vault Secrets User` role to the service principal.
- Verify the assignment to ensure the service principal has the correct permissions.bn

### 4. **Environment Variables Sharing (Secure Method)**

- If you need to share your environment variables directly (not recommended for security reasons), do so securely using a method like an encrypted file or a secret-sharing service.

### 5. **Running the Docker Containers**

- Once they have the `.env` file configured with the correct Azure credentials, they can run the Docker containers as usual, and the application should work with their credentials.

### **Important Notes:**

- **Security:** Never share sensitive information like `AZURE_CLIENT_SECRET` publicly or in an insecure way. If you have to share it, make sure it's done securely.
- **Role Assignment:** Ensure the Service Principal used has the correct role assignments (e.g., `Contributor`) and scope to access the necessary resources in Azure.
- **Access Policy:** Verify that their Service Principal has the necessary permissions in Azure Key Vault.

### **Summary:**

For someone else to run your application locally, they need to use their Azure credentials in the `.env` file and ensure they have the right permissions to access the necessary Azure resources, such as the Azure Key Vault and Cosmos DB.
