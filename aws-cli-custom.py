#!/bin/python3 

# Import necessary libraries
# argparse: for handling command-line arguments
# boto3: AWS SDK for Python to interact with AWS services
# botocore.exceptions: for handling various AWS-related exceptions
import argparse
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Initialize AWS clients for EC2, S3, and IAM services
ec2 = boto3.client('ec2')  # EC2 client for managing instances
s3 = boto3.client('s3')    # S3 client for handling object storage
iam = boto3.client('iam')  # IAM client for managing policies and roles

# Function to start EC2 instances based on the instance name
def start_ec2(instance_name):
    """
    Starts EC2 instance(s) with a given name.

    :param instance_name: Name of the EC2 instance (tagged with 'Name') to start
    """
    try:
        # Retrieve instance IDs matching the given name
        instance_ids = get_instance_id_by_name(instance_name)
        if instance_ids:
            # Start the EC2 instance(s)
            ec2.start_instances(InstanceIds=instance_ids)
            print(f"Starting instance(s): {', '.join(instance_ids)}")
    except ClientError as e:
        # Handle errors related to AWS services
        print(f"Failed to start instance(s): {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")

# Function to stop EC2 instances based on the instance name
def stop_ec2(instance_name):
    """
    Stops EC2 instance(s) with a given name.

    :param instance_name: Name of the EC2 instance (tagged with 'Name') to stop
    """
    try:
        # Retrieve instance IDs matching the given name
        instance_ids = get_instance_id_by_name(instance_name)
        if instance_ids:
            # Stop the EC2 instance(s)
            ec2.stop_instances(InstanceIds=instance_ids)
            print(f"Stopping instance(s): {', '.join(instance_ids)}")
    except ClientError as e:
        # Handle errors related to AWS services
        print(f"Failed to stop instance(s): {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")

# Function to upload a file to an S3 bucket
def upload_file_s3(bucket_name, file_name):
    """
    Uploads a file to the specified S3 bucket.

    :param bucket_name: Name of the S3 bucket
    :param file_name: Local path to the file being uploaded
    """
    try:
        # Upload the file to the specified S3 bucket
        s3.upload_file(file_name, bucket_name, file_name)
        print(f"Uploaded {file_name} to {bucket_name}")
    except FileNotFoundError:
        # Handle case where the specified file is not found
        print(f"File {file_name} not found")
    except NoCredentialsError:
        # Handle missing AWS credentials
        print("AWS credentials not found")
    except ClientError as e:
        # Handle errors related to AWS services
        print(f"Failed to upload file to S3: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")

# Function to create an IAM policy
def create_policy(policy_name, policy_document):
    """
    Creates an IAM policy with the given name and policy document.

    :param policy_name: Name of the policy to create
    :param policy_document: Policy document in JSON format defining permissions
    """
    try:
        # Create a new IAM policy
        response = iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=policy_document
        )
        print(f"Created policy {policy_name}")
    except ClientError as e:
        # Handle errors related to AWS services
        print(f"Failed to create policy: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")

# Helper function to retrieve EC2 instance IDs based on instance name tag
def get_instance_id_by_name(instance_name):
    """
    Retrieves EC2 instance IDs by searching for instances with a specific 'Name' tag.

    :param instance_name: Name of the EC2 instance (tagged with 'Name') to retrieve
    :return: List of instance IDs matching the provided name, or None if no instances are found
    """
    try:
        # Describe EC2 instances with a 'Name' tag matching the instance_name
        response = ec2.describe_instances(
            Filters=[{
                'Name': 'tag:Name',
                'Values': [instance_name]
            }]
        )
        # Initialize list to store found instance IDs
        instance_ids = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])
        
        if not instance_ids:
            # Handle case where no instances are found with the given name
            print(f"No instances found with the name: {instance_name}")
            return None
        return instance_ids
    except ClientError as e:
        # Handle errors related to AWS services
        print(f"Failed to retrieve instance ID: {e}")
        return None
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")
        return None

# Main function for parsing command-line arguments and executing commands
def main():
    """
    Main function to parse command-line arguments and execute the corresponding AWS operation.
    Supports starting/stopping EC2 instances, uploading files to S3, and creating IAM policies.
    """
    parser = argparse.ArgumentParser(description="Custom AWS CLI Tool")

    # Define subcommands for different operations
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Subcommand to start an EC2 instance
    ec2_start_parser = subparsers.add_parser('start-ec2', help='Start an EC2 instance by name')
    ec2_start_parser.add_argument('instance_name', help='Name of the EC2 instance to start')

    # Subcommand to stop an EC2 instance
    ec2_stop_parser = subparsers.add_parser('stop-ec2', help='Stop an EC2 instance by name')
    ec2_stop_parser.add_argument('instance_name', help='Name of the EC2 instance to stop')

    # Subcommand to upload a file to an S3 bucket
    s3_upload_parser = subparsers.add_parser('upload-s3', help='Upload a file to an S3 bucket')
    s3_upload_parser.add_argument('bucket_name', help='Name of the S3 bucket')
    s3_upload_parser.add_argument('file_name', help='Path to the file to upload')

    # Subcommand to create an IAM policy
    iam_policy_parser = subparsers.add_parser('create-policy', help='Create an IAM policy')
    iam_policy_parser.add_argument('policy_name', help='Name of the IAM policy')
    iam_policy_parser.add_argument('policy_document', help='Policy document in JSON format')

    # Provide usage examples
    parser.epilog = """
    Example usage:

    Start an EC2 instance:
    python aws-cli-custom.py start-ec2 MyInstanceName

    Stop an EC2 instance:
    python aws-cli-custom.py stop-ec2 MyInstanceName

    Upload a file to S3:
    python aws-cli-custom.py upload-s3 my-bucket myfile.txt

    Create an IAM policy:
    python aws-cli-custom.py create-policy MyPolicy '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}'
    """

    # Parse command-line arguments
    args = parser.parse_args()

    # Execute the corresponding function based on the command provided
    if args.command == 'start-ec2':
        if not args.instance_name:
            print("Error: 'instance_name' is required for start-ec2")
        else:
            start_ec2(args.instance_name)

    elif args.command == 'stop-ec2':
        if not args.instance_name:
            print("Error: 'instance_name' is required for stop-ec2")
        else:
            stop_ec2(args.instance_name)

    elif args.command == 'upload-s3':
        if not args.bucket_name or not args.file_name:
            print("Error: Both 'bucket_name' and 'file_name' are required for upload-s3")
        else:
            upload_file_s3(args.bucket_name, args.file_name)

    elif args.command == 'create-policy':
        if not args.policy_name or not args.policy_document:
            print("Error: Both 'policy_name' and 'policy_document' are required for create-policy")
        else:
            create_policy(args.policy_name, args.policy_document)

    else:
        parser.print_help()

# Entry point for the script
if __name__ == '__main__':
    main()
