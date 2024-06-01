# AWS Policy Checker

## Introduction

This project comprises Python scripts utilizing the boto3 library to interact with AWS services. Each script is accompanied by unit tests to ensure its functionality. The aim of this project is to show knowledge in Python, AWS, and boto3 by implementing solutions to various scenarios such as checking for public access in S3 buckets, RDS instances, and managing SSM policies on EC2 instances.

## Description and Usage Information

### Script 1: S3 Check Remove Public Access

Description: This script checks if S3 buckets have public access. If public access is found, it removes the public access configuration to prevent unauthorized access.

Usage:

```
python3 -m code.s3_check_remove_public_access
```

### Script 2: RDS Check Remove Public Access

Description: This script checks if RDS instances have public access. If public access is found, it removes the public access to enhance security.

Usage:

```
python3 -m code.rds_check_remove_public_access
```

### Script 3: EC2 Check Remove SSM Policy

Description: This script checks if EC2 instances have the SSM policy attached to their roles. If the SSM policy is detected, it removes the policy from all instances to manage permissions effectively.
Usage:

```
python3 -m code.ec2_check_remove_ssm_policy
```

## Project Structure

```
AWS_Policy_Checker/
│
├── code/
│   ├── __init__.py 
│   ├── helpers.py 
│   ├── ec2_check_remove_ssm_policy.py
│   ├── rds_check_remove_public_access.py
│   └── s3_check_remove_public_access.py
│
├── tests/
│   ├── __init__.py 
│   ├── test_ec2_check_remove_ssm_policy.py
│   ├── test_rds_check_remove_public_access.py
│   └── test_s3_check_remove_public_access.py
│
├── README.md
├── Makefile 
├── setup.py 
└── requirements.txt
```

- **code/**: Contains Python scripts for interacting with AWS services.
- **tests/**: Holds unit test scripts for each code module to ensure functionality.
- **README.md**: Documentation providing an overview of the project, script descriptions, usage instructions, and project structure.
- **requirements.txt**: Lists the dependencies required to run the scripts.
- **setup.py**: Python script used for packaging the project. It contains metadata such as project name, version, dependencies, and entry points for scripts and modules. 
- **Makefile**: Makefile provides shortcuts for common development tasks.

