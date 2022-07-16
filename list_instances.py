#!/opt/homebrew/bin/python3

import boto3

AWS_REGION = "us-east-1"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
INSTANCE_STATE = 'running'
KEY_PAIR_NAME = 'eric.kufta'

instances = EC2_RESOURCE.instances.filter(
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

print(f'Instances in state "{INSTANCE_STATE}":')
user_instances=[i for i in instances]
for instance in instances:
    print(f'  - Instance ID: {instance.id}')