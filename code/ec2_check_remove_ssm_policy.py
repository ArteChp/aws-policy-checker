# -*- coding: utf-8 -*-
import logging
from typing import Tuple
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from .helpers import initialize_clients, describe_instances, get_instance_profile, list_attached_policies, detach_policy,handle_error, handle_success

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_remove_ssm_policy(region: str = "us-east-1") -> str:
    """
    Check all EC2 instances for assigned SSM policy on their IAM roles and remove it if found.

    :param region: AWS region where the EC2 instances are located
    :return: Result message
    :raises NoCredentialsError: If AWS credentials are not found.
    :raises PartialCredentialsError: If incomplete AWS credentials are provided.
    """
    try:
        ec2_client, iam_client = initialize_clients(region)
        response = describe_instances(ec2_client)

        # Iterate over all instances
        ssm_instances = 0
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                ssm_instances += process_instance(iam_client, instance)
        
        if ssm_instances > 0: 
            return handle_success(f"Detached SSM policy from roles of {ssm_instances} instance/-s") 
        else:
            return handle_success("No instances with SSM policy")
    
    except (NoCredentialsError, PartialCredentialsError) as e:
        return handle_error(e, "Error: ")
    except Exception as e:
        return handle_error(e, "Unexpected error: ")


def process_instance(iam_client, instance: dict) -> int:
    """
    Process an EC2 instance to check and detach SSM policy if attached.

    :param iam_client: Initialized IAM client
    :param instance: EC2 instance information
    :return: Number of instances from which SSM policy was detached
    """
    ssm_detached_count = 0

    if 'IamInstanceProfile' in instance:
        profile_name = instance['IamInstanceProfile']['Arn'].split('/')[-1]
        instance_profile = get_instance_profile(iam_client, profile_name)

        # Iterate over roles in the instance profile
        for role in instance_profile['InstanceProfile']['Roles']:
            role_name = role['RoleName']
            attached_policies = list_attached_policies(iam_client, role_name)

            # Check for SSM policy and detach if found
            for policy in attached_policies['AttachedPolicies']:
                if policy['PolicyName'] == 'AmazonSSMManagedInstanceCore':
                    detach_policy(iam_client, role_name, policy['PolicyArn'])
                    ssm_detached_count += 1

    return ssm_detached_count

if __name__ == '__main__':
    result = check_remove_ssm_policy()
    logger.info(result)
