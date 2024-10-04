import boto3
from operator import itemgetter

# Initialize EC2 client and resource
region_name = 'us-east-1'
ec2_client = boto3.client('ec2', region_name=region_name)
ec2_resource = boto3.resource('ec2', region_name=region_name)

# Load instance_id and volume_id from file
def load_instance_volume_data():
    data = {}
    with open('instance_volume_data.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            data[key] = value
    return data['instance_id'], data['volume_id']

def get_latest_snapshot(volume_id):
    snapshots = ec2_client.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [volume_id]}, {'Name': 'owner-id', 'Values': ['self']}]
    )['Snapshots']
    
    if not snapshots:
        raise Exception(f"No snapshots found for volume {volume_id}. Ensure the volume has at least one snapshot.")
    
    return sorted(snapshots, key=itemgetter('StartTime'), reverse=True)[0]

def create_volume_from_snapshot(snapshot_id, availability_zone):
    volume = ec2_client.create_volume(SnapshotId=snapshot_id, AvailabilityZone=availability_zone)
    return volume['VolumeId']

def wait_for_volume(volume_id):
    volume = ec2_resource.Volume(volume_id)
    while volume.state != 'available':
        volume.reload()
    print(f"Volume {volume_id} is now available.")

def attach_volume(instance_id, volume_id, device='/dev/sdf'):
    instance = ec2_resource.Instance(instance_id)
    instance.attach_volume(VolumeId=volume_id, Device=device)
    print(f"Volume {volume_id} attached to instance {instance_id}")

def recover_instance_from_snapshot():
    instance_id, volume_id = load_instance_volume_data()
    latest_snapshot = get_latest_snapshot(volume_id)
    new_volume_id = create_volume_from_snapshot(latest_snapshot['SnapshotId'], 'us-east-1a')
    wait_for_volume(new_volume_id)
    attach_volume(instance_id, new_volume_id)

if __name__ == "__main__":
    recover_instance_from_snapshot()
