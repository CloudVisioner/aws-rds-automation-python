import boto3
import time

# Instantiate a boto3 client for RDS
rds = boto3.client('rds')

# User-defined variables
username = 'rds_boto3'
password = '1234qwer'
db_subnet_group = 'vpc-hol'
db_cluster_id = 'rds-hol-cluster'

try:
    response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
    print(f"The DB cluster named '{db_cluster_id}' already exists. Skipping creation.")
except rds.exceptions.DBClusterNotFoundFault:
    response = rds.create_db_cluster(
        Engine='aurora-mysql',
        EngineVersion='5.7.mysql_aurora.2.11.4',  # Use Aurora MySQL 8.0 which supports serverless
        DBClusterIdentifier=db_cluster_id,
        MasterUsername=username,
        MasterUserPassword=password,
        DatabaseName='rds_hol_db',
        DBSubnetGroupName=db_subnet_group,
        #EnableHttpEndpoint=True
        # Remove the ScalingConfiguration and EngineMode if using provisioned
    )
    print(f"The DB cluster named '{db_cluster_id}' has been created.")

    # Wait for the DB cluster to become available
    while True:
        response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
        status = response['DBClusters'][0]['Status']
        print(f"The status of the cluster is '{status}'")
        
        if status == 'available':
            break

        print("Waiting for the DB Cluster to become available...")
        time.sleep(40)

print("The DB Cluster is now available.")
