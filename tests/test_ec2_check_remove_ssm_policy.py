import unittest
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from moto import mock_aws
from code.ec2_check_remove_ssm_policy import check_remove_ssm_policy

# JSON policy document for SSM instance policy
SSM_INSTANCE_POLICY = """
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:DescribeAssociation",
                "ssm:GetDeployablePatchSnapshotForInstance",
                "ssm:GetDocument",
                "ssm:DescribeDocument",
                "ssm:GetManifest",
                "ssm:GetParameter",
                "ssm:GetParameters",
                "ssm:ListAssociations",
                "ssm:ListInstanceAssociations",
                "ssm:PutInventory",
                "ssm:PutComplianceItems",
                "ssm:PutConfigurePackageResult",
                "ssm:UpdateAssociationStatus",
                "ssm:UpdateInstanceAssociationStatus",
                "ssm:UpdateInstanceInformation"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2messages:AcknowledgeMessage",
                "ec2messages:DeleteMessage",
                "ec2messages:FailMessage",
                "ec2messages:GetEndpoint",
                "ec2messages:GetMessages",
                "ec2messages:SendReply"
            ],
            "Resource": "*"
        }
    ]
}
"""

# JSON policy document for assuming role
ROLE_POLICY_DOC = """
{
    "Version": "2012-10-17", 
    "Statement": [
        {
            "Effect": "Allow", 
            "Principal": 
                {
                    "Service": "ec2.amazonaws.com"
                }, 
            "Action": "sts:AssumeRole"
        }
    ]
}
"""

# Constants for test setup
REGION="us-west-2"
PROFILE_NAME = 'test_profile'
ROLE_NAME = 'test_role'
AMI = 'ami-061392db613a6357b' 

# Test method to check removal of SSM policy
class TestCheckRemoveSSMPolicy(unittest.TestCase):

    @mock_aws
    def test_check_remove_ssm_policy(self):

        iam = boto3.client('iam', region_name=REGION)
        
        # Create instance profile
        instance_profile = iam.create_instance_profile(
            InstanceProfileName=PROFILE_NAME
        )

        # Create role with assume role policy
        iam.create_role(
            RoleName=ROLE_NAME, 
            AssumeRolePolicyDocument=ROLE_POLICY_DOC
        )
        
        # Create policy and attach it to the role
        policy_arn = iam.create_policy(
            PolicyName="AmazonSSMManagedInstanceCore", 
            PolicyDocument=SSM_INSTANCE_POLICY
        )
        
        iam.attach_role_policy(
            RoleName=ROLE_NAME, 
            PolicyArn=policy_arn['Policy']['Arn']
        )
        
        # Add role to instance profile
        iam.add_role_to_instance_profile(
            InstanceProfileName=PROFILE_NAME,
            RoleName=ROLE_NAME
        )

        ec2 = boto3.resource('ec2', region_name=REGION)
        
        # Create EC2 instance with IAM instance profile
        instance = ec2.create_instances(
            ImageId=AMI,
            MinCount=1,
            MaxCount=1,
            IamInstanceProfile={
                'Arn': instance_profile['InstanceProfile']['Arn']
                }
        )[0]

        instance.wait_until_exists()
        
        # Invoke the function to check and remove SSM policy
        result = check_remove_ssm_policy(REGION)
        
        # Assertions to verify the function's behavior
        assert "Success" == result['status']
        assert "Detached SSM policy from role" in result['reason']

    @mock_aws
    def test_check_remove_no_ssm_policy(self):

        ec2 = boto3.resource('ec2', region_name=REGION)

        # Create EC2 instance without IAM instance profile
        instance = ec2.create_instances(
            ImageId=AMI,
            MinCount=1,
            MaxCount=1
        )[0]

        instance.wait_until_exists()
        
        # Invoke the function to check and remove SSM policy
        result = check_remove_ssm_policy(REGION)

        # Assertions to verify the function's behavior
        assert "Success" == result['status']
        assert "No instances with SSM policy" in result['reason']

if __name__ == '__main__':
    unittest.main()
