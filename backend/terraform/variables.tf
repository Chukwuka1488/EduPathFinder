# Define the subscription ID
variable "subscription_id" {
  description = "The subscription ID for the Azure account"
  type        = string
  # default     = "******-*****-*****" # Add your azure subscription_id here
}

# Define the resource group name
variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "student-success"
}

# Define the location for the resources
variable "location" {
  description = "The location of the resources"
  type        = string
  default     = "centralus"
}

# Define the Cosmos DB account name
variable "cosmosdb_account_name" {
  description = "The name of the Cosmos DB account"
  type        = string
  default     = "edupathfinder-cosmosdb-account"
}

variable "acr_name" {
  description = "The name of the Azure Container Registry"
  type        = string
}