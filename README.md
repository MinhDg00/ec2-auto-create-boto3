# Requirements

Develop an automation program that takes a YAML configuration file as input and deploys a Linux AWS EC2 instance with two volumes and two users.

Here are some guidelines to follow:

- Create a YAML file based on the configuration provided below for consumption by your application
- You may modify the configuration, but do not do so to the extent that you fundamentally change the exercise
- Include the YAML config file in your repo
- Use Python and Boto3
- Do not use configuration management, provisioning, or IaC tools such as Ansible, CloudFormation, Terraform, etc.


# Instruction

I. Create IAM user with Programmic Access. A detail instructions can be from [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)

II. Set up credentials in `~/.aws/credentials` file with your aws_access_key_id and aws_secret_access_key. More details can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

III. Navigate to this folder and Run `main.py` 

```python
python3 main.py <aws_access_key_id> <aws_secret_access_key> <region> 
```
