import boto3

# Initialize EC2 resource and client
region_name = 'us-east-1'
ami_id = 'ami-0ebfd941bbafe70c6'
key_name = 'pipeline-plumbers'

ec2_resource = boto3.resource('ec2', region_name=region_name)

def create_ec2_instance():
    instances = ec2_resource.create_instances(
        ImageId=ami_id,
        InstanceType='t2.micro',
        KeyName=key_name,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'prod'}]
        }],
        BlockDeviceMappings=[{
            'DeviceName': '/dev/sdh',
            'Ebs': {
                'VolumeSize': 8,
                'DeleteOnTermination': True,
                'VolumeType': 'gp2'
            }
        }]
    )
    instance_id = instances[0].id
    print(f"Created EC2 instance with ID: {instance_id}")
    
    # Save instance_id to file
    with open('instance_volume_data.txt', 'w') as file:
        file.write(f"instance_id={instance_id}\n")
    
    return instance_id

if __name__ == "__main__":
    create_ec2_instance()
