# -*- coding: utf-8 -*-
import unittest
from moto import mock_aws
import boto3
from botocore.exceptions import ClientError
from code.rds_check_remove_public_access import check_remove_public_access

# Constants for test setup
REGION = 'us-west-2'
DB_NAME = 'test-db'
DB_INSTANCE = 'db.t4g.micro' 
DB_ENGINE = 'mysql'
DB_USER = 'admin'
DB_PASS = 'password'

class TestRdsCheckRemovePublicAccess(unittest.TestCase):

    # Test method to check and remove public access from an RDS instance
    @mock_aws
    def test_check_remove_public_access(self):
        rds = boto3.client('rds', region_name=REGION)
        
        # Create a mock RDS instance with public access
        rds.create_db_instance(
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
        assert "Success" == result['status']
        assert "Disabled public access for" in result['reason']
    
    # Test method for scenario with no public access on RDS instance
    @mock_aws
    def test_check_remove_no_public_access(self):
        rds = boto3.client('rds', region_name=REGION)
        
        # Create a mock RDS instance without public access
        rds.create_db_instance(
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
        assert "Success" == result['status']
        assert "No public access for RDS instance" in result['reason']

# Entry point for the test script
if __name__ == '__main__':
    unittest.main()
