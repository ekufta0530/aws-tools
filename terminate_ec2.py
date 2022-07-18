#!/opt/homebrew/bin/python3

# eric kufta
# For, ya know, terminating ec2s

import boto3
import sys

AWS_REGION = "us-east-1"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
INSTANCE_ID = sys.argv[1] # define what instance to be deleted. 

def main():
    instance = EC2_RESOURCE.Instance(INSTANCE_ID)
    print(f'Terminating EC2 instance: {instance.id}')
    instance.terminate()
    instance.wait_until_terminated()
    print(f'EC2 instance "{instance.id}" has been terminated')

if __name__ == "__main__":
    main()