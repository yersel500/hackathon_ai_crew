@description('Base name of the resource, such as web app name and app service plan')
@minLength(2)
param webAppName string = 'AzureLinuxApp'

@description('The SKU of the App Service Plan')
param sku string = 'B1'

@description('Location for all resources')
param location string = 'canadacentral'

var webAppPortalName = '${webAppName}-webapp3'
var appServicePlanName = 'AppServicePlan3-${webAppName}'

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: sku
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webAppPortal 'Microsoft.Web/sites@2022-03-01' = {
  name: webAppPortalName
  location: location
  kind: 'app,linux,container'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'DOCKER|nginx' // Forzar el modo Docker
      ftpsState: 'FtpsOnly'
    }
  }
} 
