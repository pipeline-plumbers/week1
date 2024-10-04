import boto3

# Initialize EC2 resource and client
region_name = 'us-east-1'
ec2_resource = boto3.resource('ec2', region_name=region_name)
ec2_client = boto3.client('ec2', region_name=region_name)

# Load instance_id and volume_id from file
def load_instance_volume_data():
    data = {}
    with open('instance_volume_data.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            data[key] = value
    return data['instance_id'], data['volume_id']

def delete_ec2_instance():
    try:
        instance_id, volume_id = load_instance_volume_data()

        # Terminate the EC2 instance
        instance = ec2_resource.Instance(instance_id)
        instance.terminate()
        instance.wait_until_terminated()
        print(f"Instance {instance_id} terminated.")
        
        # Delete the attached volume
        ec2_client.delete_volume(VolumeId=volume_id)
        print(f"Volume {volume_id} deleted.")
    except Exception as e:
        print(f"Error during EC2 instance deletion: {e}")

def delete_snapshots():
    try:
        _, volume_id = load_instance_volume_data()

        # Get and delete snapshots for the given volume
        snapshots = ec2_client.describe_snapshots(Filters=[{'Name': 'volume-id', 'Values': [volume_id]}, {'Name': 'owner-id', 'Values': ['self']}])['Snapshots']
        for snapshot in snapshots:
            ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            print(f"Deleted snapshot {snapshot['SnapshotId']}.")
    except Exception as e:
        print(f"Error during snapshot deletion: {e}")

if __name__ == "__main__":
    delete_ec2_instance()
    delete_snapshots()
