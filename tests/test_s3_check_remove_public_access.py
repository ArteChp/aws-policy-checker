# -*- coding: utf-8 -*-
import unittest
import logging
import json
from typing import Dict, Any
from unittest.mock import patch
from moto import mock_aws
import boto3
from code.s3_check_remove_public_access import check_remove_public_access

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for test setup
BUCKET_NAME: str = 's3-test-bucket'
REGION: str = 'us-west-2'

class TestCheckRemovePublicAccess(unittest.TestCase):
    """Unit tests for the check_remove_public_access function."""

    def setUp(self) -> None:
        """Set up the mock S3 environment."""
        self.mock_s3 = mock_aws()
        self.mock_s3.start()
        self.s3 = boto3.client('s3', region_name=REGION)
        self.s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )

    def tearDown(self) -> None:
        """Clean up the mock S3 environment."""
        self.mock_s3.stop()

    @patch('code.s3_check_remove_public_access.initialize_s3_client')
    def test_check_remove_public_access_with_policy(self, mock_initialize_s3_client) -> None:
        """Test removing a public access policy from an S3 bucket."""
        mock_initialize_s3_client.return_value = self.s3

        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': f'arn:aws:s3:::{BUCKET_NAME}/*'
            }]
        }
        bucket_policy_json = json.dumps(bucket_policy)

        # Attach policy for public access
        self.s3.put_bucket_policy(Bucket=BUCKET_NAME, Policy=bucket_policy_json)

        # Invoke the function to check and remove public access
        logger.info("Running test_check_remove_public_access_with_policy...")
        result = check_remove_public_access(self.s3, BUCKET_NAME)

        # Assertions to verify the function's behavior
        self.assertEqual(result['status'], "Success")
        self.assertIn("Removed a policy", result['reason'])

    @patch('code.s3_check_remove_public_access.initialize_s3_client')
    def test_check_remove_no_public_access_with_policy(self, mock_initialize_s3_client) -> None:
        """Test checking an S3 bucket with no public access policy."""
        mock_initialize_s3_client.return_value = self.s3

        # Invoke the function to check and confirm no public access policy
        logger.info("Running test_check_remove_no_public_access_with_policy...")
        result = check_remove_public_access(self.s3, BUCKET_NAME)

        # Assertions to verify the function's behavior
        self.assertEqual(result['status'], "Success")
        self.assertIn("No bucket policy found", result['reason'])

# Entry point for the test script
if __name__ == '__main__':
    result = unittest.main()
    logger.info(result)
