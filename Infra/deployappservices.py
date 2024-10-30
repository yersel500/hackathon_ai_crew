import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Set your variables
subscription_id = '6e2de274-878a-4770-a22c-29ba015954cb'#'1ebc319f-022d-4336-ae45-bc25500bfcea'#'2f09114e-b75d-4998-9d09-23fbf442ebea'#'6e2de274-878a-4770-a22c-29ba015954cb'#
os.system(f'az account set --subscription {subscription_id}')   
location = 'westus2'
resource_group_name = 'test5'+location

# Authenticate
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)

# Create Resource Group
resource_client.resource_groups.create_or_update(resource_group_name, {'location': location})

# Deploy Bicep Template
bicep_template_path = 'main.bicep'
os.system(f'az deployment group create --resource-group {resource_group_name} --template-file {bicep_template_path}')   