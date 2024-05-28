import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient

# Set up the Azure credentials
credential = DefaultAzureCredential()

# Replace with your Azure subscription ID
subscription_id = 'your_subscription_id'

# Initialize the Compute and Network clients
compute_client = ComputeManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

# Get a list of all resource groups
resource_groups = [rg.name for rg in compute_client.resource_groups.list()]

# Delete unassigned disks


def delete_unassigned_disks():
    for rg in resource_groups:
        disks = compute_client.disks.list_by_resource_group(rg)
        for disk in disks:
            if disk.managed_by is None:
                print(f"Deleting unassigned disk: {disk.name}")
                compute_client.disks.begin_delete(rg, disk.name).result()

# Delete unassigned public IP addresses


def delete_unassigned_public_ips():
    for rg in resource_groups:
        public_ips = network_client.public_ip_addresses.list(rg)
        for ip in public_ips:
            if ip.ip_configuration is None:
                print(f"Deleting unassigned public IP address: {ip.name}")
                network_client.public_ip_addresses.begin_delete(
                    rg, ip.name).result()


if __name__ == '__main__':
    delete_unassigned_disks()
    delete_unassigned_public_ips()
