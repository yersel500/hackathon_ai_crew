### Step 1: Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/yersel500/hackathon_ai_crew
cd bicep
```

### Step 2: Configure Parameters

Edit the [main.bicepparam](./main.bicepparam) parameters file:
Location
ObjectID: Azure Entra
prefix and suffix


### Step 3: Deploy Resources

Use the [deploy.sh](./deploy.sh) Bash script to deploy the Azure resources via Bicep. This script will provision all the necessary resources as defined in the Bicep templates.

Run the following command to deploy the resources:

```bash
./deploy.sh --resourceGroupName <resource-group-name> --location <location> --virtualNetworkResourceGroupName <client-virtual-network-resource-group-name>
```

