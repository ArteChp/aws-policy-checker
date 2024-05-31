# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from code.helpers import initialize_clients, describe_instances, get_instance_profile, list_attached_policies, detach_policy,handle_error, handle_success


def check_remove_ssm_policy(region = "us-east-1"):
    """
    Check all EC2 instances for assigned SSM policy on their IAM roles and remove it if found.

    Raises:
        NoCredentialsError: If AWS credentials are not found.
        PartialCredentialsError: If incomplete AWS credentials are provided.
    """
    try:
        ec2_client, iam_client = initialize_clients(region)
        response = describe_instances(ec2_client)

        # Iterate over all instances
        ssm_instances = 0
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if 'IamInstanceProfile' in instance:
                    profile_arn = instance['IamInstanceProfile']['Arn']
                    profile_name = profile_arn.split('/')[-1]

                    instance_profile = get_instance_profile(iam_client, profile_name)

                    # Iterate over roles in the instance profile
                    for role in instance_profile['InstanceProfile']['Roles']:
                        role_name = role['RoleName']
                        attached_policies = list_attached_policies(iam_client, role_name)

                        # Check for SSM policy and detach if found
                        for policy in attached_policies['AttachedPolicies']:
                            if policy['PolicyName'] == 'AmazonSSMManagedInstanceCore':
                                detach_policy(iam_client, role_name, policy['PolicyArn'])
                                ssm_instances += 1
        
        if ssm_instances > 0: 
            return handle_success(f"Detached SSM policy from roles of {ssm_instances} instance/-s") 
        else:
            return handle_success("No instances with SSM policy")
    
    except (NoCredentialsError, PartialCredentialsError) as e:
        return handle_error(e, "Error: ")
    except Exception as e:
        return handle_error(e, "Unexpected error: ")

if __name__ == '__main__':
    check_remove_ssm_policy()
