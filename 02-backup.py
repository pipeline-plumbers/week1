import boto3

# Initialize EC2 client
region_name = 'us-east-1'
ec2_client = boto3.client('ec2', region_name=region_name)

def get_volume_id_from_instance(instance_id):
    volumes = ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])
    
    if volumes['Volumes']:
        volume_id = volumes['Volumes'][0]['VolumeId']
        print(f"Volume ID for instance {instance_id}: {volume_id}")
        return volume_id
    else:
        raise Exception(f"No volume found for instance {instance_id}")

# Load instance_id from file
def load_instance_id():
    with open('instance_volume_data.txt', 'r') as file:
        for line in file:
            if line.startswith('instance_id'):
                return line.strip().split('=')[1]

# Save volume_id to file
def save_volume_id(volume_id):
    with open('instance_volume_data.txt', 'a') as file:
        file.write(f"volume_id={volume_id}\n")

if __name__ == "__main__":
    instance_id = load_instance_id()
    volume_id = get_volume_id_from_instance(instance_id)
    save_volume_id(volume_id)
