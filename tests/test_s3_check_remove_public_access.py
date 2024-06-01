# -*- coding: utf-8 -*-
import unittest
import json
import boto3
from moto import mock_aws
from code.s3_check_remove_public_access import check_remove_public_access

# Constants for test setup
BUCKET_NAME = 's3-test-bucket'
REGION = 'us-west-2'

class TestCheckRemovePublicAccess(unittest.TestCase):
    
    # Test method to check and remove public access policy from S3 bucket
    @mock_aws
    def test_check_remove_public_access_with_policy(self):

        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': f'arn:aws:s3:::{BUCKET_NAME}/*'
            }]
        }

        # Convert the policy from JSON dict to string
        bucket_policy = json.dumps(bucket_policy)

        s3 = boto3.client('s3', region_name=REGION)

        # Create S3 bucket and attach policy for public access
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )
        s3.put_bucket_policy(Bucket=BUCKET_NAME, Policy=bucket_policy)

        # Invoke the function to check and remove public access
        result = check_remove_public_access(s3, BUCKET_NAME)
        
        # Assertions to verify the function's behavior
        assert "Success" == result['status']
        assert "Removed a policy" in result['reason']

    # Test method for scenario with no public access policy on S3 bucket
    @mock_aws
    def test_check_remove_no_public_access_with_policy(self):

        s3 = boto3.client('s3', region_name=REGION)

        # Create S3 bucket without public access
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )
        # Invoke the function to check and confirm no public access policy
        result = check_remove_public_access(s3, BUCKET_NAME)
        
        # Assertions to verify the function's behavior
        assert "Success" == result['status']
        assert "No bucket policy found" in result['reason']

# Entry point for the test script
if __name__ == '__main__':
    unittest.main()
