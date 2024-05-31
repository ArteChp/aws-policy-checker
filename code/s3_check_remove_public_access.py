# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from code.helpers import initialize_s3_client, get_bucket_policy, delete_bucket_policy, handle_error, handle_success

def check_remove_public_access(bucket_name, region = "us-east-1"):
    """
    Check if an S3 bucket has public access, and if so, remove it.

    :param bucket_name: Name of the S3 bucket
    """

    s3_client = initialize_s3_client(region)

    # Check bucket policy
    try:
        bucket_policy = get_bucket_policy(s3_client, bucket_name)
        if bucket_policy:
            # Remove bucket policy
            delete_bucket_policy(s3_client, bucket_name)
            return handle_success(f"Bucket {bucket_name} has a bucket policy. Removed a policy.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            return handle_success(f"No bucket policy found for {bucket_name}") 
        else:
            print(f"Error checking bucket policy: {e}")
            return handle_error(f"Error checking bucket policy: {e}") 


def main():
    """
    Main function to check all S3 buckets and remove public access if found.
    """
    s3_client = initialize_s3_client(region)
    try:
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        for bucket in buckets:
            check_and_remove_public_access(bucket['Name'])
    except NoCredentialsError:
        return handle_error("Credentials not available.") 


if __name__ == '__main__':
    main()
