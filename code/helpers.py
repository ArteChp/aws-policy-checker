# -*- coding: utf-8 -*-
import boto3
import logging
from typing import Tuple, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_clients(region: str) -> Tuple[boto3.client, boto3.client]:
    """
    Initializes EC2 and IAM clients.

    :param region: AWS region name
    :return: Tuple of EC2 and IAM clients
    """
    ec2_client = boto3.client('ec2', region_name=region)
    iam_client = boto3.client('iam', region_name=region)
    return ec2_client, iam_client

def initialize_s3_client(region: str) -> boto3.client:
    """
    Initializes S3 client.

    :param region: AWS region name
    :return: S3 client
    """
    return boto3.client('s3', region_name=region)

def initialize_rds_client(region: str) -> boto3.client:
    """
    Initializes RDS client.

    :param region: AWS region name
    :return: RDS client
    """
    return boto3.client('rds', region_name=region)

def get_bucket_policy(s3_client: boto3.client, bucket_name: str) -> Dict[str, Any]:
    """
    Retrieves the bucket policy for a specified S3 bucket.

    :param s3_client: Initialized S3 client
    :param bucket_name: Name of the S3 bucket
    :return: Bucket policy
    """
    return s3_client.get_bucket_policy(Bucket=bucket_name)

def delete_bucket_policy(s3_client: boto3.client, bucket_name: str) -> None:
    """
    Deletes the bucket policy for a specified S3 bucket.

    :param s3_client: Initialized S3 client
    :param bucket_name: Name of the S3 bucket
    """
    s3_client.delete_bucket_policy(Bucket=bucket_name)
    logger.info(f"Bucket {bucket_name} policy removed.")

def describe_instances(ec2_client: boto3.client) -> Dict[str, Any]:
    """
    Describes EC2 instances.

    :param ec2_client: Initialized EC2 client
    :return: Description of EC2 instances
    """
    return ec2_client.describe_instances()

def get_instance_profile(iam_client: boto3.client, profile_name: str) -> Dict[str, Any]:
    """
    Retrieves an IAM instance profile.

    :param iam_client: Initialized IAM client
    :param profile_name: Name of the IAM instance profile
    :return: Instance profile
    """
    return iam_client.get_instance_profile(InstanceProfileName=profile_name)

def list_attached_policies(iam_client: boto3.client, role_name: str) -> Dict[str, Any]:
    """
    Lists policies attached to a specified IAM role.

    :param iam_client: Initialized IAM client
    :param role_name: Name of the IAM role
    :return: List of attached policies
    """
    return iam_client.list_attached_role_policies(RoleName=role_name)

def detach_policy(iam_client: boto3.client, role_name: str, policy_arn: str) -> None:
    """
    Detaches a policy from a specified IAM role.

    :param iam_client: Initialized IAM client
    :param role_name: Name of the IAM role
    :param policy_arn: ARN of the policy to detach
    """
    iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
    logger.info(f"Detached SSM policy from role: {role_name}")

def describe_db_instances(rds_client: boto3.client) -> Dict[str, Any]:
    """
    Describes RDS instances.

    :param rds_client: Initialized RDS client
    :return: Description of RDS instances
    """
    return rds_client.describe_db_instances()

def check_public_access(instance: Dict[str, Any]) -> bool:
    """
    Checks if an RDS instance has public access.

    :param instance: RDS instance information
    :return: True if the instance is publicly accessible, False otherwise
    """
    return instance.get('PubliclyAccessible', False)

def modify_db_instance(rds_client: boto3.client, instance_id: str) -> None:
    """
    Modifies an RDS instance to disable public access.

    :param rds_client: Initialized RDS client
    :param instance_id: ID of the RDS instance
    """
    rds_client.modify_db_instance(
        DBInstanceIdentifier=instance_id,
        PubliclyAccessible=False,
        ApplyImmediately=True
    )
    logger.info(f"Disabled public access for RDS instance: {instance_id}")

def handle_success(message: str) -> Dict[str, str]:
    """
    Handles success response.

    :param message: Success message
    :return: Success response dictionary
    """
    logger.info(message)
    return {"status": "Success", "reason": message}

def handle_error(exception: Exception, message: str) -> Dict[str, str]:
    """
    Handles error response.

    :param exception: Exception object
    :param message: Error message
    :return: Error response dictionary
    """
    logger.error(f"{message}{exception}")
    return {"status": "Error", "reason": f"{message}{exception}"}
