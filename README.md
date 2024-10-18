# AWS Custom CLI

A custom Python-based CLI tool to manage AWS services like EC2, S3, and IAM using `boto3`. This tool simplifies operations like starting/stopping EC2 instances, uploading files to S3, and creating IAM policies.

## Features

- **Start/Stop EC2 Instances**: Manage EC2 instances by specifying the instance name (tagged as `Name`).
- **Upload Files to S3**: Upload files to a specified S3 bucket.
- **Create IAM Policies**: Create new IAM policies using a provided JSON document.

## Prerequisites

- Python 3.x installed
- AWS CLI configured with valid credentials (AWS Access Key ID, Secret Access Key)
- Python libraries: `boto3`, `argparse`

To configure your AWS CLI, run:

```bash
aws configure
```

Follow the prompts to set your AWS credentials and region.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/VanHelwig/aws-custom-cli.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd aws-custom-cli
   ```

3. **(Optional) Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

This tool provides several commands to interact with AWS resources.

### Start an EC2 Instance

To start an EC2 instance by specifying its name (tagged as `Name`):

```bash
python aws-cli-custom.py start-ec2 <instance_name>
```

Example:

```bash
python aws-cli-custom.py start-ec2 MyInstanceName
```

### Stop an EC2 Instance

To stop an EC2 instance by specifying its name (tagged as `Name`):

```bash
python aws-cli-custom.py stop-ec2 <instance_name>
```

Example:

```bash
python aws-cli-custom.py stop-ec2 MyInstanceName
```

### Upload a File to S3

To upload a local file to an S3 bucket:

```bash
python aws-cli-custom.py upload-s3 <bucket_name> <file_name>
```

Example:

```bash
python aws-cli-custom.py upload-s3 my-bucket myfile.txt
```

### Create an IAM Policy

To create an IAM policy by specifying the policy name and providing a JSON policy document:

```bash
python aws-cli-custom.py create-policy <policy_name> <policy_document>
```

Example:

```bash
python aws-cli-custom.py create-policy MyPolicy '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}'
```

### Help

To view all available commands and options, use the `-h` or `--help` flag:

```bash
python aws-cli-custom.py --help
```

## Example Commands

```bash
# Start an EC2 instance
python aws-cli-custom.py start-ec2 MyInstance

# Stop an EC2 instance
python aws-cli-custom.py stop-ec2 MyInstance

# Upload a file to an S3 bucket
python aws-cli-custom.py upload-s3 mybucket myfile.txt

# Create an IAM policy
python aws-cli-custom.py create-policy MyPolicy '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}'
```

## Error Handling

- **NoCredentialsError**: Ensure that AWS credentials are configured correctly using `aws configure`.
- **FileNotFoundError**: Verify that the file being uploaded to S3 exists and is correctly specified.
- **ClientError**: Ensure that your AWS services (like EC2 instances or IAM policies) are correctly configured and available.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License 

## Authors and Acknowledgments

Created by VanHelwig (Keenan Helwig). Special thanks to all contributors.

## Project Status

This project is actively maintained. Feel free to submit issues or suggestions for improvement.
