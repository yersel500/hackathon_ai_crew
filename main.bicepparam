using './main.bicep'

param prefix = 'bami6'
param suffix = 'test6'
param userObjectId = 'fba16f87-9491-4997-95bf-4f4d8621a457'
param keyVaultEnablePurgeProtection = false
param acrEnabled = true
param vmAdminUsername = 'azadmin'
param vmAdminPasswordOrKey = 'Trustno1234!'
param openAiDeployments = [
  {
    model: {
      name: 'text-embedding-ada-002'
      version: '2'
    }
    sku: {
      name: 'Standard'
      capacity: 2
    }
  }
  {
    model: {
      name: 'gpt-4o'
      version: '2024-05-13'
    }
    sku: {
      name: 'GlobalStandard'
      capacity: 1
    }
  }
]
param tags = {
  environment: 'development'
  iac: 'bicep'
}
