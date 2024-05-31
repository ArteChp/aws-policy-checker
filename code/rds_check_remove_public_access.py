# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from code.helpers import initialize_rds_client, describe_db_instances, check_public_access, modify_db_instance, handle_error, handle_success

def check_remove_public_access(region = "us-east-1"):
    """
    Check all RDS instances for public accessibility and disable it if found.

    Raises:
        NoCredentialsError: If AWS credentials are not found.
        PartialCredentialsError: If incomplete AWS credentials are provided.
    """
    try:
        rds_client = initialize_rds_client(region)
        response = describe_db_instances(rds_client)

        for instance in response['DBInstances']:
            if check_public_access(instance):
                instance_id = instance['DBInstanceIdentifier']
                modify_db_instance(rds_client, instance_id)
                return handle_success(f"Disabled public access for RDS instance: {instance_id}") 
            else:
                return handle_success("No public access for RDS instance") 

    except (NoCredentialsError, PartialCredentialsError) as e:
        return handle_error(e, "Error: ")
    except Exception as e:
        return handle_error(e, "Unexpected error: ")

if __name__ == '__main__':
    check_remove_public_access()
