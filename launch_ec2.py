#!/opt/homebrew/bin/python3

# Eric Kufta | Datadog
# link to documention in atlassian
'''
Improvements:
1) command line args for instance name + random name generator
2) Change size of ebs volume (can do this through custom ami)
3) User data script for installing datadog agent
Ideas:
Be able to create config files for instances, some generic ones out of the box

'''

import boto3

# CHANGE THESE AS NEEDED
INSTANCE_NAME = 'generic_sandbox'
SECURITY_GROUP_ID = 'sg-0348948a9f025a14e' # Optionally use your own custom security group 
KEY_PAIR_NAME = 'eric.kufta'
INSTANCE_TYPE = 't3.small' # t3.medium t3.large !!please do not over-provision!!
AMI_ID = 'ami-005de95e8ff495156' # Ubuntu 18.04 | ami-041306c411c38a789 for Windows 2019 Base
# USER_DATA = Script to install agent automatically

# Keep these unless you know what you are doing
AWS_REGION = "us-east-1"
SUBNET_ID = 'subnet-3f5db45b' # sandbox- private | For public access: https://github.com/DataDog/devops/wiki/AWS-Sandbox#using-a-custom-security-group
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
EC2_CLIENT = boto3.client('ec2', region_name=AWS_REGION)
INSTANCE_STATE = 'running'
INSTANCE_LIMIT = 3

def create_instance():
    instances = EC2_RESOURCE.create_instances(
        MinCount = 1,
        MaxCount = 1,
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_PAIR_NAME,
        SecurityGroupIds=[
            SECURITY_GROUP_ID,
        ],
        SubnetId=SUBNET_ID,
        TagSpecifications=[
         {
                'ResourceType': 'instance',
               'Tags': [
                  {
                      'Key': 'Name',
                      'Value': INSTANCE_NAME
                 },
                 {
                     'Key': 'team',
                     'Value': 'mcse'
                 },
                  {
                     'Key': 'purpose',
                        'Value': 'sandbox'
                 },
                 {
                     'Key': 'created_by', # assumes your key pair name matches your aws user id
                     'Value': KEY_PAIR_NAME
                    },
                    {
                     'Key': 'source', #for internal tracking of usage
                     'Value': 'quickstartscript'
                    },
             ]
            },
        ]
    )
    return instances

# this will also call create_instance()
def print_details():
    instances = create_instance()
    for instance in instances:
        print(f'EC2 instance "{instance.id}" has been launched\n')
        print('For easy access, copy paste this into your ~/.ssh/config:\n')
        print(f'Host {INSTANCE_NAME}')
        print(f'HostName {instance.private_ip_address}')
        print('User ubuntu')
        print(f'IdentityFile ~/.ssh/{KEY_PAIR_NAME}.pem\n')
    instance.wait_until_running()
    print(f'EC2 instance "{instance.id}" has been started')

def main():
# Pull list of running instances for this user
    running_instances = EC2_RESOURCE.instances.filter(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    INSTANCE_STATE
                ]
            },
            {
                'Name': 'tag:created_by',
                'Values': [
                    KEY_PAIR_NAME
                ]
            }
        ]
    )
    #If user is under limit for allowed instances, spin up the new one and output instance details
    user_instances=[i for i in running_instances]
    if len(user_instances) < INSTANCE_LIMIT:
        print_details() # also creates the instance
    else:
        print(f'You can only run {INSTANCE_LIMIT} instances at a time. Please terminate some to proceed')
        print(f'Instances in {INSTANCE_STATE} state:')
        for instance in running_instances:
            print(f'- Instance ID: {instance.id}')

if __name__ == "__main__":
    main()