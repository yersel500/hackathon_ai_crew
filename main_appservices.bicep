param location string = resourceGroup().location
param resourceOpenAIName string = 'hackathon-openai'

resource openAI 'Microsoft.CognitiveServices/accounts@2024-04-01-preview' = {
  name: resourceOpenAIName
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    apiProperties: {
      // Add any specific properties you need
    }
  }
}

resource model 'Microsoft.CognitiveServices/accounts/deployments@2024-04-01-preview' =  {
  name: 'deployment-gpt'
  parent: openAI
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-35-turbo'
      version: '0613'}
    raiPolicyName: ''}
    sku: {
    name:'Standard'
    capacity: 1
   }
  }


output openAIEndpoint string = openAI.properties.endpoint



//Storage account
param envResourceNamePrefix string = resourceGroup().name
/* ###################################################################### */
// Create storage account for function app prereq
/* ###################################################################### */
resource azStorageAccount 'Microsoft.Storage/storageAccounts@2021-08-01' = {
  name: '${envResourceNamePrefix}storage'
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
}
var azStorageAccountPrimaryAccessKey = listKeys(azStorageAccount.id, azStorageAccount.apiVersion).keys[0].value



// Create Application Insights
/* ###################################################################### */
resource azAppInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${envResourceNamePrefix}-ai'
  location: location
  kind: 'web'
  properties:{
    Application_Type: 'web'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}
var azAppInsightsInstrumentationKey = azAppInsights.properties.InstrumentationKey

resource azHostingPlan 'Microsoft.Web/serverfarms@2021-03-01' = {
  name: '${envResourceNamePrefix}-asp'
  location: location
  kind: 'linux'
  sku: {
    name: 'B1'
  }
  properties: {
    reserved: true
  }
}

