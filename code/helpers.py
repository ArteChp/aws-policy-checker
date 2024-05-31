# -*- coding: utf-8 -*-

import boto3

def initialize_clients(region):
    ec2_client = boto3.client('ec2', region_name=region)
    iam_client = boto3.client('iam', region_name=region)
    return ec2_client, iam_client

def initialize_s3_client(region):
    return boto3.client('s3', region_name=region)

def get_bucket_policy(s3_client, bucket_name):
    return s3_client.get_bucket_policy(Bucket=bucket_name)

def delete_bucket_policy(s3_client, bucket_name):

    print(f"Bucket {bucket_name} has a bucket policy. Removing policy.")
    s3_client.delete_bucket_policy(Bucket=bucket_name)
    print(f"Bucket {bucket_name} policy removed.")

def describe_instances(ec2_client):
    return ec2_client.describe_instances()

def get_instance_profile(iam_client, profile_name):
    return iam_client.get_instance_profile(InstanceProfileName=profile_name)

def list_attached_policies(iam_client, role_name):
    return iam_client.list_attached_role_policies(RoleName=role_name)

def detach_policy(iam_client, role_name, policy_arn):
    iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
    print(f"Detaching SSM policy from role: {role_name}")

def initialize_rds_client(region):
    return boto3.client('rds', region_name=region)

def describe_db_instances(rds_client):
    return rds_client.describe_db_instances()

def check_public_access(instance):
    return instance.get('PubliclyAccessible')

def modify_db_instance(rds_client, instance_id):
    rds_client.modify_db_instance(
        DBInstanceIdentifier=instance_id,
        PubliclyAccessible=False,
        ApplyImmediately=True
    )
    print(f"Disabling public access for RDS instance: {instance_id}")

def handle_success(message):
    print(f"{message}")
    return {"status": "Success", "reason": message}

def handle_error(exception, message):
    print(f"{message}{exception}")
    return {"status": "Error", "reason": f"{message}{exception}"}
