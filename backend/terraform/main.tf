terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id            = var.subscription_id
  skip_provider_registration = true
}

resource "azurerm_resource_group" "az_res_grp" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_cosmosdb_account" "az_cosmos_mongo" {
  name                = var.cosmosdb_account_name
  location            = azurerm_resource_group.az_res_grp.location
  resource_group_name = azurerm_resource_group.az_res_grp.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = false
  is_virtual_network_filter_enabled = false
  enable_multiple_write_locations   = false
  enable_free_tier                  = true
  public_network_access_enabled     = true  # Allow connectivity from all networks

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = var.location
    failover_priority = 0
  }

  capabilities {
    name = "EnableMongo"
  }

  tags = {
    environment = "development"
    project     = "edupathfinder"
  }
}

resource "azurerm_cosmosdb_mongo_database" "mongodb" {
  name                = "cosmosmongodb"
  resource_group_name = azurerm_cosmosdb_account.az_cosmos_mongo.resource_group_name
  account_name        = azurerm_cosmosdb_account.az_cosmos_mongo.name
  throughput          = 400  # Set throughput to 100 RUs
}

# resource "azurerm_cosmosdb_mongo_collection" "coll" {
#   name                = "cosmosmongodbcollection"
#   resource_group_name = azurerm_cosmosdb_account.az_cosmos_mongo.resource_group_name
#   account_name        = azurerm_cosmosdb_account.az_cosmos_mongo.name
#   database_name       = azurerm_cosmosdb_mongo_database.mongodb.name

#   default_ttl_seconds = 777  # TTL setting for auto-deleting documents
#   shard_key           = "uniqueKey"
#   throughput          = 400  # Set throughput to 400 RUs

#   index {
#     keys    = ["_id"]
#   }

#   lifecycle {
#     ignore_changes = [index]
#   }

#   depends_on = [azurerm_cosmosdb_mongo_database.mongodb]
# }

# Azure Container Registry (ACR)
resource "azurerm_container_registry" "acr" {
  name                     = var.acr_name
  resource_group_name      = azurerm_resource_group.az_res_grp.name
  location                 = azurerm_resource_group.az_res_grp.location
  sku                      = "Basic"  # Choose SKU (Basic, Standard, Premium)
  admin_enabled            = true  # Optional: Enable the admin user
  
  # Optional: Tags to help categorize your resources
  tags = {
    environment = "development"
    project     = "edupathfinder"
  }
}