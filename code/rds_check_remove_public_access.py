# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from .helpers import initialize_rds_client, describe_db_instances, check_public_access, modify_db_instance, handle_error, handle_success

def check_remove_public_access(region: str = "us-east-1") -> str:
    """
    Check all RDS instances for public accessibility and disable it if found.


    :param region: AWS region where the RDS instances are located
    :return: Success or error message
    :raises NoCredentialsError: If AWS credentials are not found.
    :raises PartialCredentialsError: If incomplete AWS credentials are provided.
    """
    try:
        # Initialize RDS client
        rds_client = initialize_rds_client(region)

        # Describe RDS instances
        response = describe_db_instances(rds_client)

        rds_instances = 0
        for instance in response['DBInstances']:
            # Check if RDS instance has public access
            if check_public_access(instance):
                instance_id = instance['DBInstanceIdentifier']
                # Modify RDS instance to disable public access
                modify_db_instance(rds_client, instance_id)
                rds_instances += 1
        if rds_instances > 0: 
            return handle_success(f"Disabled public access for {rds_instances} RDS instance/-s") 
        else:
            return handle_success("No public access for RDS instance")

    except NoCredentialsError as e:
        return handle_error(e, "AWS credentials not found.")
    except PartialCredentialsError as e:
        return handle_error(e, "Incomplete AWS credentials provided.")
    except Exception as e:
        return handle_error(e, "Unexpected error: ")

if __name__ == '__main__':
    check_remove_public_access()
