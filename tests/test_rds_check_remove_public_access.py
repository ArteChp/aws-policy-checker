# -*- coding: utf-8 -*-
import unittest
from moto import mock_aws
import logging
import boto3
from botocore.exceptions import ClientError
from code.rds_check_remove_public_access import check_remove_public_access

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for test setup
REGION = 'us-west-2'
DB_NAME = 'test-db'
DB_INSTANCE = 'db.t4g.micro' 
DB_ENGINE = 'mysql'
DB_USER = 'admin'
DB_PASS = 'password'


class TestRdsCheckRemovePublicAccess(unittest.TestCase):

    def setUp(self):
        """Set up the mock RDS environment."""
        logger.info("Setting up the mock RDS environment")
        self.mock_rds = mock_aws()
        self.mock_rds.start()
        self.rds = boto3.client('rds', region_name=REGION)

    def tearDown(self):
        """Clean up the mock RDS environment."""
        self.mock_rds.stop()

    @mock_aws
    def test_remove_public_access_success(self):
        """Test removing public access from an RDS instance."""
        logger.info("Running test_remove_public_access_success")

        # Create a mock RDS instance with public access
        self.rds.create_db_instance(
            DBInstanceIdentifier=DB_NAME,
            AllocatedStorage=20,
            DBInstanceClass=DB_INSTANCE,
            Engine=DB_ENGINE,
            MasterUsername=DB_USER,
            MasterUserPassword=DB_PASS,
            PubliclyAccessible=True
        )

        # Invoke the function to check and remove public access
        result = check_remove_public_access(REGION)
        
        # Assertions to verify the function's behavior
        self.assertEqual(result['status'], "Success")
        self.assertIn("Disabled public access for", result['reason'])

    @mock_aws
    def test_no_public_access(self):
        """Test checking an RDS instance with no public access."""
        logger.info("Running test_no_public_access")

        # Create a mock RDS instance without public access
        self.rds.create_db_instance(
            DBInstanceIdentifier=DB_NAME,
            AllocatedStorage=20,
            DBInstanceClass=DB_INSTANCE,
            Engine=DB_ENGINE,
            MasterUsername=DB_USER,
            MasterUserPassword=DB_PASS,
            PubliclyAccessible=False
        )

        # Invoke the function to check and confirm no public access
        result = check_remove_public_access(REGION)
        
        # Assertions to verify the function's behavior
        self.assertEqual(result['status'], "Success")
        self.assertIn("No public access for RDS instance", result['reason'])

# Entry point for the test script
if __name__ == '__main__':
    result = unittest.main()
    logger.info(result)
